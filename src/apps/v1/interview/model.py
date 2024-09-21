from uuid import UUID

from base.model import Base
from sqlalchemy import JSON, ForeignKey, Text
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
    
    
class Chat(Base):
    __tablename__ = "chat"
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        doc="Пользователь",
    )
    title: Mapped[str] = mapped_column(Text, doc="Название чата")
    config: Mapped[dict] = mapped_column(JSON, doc="Конфигурация")
    
    user = relationship("User", back_populates="chats", lazy="joined")
    messages = relationship("Message", back_populates="chat", lazy="selectin")
    
    
class Message(Base):
    __tablename__ = "message"
    
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"),
        doc="Сообщение"
    )
    is_user_message: Mapped[bool]
    text: Mapped[str] = mapped_column(Text, doc="Текст сообщения")
    
    chat = relationship("Chat", back_populates="messages", lazy="joined")
