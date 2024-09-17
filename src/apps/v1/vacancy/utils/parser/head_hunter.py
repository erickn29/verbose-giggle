import asyncio
import json

from apps.v1.vacancy.schema import (
    CityInputSchema,
    CompanyInputSchema,
    ToolInputSchema,
    VacancyCreateSchema,
    VacancyInputSchema,
)
from apps.v1.vacancy.service import VacancyService
from apps.v1.vacancy.utils.parser.analyzer import Analyzer
from apps.v1.vacancy.utils.parser.base import BaseParser
from bs4 import BeautifulSoup
from core.database import async_session_maker
from fastapi import HTTPException
from tqdm import tqdm


class HeadHunterParser(BaseParser):
    LINK = "https://hh.ru/search/vacancy?area=113&employment=full&excluded_text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%2C%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B0%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B8&search_field=name&search_field=description&only_with_salary=true&text=python+OR+php+OR+c%2B%2B+OR+c%23+OR+javascript+OR+java&no_magic=true&L_save_area=true&search_period=1&items_on_page=20&hhtmFrom=vacancy_search_list&page=0"  # noqa: E501
    RUR_CODE = "RUR"

    def content_to_dict(self, content: str, html_tag: str, html_id: str) -> dict | None:
        soup = BeautifulSoup(content, "html.parser")
        bs4_data = soup.find(html_tag, {"id": html_id})
        if not bs4_data or not bs4_data.contents:
            print(f"No vacancies found {self.LINK}")
            return
        bs4_text = str(bs4_data.contents[0])
        return json.loads(bs4_text)

    @staticmethod
    def get_page_count(content_dict: dict) -> int:
        page_count = 0
        if not content_dict.get("paging"):
            return page_count
        if not content_dict["paging"].get("lastPage"):
            return page_count
        if not content_dict["paging"]["lastPage"].get("page"):
            return page_count
        return content_dict["paging"]["lastPage"].get("page")

    def get_all_vacancies_links(self, only_one: bool = False) -> list:
        content = self.get_page_content(self.LINK)
        if not content:
            print(f"No content {self.LINK}")
        vacancies_dict = self.content_to_dict(
            content,
            "template",
            "HH-Lux-InitialState",
        )
        page_count = self.get_page_count(vacancies_dict["vacancySearchResult"])
        vacancies_list = []
        if only_one:
            vacancies_list.extend(self.get_vacancies_links(self.LINK))
            return vacancies_list
        last_number = 0
        last_link = self.LINK
        for page_number in tqdm(range(page_count)):
            link = last_link.replace(
                f"&page={str(last_number)}", f"&page={str(page_number)}"
            )
            last_link = link
            try:
                vacancies_list.extend(self.get_vacancies_links(link))
                last_number = page_number
            except Exception:
                continue
        print(len(vacancies_list), len(set(vacancies_list)))
        return vacancies_list

    def get_vacancies_list(self, link: str) -> list | None:
        content = self.get_page_content(link)
        if not content:
            print(f"No content {link}")
        vacancies_dict = self.content_to_dict(
            content,
            "template",
            "HH-Lux-InitialState",
        )
        if not vacancies_dict or not vacancies_dict.get("vacancySearchResult"):
            print(f"No vacancies in page content {link}")
            return
        return vacancies_dict["vacancySearchResult"].get("vacancies")

    def get_vacancies_links(self, link: str) -> list | None:
        vacancies_list = self.get_vacancies_list(link)
        if not vacancies_list:
            print(f"Empty vacancies list {link}")
            return
        links = []
        for vacancy in vacancies_list:
            if not vacancy.get("links") or not vacancy.get("links").get("desktop"):
                continue
            links.append(vacancy.get("links").get("desktop"))
        return links

    def get_vacancy_data(self, link: str):
        content = self.get_page_content(link)
        vacancy_dict = self.content_to_dict(content, "template", "HH-Lux-InitialState")
        if not vacancy_dict or not vacancy_dict.get("vacancyView"):
            print(f"No vacancy in page content {link}")
            return
        return vacancy_dict["vacancyView"]

    def get_vacancy_schema(self, link: str) -> VacancyCreateSchema | None:
        vacancy_data: dict = self.get_vacancy_data(link)
        if not vacancy_data:
            print(f"No vacancy data found {link}")
            return
        if not vacancy_data.get("area") or not vacancy_data.get("area").get("name"):
            print(f"No area data found {link}")
            return
        city = CityInputSchema(name=vacancy_data.get("area").get("name"))
        if not vacancy_data.get("company") or not vacancy_data.get("company").get(
            "name"
        ):
            print(f"No company data found {link}")
        company = CompanyInputSchema(name=vacancy_data.get("company").get("name"))
        tools = []
        if skills := vacancy_data.get("keySkills"):
            tools = [
                ToolInputSchema(name=tool) for tool in skills.get("keySkill") or []
            ]
        if not vacancy_data.get("compensation"):
            print(f"No compensation data found {link}")
        salary_from = vacancy_data["compensation"].get("from")
        salary_to = vacancy_data["compensation"].get("to")
        if not any([salary_from, salary_to]):
            print(f"No salary data found (from, to) {link}")
            return
        salary_from = (
            salary_from * self.DOLLAR_TO_RUB
            if vacancy_data["compensation"]["currencyCode"] != self.RUR_CODE
            and salary_from
            else salary_from
        )
        salary_to = (
            salary_to * self.DOLLAR_TO_RUB
            if vacancy_data["compensation"]["currencyCode"] != self.RUR_CODE
            and salary_to
            else salary_to
        )
        analyzer = Analyzer(
            title=vacancy_data.get("name"),
            description=vacancy_data.get("description"),
            tools=vacancy_data.get("keySkills").get("keySkill") if tools else [],
            experience=vacancy_data.get("workExperience"),
        )
        language = analyzer.get_language()
        speciality = analyzer.get_speciality()
        experience = analyzer.get_head_hunter_experience()
        if not all(
            [
                language,
                speciality,
                experience,
            ]
        ):
            print(
                f"No vacancy data found ({language}, {speciality}, {experience}) {link}"
            )
            return
        vacancy = VacancyInputSchema(
            title=vacancy_data.get("name"),
            description=vacancy_data.get("description"),
            language=language,
            speciality=speciality,
            experience=experience,
            salary_from=salary_from,
            salary_to=salary_to,
        )
        vacancy_schema = VacancyCreateSchema(
            city=city,
            company=company,
            vacancy=vacancy,
            tool=tools,
        )
        return vacancy_schema

    async def get_vacancies(
        self,
        save: bool = True,
        only_one: bool = False,
    ):
        links = self.get_all_vacancies_links(only_one=only_one)
        vacancy_service = VacancyService(session=async_session_maker())
        if only_one:
            return self.get_vacancy_schema(links[0])
        for link in tqdm(links):
            await asyncio.sleep(self.get_sleep_time())
            vacancy_schema = self.get_vacancy_schema(link)
            if not vacancy_schema:
                continue
            if not save:
                continue
            try:
                await vacancy_service.create(vacancy_schema)
            except HTTPException as exc:
                print(exc)
                continue


async def main():
    parser = HeadHunterParser()
    await parser.get_vacancies()


if __name__ == "__main__":
    asyncio.run(main())
