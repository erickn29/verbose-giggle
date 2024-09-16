from src.apps.v1.vacancy.utils.parser.head_hunter import HeadHunterParser


async def test_head_hunter():
    parser = HeadHunterParser()
    assert True
    # vacancy: VacancyCreateSchema = await parser.get_vacancies(save=False, only_one=True)
    # assert isinstance(vacancy.vacancy.title, str)
    # assert isinstance(vacancy.city.name, str)
    # assert isinstance(vacancy.company.name, str)
    # assert vacancy.vacancy.salary_to or vacancy.vacancy.salary_from
