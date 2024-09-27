from apps.v1.interview.model import Answer, Chat, Evaluation, Message, Question
from apps.v1.user.model import User
from apps.v1.user.service import UserService
from core.database import db_conn
from fastapi import FastAPI
from pydantic import BaseModel
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request


class UpdateUserPassword(BaseModel):
    password: str


class UserAdmin(ModelView, model=User):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        User.id,
        User.email,
        User.is_active,
        User.is_admin,
        User.is_verified,
        User.coin,
        User.subscription,
        User.created_at,
    ]
    column_sortable_list = [User.email, User.created_at, User.is_active]
    column_searchable_list = [User.email]
    column_default_sort = [(User.created_at, True), (User.email, False)]
    column_labels = {k: v.doc for k, v in User.__mapper__.columns.items() if v.doc}
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    async def after_model_change(
        self, data: dict, model: User, is_created: bool, request: Request
    ) -> None:
        session_generator = db_conn.get_session()
        session = await anext(session_generator)
        async with session:
            await UserService(session=session).update(
                model.id,
                UpdateUserPassword(password=data.get("password")),
            )
            
            
class ChatAdmin(ModelView, model=Chat):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Chat.id,
        Chat.title,
        Chat.created_at,
    ]
    column_sortable_list = [
        Chat.title,
        Chat.created_at,
    ]
    column_searchable_list = [Chat.title]
    column_labels = {k: v.doc for k, v in Chat.__mapper__.columns.items() if v.doc}
    name = "Чат"
    name_plural = "Чаты"
    icon = "fa-solid fa-comment"
    
    
class MessageAdmin(ModelView, model=Message):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Message.id,
        Message.type,
        Message.created_at,
        Message.text,
    ]
    column_sortable_list = [
        Message.type,
        Message.created_at,
    ]
    column_searchable_list = [Message.text]
    column_labels = {k: v.doc for k, v in Message.__mapper__.columns.items() if v.doc}
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-message"


class QuestionAdmin(ModelView, model=Question):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Question.id,
        Question.text,
        Question.technology,
        Question.complexity,
        Question.created_at,
    ]
    column_sortable_list = [
        Question.technology,
        Question.created_at,
        Question.complexity,
    ]
    column_searchable_list = [Question.text]
    column_labels = {k: v.doc for k, v in Question.__mapper__.columns.items() if v.doc}
    name = "Вопрос"
    name_plural = "Вопросы"
    icon = "fa-solid fa-question"


class AnswerAdmin(ModelView, model=Answer):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Answer.id,
        Answer.text,
        Answer.score,
        Answer.created_at,
    ]
    column_sortable_list = [
        Answer.score,
        Answer.created_at,
    ]
    column_searchable_list = [Answer.text]
    column_labels = {k: v.doc for k, v in Answer.__mapper__.columns.items() if v.doc}
    name = "Ответ"
    name_plural = "Ответы"
    icon = "fa-solid fa-lightbulb"
    
    
class EvaluationAdmin(ModelView, model=Evaluation):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Evaluation.id,
        Evaluation.created_at,
        Evaluation.text,
    ]
    column_sortable_list = [
        Evaluation.created_at,
    ]
    column_searchable_list = [Evaluation.text]
    column_labels = {k: v.doc for k, v in Evaluation.__mapper__.columns.items() if v.doc}
    name = "Ответ модели"
    name_plural = "Ответы модели"
    icon = "fa-solid fa-brain"


# class RecoveryTokenAdmin(ModelView, model=RecoveryToken):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         RecoveryToken.id,
#         RecoveryToken.user,
#         RecoveryToken.token,
#         RecoveryToken.is_used,
#         RecoveryToken.created_at,
#     ]
#     column_sortable_list = [RecoveryToken.user, RecoveryToken.created_at]
#     column_searchable_list = [RecoveryToken.user]
#     column_labels = {
#         k: v.doc for k, v in RecoveryToken.__mapper__.columns.items() if v.doc
#     }
#     name = "Токен восстановления пароля"
#     name_plural = "Токены восстановления пароля"
#     icon = "fa-solid fa-lock"


# class ProjectAdmin(ModelView, model=Project):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [Project.id, Project.title, Project.created_at]
#     column_sortable_list = [Project.title, Project.created_at]
#     column_searchable_list = [Project.title]
#     column_labels = {k: v.doc for k, v in Project.__mapper__.columns.items() if v.doc}
#     name = "Проект"
#     name_plural = "Проекты"
#     icon = "fa-solid fa-box-open"


# class CategoryAdmin(ModelView, model=Category):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         Category.id,
#         Category.title,
#         Category.status,
#         Category.created_at,
#     ]
#     column_sortable_list = [Category.project_id, Category.created_at]
#     column_searchable_list = [Category.title]
#     name = "Категория сайта"
#     name_plural = "Категории сайта"
#     icon = "fa-solid fa-folder"


# class PageAdmin(ModelView, model=Page):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         Page.id,
#         Page.family,
#         Page.title,
#         Page.action,
#         Page.project_id,
#         Page.created_at,
#     ]
#     column_sortable_list = [Page.family, Page.action, Page.project_id, Page.created_at]
#     column_searchable_list = [Page.family, Page.action, Page.title]
#     column_labels = {k: v.doc for k, v in Page.__mapper__.columns.items() if v.doc}
#     name = "Страница сайта"
#     name_plural = "Страницы сайта"
#     icon = "fa-solid fa-file"


# class GroupAdmin(ModelView, model=Group):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         Group.id,
#         Group.title,
#         Group.project_id,
#         Group.created_at,
#     ]
#     column_sortable_list = [Group.project_id, Group.created_at]
#     column_searchable_list = [Group.title]
#     name = "Группа компонентов"
#     name_plural = "Группы компонентов"
#     icon = "fa-solid fa-folder"


# class ComponentAdmin(ModelView, model=Component):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         Component.id,
#         Component.title,
#         Component.group_id,
#         Component.created_at,
#     ]
#     column_sortable_list = [Component.title, Component.created_at]
#     column_searchable_list = [Component.title]
#     name = "Компонент"
#     name_plural = "Компоненты"
#     icon = "fa-solid fa-file"


# class ProjectUserAdmin(ModelView, model=ProjectUser):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         ProjectUser.user_id,
#         ProjectUser.project_id,
#         ProjectUser.created_at,
#     ]
#     column_sortable_list = [
#         ProjectUser.project_id,
#         ProjectUser.created_at,
#     ]
#     column_searchable_list = []
#     column_labels = {
#         k: v.doc for k, v in ProjectUser.__mapper__.columns.items() if v.doc
#     }
#     name = "Пользователь проекта"
#     name_plural = "Пользователи проекта"
#     icon = "fa-solid fa-people-carry-box"


# class StandAdmin(ModelView, model=Stand):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [Stand.id, Stand.title, Stand.project_id, Stand.created_at]
#     column_sortable_list = [Stand.title, Stand.project_id, Stand.created_at]
#     column_searchable_list = [Stand.title]
#     column_labels = {k: v.doc for k, v in Stand.__mapper__.columns.items() if v.doc}
#     name = "Стенд"
#     name_plural = "Стенды"
#     icon = "fa-solid fa-code-branch"


# class SettingsAdmin(ModelView, model=Settings):
#     page_size = 50
#     page_size_options = [25, 50, 100, 200]
#     column_list = [
#         Settings.id,
#         Settings.title,
#         Settings.domain,
#         Settings.created_at,
#     ]
#     column_sortable_list = [Settings.title, Settings.domain, Settings.created_at]
#     column_searchable_list = [Settings.title, Settings.domain]
#     name = "Настройки сайта"
#     name_plural = "Настройки сайта"
#     icon = "fa-solid fa-cog"


def init_admin(
    app: FastAPI,
    engine: AsyncEngine,
    title: str,
    authentication_backend: AuthenticationBackend,
):
    admin = Admin(
        app=app,
        engine=engine,
        title=title,
        authentication_backend=authentication_backend,
    )

    admin.add_view(UserAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(AnswerAdmin)
    admin.add_view(EvaluationAdmin)

    return admin
