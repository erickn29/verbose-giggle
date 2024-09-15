import random

import requests


class BaseParser:
    LINK = None

    HH_LINK = "https://hh.ru/search/vacancy?area=113&employment=full&excluded_text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%2C%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B0%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B8&search_field=name&search_field=description&only_with_salary=true&text=python+OR+php+OR+c%2B%2B+OR+c%23+OR+javascript+OR+java&no_magic=true&L_save_area=true&search_period=1&items_on_page=20&hhtmFrom=vacancy_search_list"  # noqa: E501
    HABR_LINK = "https://career.habr.com/vacancies/rss?currency=RUR&s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=6&s[]=77&s[]=83&s[]=86&s[]=73&s[]=8&s[]=9&s[]=85&s[]=7&s[]=75&sort=relevance&type=all&with_salary=true"  # noqa: E501
    SUPERJOB_LINK = "https://russia.superjob.ru/vacancy/search/?keywords=c%23%2Cpython%2Cjavascript%2Cphp%2Cc%2B%2B%2Cjava&payment_value=20000&period=1&payment_defined=1&click_from=facet"  # noqa: E501
    GETMATCH_LINK = "https://getmatch.ru/vacancies?sa=150000&l=moscow&l=remote&l=saints_p&pa=3d&s=landing_ca_header"  # noqa: E501

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",  # noqa: E501
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept-encoding": "gzip,deflate,br",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa: E501
    }

    STOP_WORDS = (
        "1C",
        "1С",
        "1с",
        "1c",
        "машинист",
        "водитель",
        "таксист",
        "курьер",
        "охранник",
        "поддержки",
        "поддержку",
        "оператор",
        "поддержка",
        "маркетолог",
        "онлайн-поддержки",
        "менеджер",
        "инженер-проектировщик",
    )

    DOLLAR_TO_RUB = 100
    EURO_TO_RUB = 100

    @staticmethod
    def get_sleep_time():
        return random.randint(1, 3)

    def get_page_content(self, link: str) -> str | None:
        try:
            response = requests.get(link, headers=self.HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"Bad response {link}")
                return None
            return response.text
        except requests.exceptions.RequestException:
            print(f"Request failed {link}")
            return


# class HeadHunterParser(BaseParser):
#     LINK = "https://hh.ru/search/vacancy?area=113&employment=full&excluded_text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%2C%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B0%2C%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B8&search_field=name&search_field=description&only_with_salary=true&text=python+OR+php+OR+c%2B%2B+OR+c%23+OR+javascript+OR+java&no_magic=true&L_save_area=true&search_period=1&items_on_page=20&hhtmFrom=vacancy_search_list"  # noqa: E501
#     RUR_CODE = "RUR"
#
#     def content_to_dict(self, content: str, html_tag: str, html_id: str) -> dict | None:
#         soup = BeautifulSoup(content, "html.parser")
#         bs4_data = soup.find(html_tag, {"id": html_id})
#         if not bs4_data or not bs4_data.contents:
#             print(f"No vacancies found {self.LINK}")
#             return
#         bs4_text = str(bs4_data.contents[0])
#         return json.loads(bs4_text)
#
#     def get_vacancies_list(self) -> list | None:
#         content = self.get_page_content(self.LINK)
#         if not content:
#             print(f"No content {self.LINK}")
#         vacancies_dict = self.content_to_dict(
#             content,
#             "template",
#             "HH-Lux-InitialState",
#         )
#         if not vacancies_dict or not vacancies_dict.get("vacancySearchResult"):
#             print(f"No vacancies in page content {self.LINK}")
#             return
#         return vacancies_dict["vacancySearchResult"].get("vacancies")
#
#     def get_vacancies_links(self) -> list | None:
#         vacancies_list = self.get_vacancies_list()
#         if not vacancies_list:
#             print(f"Empty vacancies list {self.LINK}")
#             return
#         links = []
#         for vacancy in vacancies_list:
#             if not vacancy.get("links") or not vacancy.get("links").get("desktop"):
#                 continue
#             links.append(vacancy.get("links").get("desktop"))
#         return links
#
#     def get_vacancy_data(self, link: str):
#         content = self.get_page_content(link)
#         vacancy_dict = self.content_to_dict(content, "template", "HH-Lux-InitialState")
#         if not vacancy_dict or not vacancy_dict.get("vacancyView"):
#             print(f"No vacancy in page content {link}")
#             return
#         return vacancy_dict["vacancyView"]
#
#     def get_vacancy_schema(self, link: str) -> VacancyCreateSchema | None:
#         vacancy_data: dict = self.get_vacancy_data(link)
#         if not vacancy_data:
#             print(f"No vacancy data found {link}")
#             return
#         if not vacancy_data.get("area") or not vacancy_data.get("area").get("name"):
#             print(f"No area data found {link}")
#             return
#         city = CityInputSchema(name=vacancy_data.get("area").get("name"))
#         if not vacancy_data.get("company") or not vacancy_data.get("company").get(
#             "name"
#         ):
#             print(f"No company data found {link}")
#         company = CompanyInputSchema(name=vacancy_data.get("company").get("name"))
#         tools = []
#         if skills := vacancy_data.get("keySkills"):
#             tools = [
#                 ToolInputSchema(name=tool) for tool in skills.get("keySkill") or []
#             ]
#         if not vacancy_data.get("compensation"):
#             print(f"No compensation data found {link}")
#         salary_from = vacancy_data["compensation"].get("from")
#         salary_to = vacancy_data["compensation"].get("to")
#         if not any([salary_from, salary_to]):
#             print(f"No salary data found (from, to) {link}")
#             return
#         salary_from = (
#             salary_from * self.DOLLAR_TO_RUB
#             if vacancy_data["compensation"]["currencyCode"] != self.RUR_CODE
#             and salary_from
#             else salary_from
#         )
#         salary_to = (
#             salary_to * self.DOLLAR_TO_RUB
#             if vacancy_data["compensation"]["currencyCode"] != self.RUR_CODE
#             and salary_to
#             else salary_to
#         )
#         analyzer = Analyzer(
#             title=vacancy_data.get("name"),
#             description=vacancy_data.get("description"),
#             tools=vacancy_data.get("keySkills").get("keySkill") if tools else [],
#             experience=vacancy_data.get("workExperience"),
#         )
#         language = analyzer.get_language()
#         speciality = analyzer.get_speciality()
#         experience = analyzer.get_head_hunter_experience()
#         if not all(
#             [
#                 language,
#                 speciality,
#                 experience,
#             ]
#         ):
#             print(
#                 f"No vacancy data found ({language}, {speciality}, {experience}) {link}"
#             )
#             return
#         vacancy = VacancyInputSchema(
#             title=vacancy_data.get("name"),
#             description=vacancy_data.get("description"),
#             language=language,
#             speciality=speciality,
#             experience=experience,
#             salary_from=salary_from,
#             salary_to=salary_to,
#         )
#         vacancy_schema = VacancyCreateSchema(
#             city=city,
#             company=company,
#             vacancy=vacancy,
#             tool=tools,
#         )
#         return vacancy_schema
#
#     async def create_vacancy(self):
#         links = self.get_vacancies_links()
#         for link in tqdm(links):
#             vacancy_schema = self.get_vacancy_schema(link)
#             async with get_async_session() as session:
#                 vacancy_service = VacancyService(session=session)
#                 await vacancy_service.create(vacancy_schema)
