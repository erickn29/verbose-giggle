from uuid import UUID

from base.model import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Question(Base):
    __tablename__ = "question"

    text: Mapped[str] = mapped_column(Text, doc="Вопрос")
    technology: Mapped[str] = mapped_column(doc="Технология")

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
