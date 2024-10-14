from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MessageType(Enum):
    QUESTION = "question"
    ANSWER = "answer"
    EVALUATION = "evaluation"


class MessageCreateInputSchema(BaseModel):
    chat_id: UUID
    text: str
    type: str
    question_id: UUID | None = None
    answer_id: UUID | None = None
    evaluation_id: UUID | None = None


class MessageCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chat_id: UUID
    text: str
    type: str
    question_id: UUID | None = None
    answer_id: UUID | None = None
    evaluation_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class TechnologySchema(BaseModel):
    technology: str
    complexity: str


class ChatConfigSchema(BaseModel):
    technologies: list[TechnologySchema]


class ChatCreateInputSchema(BaseModel):
    user_id: UUID | None = None
    title: str = Field(min_length=1, max_length=64)
    config: ChatConfigSchema


class ChatCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    config: ChatConfigSchema
    # messages: list[MessageCreateOutputSchema]
    created_at: datetime
    updated_at: datetime


class ChatDetailOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    config: ChatConfigSchema
    messages: list[MessageCreateOutputSchema] = []
    created_at: datetime
    updated_at: datetime


class ChatListOutputSchema(BaseModel):
    items: list[ChatCreateOutputSchema]


class QuestionOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    technology: str
    complexity: str


class AnswerCreateInputSchema(BaseModel):
    question_id: UUID
    user_id: UUID | None = None
    text: str
    score: int = 0


class AnswerUpdateInputSchema(BaseModel):
    score: int | None = None


class AnswerCreateOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question_id: UUID
    user_id: UUID
    text: str
    score: int
    created_at: datetime
    updated_at: datetime


class EvaluationInputSchema(BaseModel):
    answer_id: UUID
    text: str
