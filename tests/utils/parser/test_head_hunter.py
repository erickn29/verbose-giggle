from utils.parser.head_hunter import HeadHunterParser
from v1.vacancy.schema.schema import VacancyCreateSchema


async def test_head_hunter():
    parser = HeadHunterParser()
    vacancy = await parser.get_vacancies(save=False, only_one=True)
    assert isinstance(vacancy, VacancyCreateSchema)
    assert isinstance(vacancy.vacancy.title, str)
    assert isinstance(vacancy.city.name, str)
    assert isinstance(vacancy.company.name, str)
    assert vacancy.vacancy.salary_to or vacancy.vacancy.salary_from
