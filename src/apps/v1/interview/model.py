from uuid import UUID

from base.model import Base
from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Question(Base):
    __tablename__ = "question"

    text: Mapped[str] = mapped_column(Text, doc="Вопрос")
    technology: Mapped[str] = mapped_column(doc="Технология")
    complexity: Mapped[str] = mapped_column(doc="Сложность")

    answers = relationship(
        "Answer",
        back_populates="question",
        lazy="selectin",
    )


class Answer(Base):
    __tablename__ = "answer"

    text: Mapped[str] = mapped_column(Text, doc="Текст ответа")
    score: Mapped[int] = mapped_column(doc="Балл")
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE"),
        doc="ID вопроса",
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        doc="Пользователь",
    )

    question = relationship("Question", back_populates="answers", lazy="joined")
    user = relationship("User", back_populates="answers", lazy="joined")
    evaluations = relationship("Evaluation", back_populates="answer", lazy="selectin")


class Evaluation(Base):
    __tablename__ = "evaluation"

    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE"),
        doc="ID ответа",
    )
    text: Mapped[str] = mapped_column(Text, doc="Текст ответа модели")

    answer = relationship("Answer", back_populates="evaluations", lazy="joined")


class Chat(Base):
    __tablename__ = "chat"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        doc="Пользователь",
    )
    title: Mapped[str] = mapped_column(Text, doc="Название чата")
    config: Mapped[dict] = mapped_column(JSON, doc="Конфигурация")

    user = relationship("User", back_populates="chats", lazy="joined")
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Message.created_at"
    )


class Message(Base):
    __tablename__ = "message"

    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"), doc="Сообщение"
    )
    text: Mapped[str] = mapped_column(Text, doc="Текст сообщения")
    type: Mapped[str] = mapped_column(String, doc="Тип сообщения")
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE"),
        doc="ID вопроса",
        nullable=True,
    )
    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE"),
        doc="ID ответа",
        nullable=True,
    )
    evaluation_id: Mapped[UUID] = mapped_column(
        ForeignKey("evaluation.id", ondelete="CASCADE"),
        doc="ID оценки",
        nullable=True,
    )

    chat = relationship("Chat", back_populates="messages", lazy="joined")
