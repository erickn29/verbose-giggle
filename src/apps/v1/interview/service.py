import random

from uuid import UUID

from apps.v1.interview.model import Answer, Chat
from apps.v1.interview.repository import (
    AnswerRepository,
    ChatRepository,
    EvaluationRepository,
    MessageRepository,
    QuestionRepository,
)
from apps.v1.interview.schema import (
    AnswerCreateInputSchema,
    AnswerUpdateInputSchema,
    EvaluationInputSchema,
    MessageCreateInputSchema,
    MessageType,
)
from apps.v1.interview.utils.request import get_evaluation
from apps.v1.user.model import User
from base.service import BaseService
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=ChatRepository)


class QuestionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=QuestionRepository)

    async def get_question(self, chat_id: UUID, user: User) -> str:
        chat_service = ChatService(self.session)
        question_service = QuestionService(self.session)

        chat = await chat_service.get(chat_id)
        used_question_ids = [answer.question_id for answer in user.answers]
        questions_by_chat_config = await question_service.fetch(
            {
                "technology": {
                    "in": [t.get("technology") for t in chat.config["technologies"]]
                },
                "complexity": {
                    "in": [t.get("complexity") for t in chat.config["technologies"]]
                },
                "id": {"not_in": used_question_ids},
            }
        )
        if not questions_by_chat_config:
            return "Все вопросы кончились =("
        question = random.choice(questions_by_chat_config)
        message_service = MessageService(self.session)
        await message_service.create(
            MessageCreateInputSchema(
                chat_id=chat_id,
                text=question.text,
                type=MessageType.QUESTION.value,
                question_id=question.id
            )
        )
        return question


class AnswerService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=AnswerRepository)

    async def get_answer(
        self,
        schema: AnswerCreateInputSchema,
        user: User,
        chat_id: UUID,
    ) -> Answer:
        chat_service = ChatService(self.session)
        message_service = MessageService(self.session)
        evaluation_service = EvaluationService(self.session)
        schema.user_id = user.id

        chat = await chat_service.get(chat_id)
        answer = await self.create(schema)
        await message_service.create(
            MessageCreateInputSchema(
                chat_id=chat.id,
                text=answer.text,
                type=MessageType.ANSWER.value,
                answer_id=answer.id,
            )
        )
        await evaluation_service.get_evaluation(chat, answer)
        return answer
        
        
class EvaluationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=EvaluationRepository)
        
    async def get_evaluation(self, chat: Chat, answer: Answer):
        message_service = MessageService(self.session)
        technologies = [t.get("technology") for t in chat.config["technologies"]]
        default_text = "Что-то пошло не так, попробуйте позже"
        prompt = f"""
        Ты - опытный разработчик. Ты эксперт в таких технологиях как 
        {''.join(technologies)}. 
        На вход тебе подается вопрос и ответ на него. 
        Очень строго и внимательно проверяй правильность и полноту ответа на вопрос. 
        В ответе дававй оценку ответу пользователя на вопрос. 
        Говори что верно и что неверно сказано. Что можно добавить к ответу на вопрос.
        Формат ответа:
        - оценка от 1 до 10 (например 5/10)
        - что сказано верно
        - что сказано неверно
        - рекомендации
        """
        question = answer.question
        user_answer = f"""
        Вопрос: {question.text}.
        Ответ: {answer.text}.
        """
        response = await get_evaluation(
            url=settings.ai.SERVICE_URL,
            data={
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_answer},
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        if (
            not response
            or not response.get("choices")
            or not response["choices"][0].get("message")
            or not response["choices"][0]["message"].get("content")
        ):
            await message_service.create(
                MessageCreateInputSchema(
                    chat_id=chat.id,
                    text=default_text,
                    type=MessageType.EVALUATION.value,
                )
            )
            return
        evaluation_text = response["choices"][0]["message"]["content"].strip().replace("\n", "<br>")
        evaluation = await self.create(
            EvaluationInputSchema(
                answer_id=answer.id,
                text=evaluation_text
            )
        )
        await message_service.create(
            MessageCreateInputSchema(
                chat_id=chat.id,
                text=evaluation_text,
                type=MessageType.EVALUATION.value,
                evaluation_id=evaluation.id
            )
        )
        if "Оценка: " in evaluation_text and "/10" in evaluation_text:
            eval_string = evaluation_text.split("/10")[0]
            eval_num = eval_string.split(" ")[-1]
            if eval_num.isdigit():
                await self.update(
                    answer.id, AnswerUpdateInputSchema(score=int(eval_num))
                )
        


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=MessageRepository)
        
        
if __name__ == "__main__":
    if not 0 or 1 or 0: print("false")
