from src.apps.v1.vacancy.service import VacancyService

import pytest

from fastapi import HTTPException


class TestOutput:
    async def test_vacancy_list(self, client, vacancy_output):
        response = await client.get("/api/v1/job/vacancy/")
        assert isinstance(response.json()["vacancies"], list)
        assert len(response.json()["vacancies"]) > 0
        assert response.json()["vacancies"][0]["id"] == str(
            vacancy_output["vacancy"].id
        )

    async def test_vacancy_detail(self, client, vacancy_output):
        response = await client.get(
            f"/api/v1/job/vacancy/{str(vacancy_output["vacancy"].id)}/"
        )
        assert response.json()["id"] == str(vacancy_output["vacancy"].id)
        assert response.json()["title"] == vacancy_output["vacancy"].title

    async def test_create_vacancy(self, client, vacancy_output, session):
        data = {
            "city": {"name": "Moscow"},
            "company": {
                "name": "Google",
                "description": "string",
            },
            "vacancy": {
                "title": "Test1",
                "description": "string",
                "language": "python",
                "speciality": "разработка",
                "experience": "без опыта",
                "salary_from": 10000,
                "salary_to": 20000,
            },
            "tool": [{"name": "qwerty"}, {"name": "asdfg"}],
        }
        await client.post("/api/v1/job/vacancy/", json=data)
        async with session:
            vacancy_service = VacancyService(session)
            vacancy_list = await vacancy_service.fetch({"title": "Test1"})
            assert len(vacancy_list) == 1
            assert vacancy_list[0].title == "Test1"
            assert vacancy_list[0].tools is not None
            assert isinstance(vacancy_list[0].tools, list)
            assert set([vt.tool.name for vt in vacancy_list[0].tools]) == {
                "qwerty",
                "asdfg",
            }

    async def test_update_vacancy(self, client, vacancy_output, session):
        async with session:
            vacancy_service = VacancyService(session)
            vacancy = await vacancy_service.get_object(vacancy_output["vacancy"].id)

        data = {
            "city": {"name": "city.name"},
            "company": {
                "name": "company.name",
                "description": "string",
            },
            "vacancy": {
                "title": "updated_title",
                "description": "string",
                "language": "python",
                "speciality": "разработка",
                "experience": "без опыта",
                "salary_from": 100000,
                "salary_to": 200000,
            },
            "tool": [{"name": "zxcvb"}],
        }
        response = await client.put(
            f"/api/v1/job/vacancy/{str(vacancy_output["vacancy"].id)}/", json=data
        )
        async with session:
            vacancy_service = VacancyService(session)
            vacancy = await vacancy_service.get_schema(vacancy_output["vacancy"].id)
        assert vacancy.title == data["vacancy"]["title"]
        assert len(vacancy.tool) == 1
        assert vacancy.tool[0].name == data["tool"][0]["name"]

    async def test_update_vacancy_modify_tools(self, client, vacancy_output, session):
        async with session:
            vacancy_service = VacancyService(session)
            vacancy = await vacancy_service.get_object(vacancy_output["vacancy"].id)
        company = vacancy.company
        city = company.city

        data = {
            "city": {"name": city.name},
            "company": {
                "name": company.name,
                "description": "string",
            },
            "vacancy": {
                "title": "updated_title",
                "description": "string",
                "language": "python",
                "speciality": "разработка",
                "experience": "без опыта",
                "salary_from": 100000,
                "salary_to": 200000,
            },
            "tool": [{"name": "zxcvb"}, {"name": "asdfg"}],
        }
        await client.put(
            f"/api/v1/job/vacancy/{str(vacancy_output["vacancy"].id)}/", json=data
        )
        async with session:
            vacancy_service = VacancyService(session)
            vacancy = await vacancy_service.get_schema(vacancy_output["vacancy"].id)
        assert vacancy.title == data["vacancy"]["title"]
        assert len(vacancy.tool) == 2
        assert set([vt.name for vt in vacancy.tool]) == {
            "zxcvb",
            "asdfg",
        }

    async def test_delete_vacancy(self, client, vacancy_output, session):
        await client.delete(
            f"/api/v1/job/vacancy/{str(vacancy_output["vacancy_del"].id)}/"
        )
        async with session:
            vacancy_service = VacancyService(session)
            with pytest.raises(HTTPException):
                await vacancy_service.get_schema(vacancy_output["vacancy_del"].id)
