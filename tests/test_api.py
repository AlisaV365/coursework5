import pytest
from superjob.job_API import Vacancy

def test_vacancy_init():
    vacancy = Vacancy(id_vacancy=1, title="Python", url="https://e.com",
                      salary_from=1000, salary_to=3000, employer="ООО", api="ООО_api")

    assert vacancy.id_vacancy == 1
    assert vacancy.title == "Python"
    assert vacancy.url == "https://e.com"
    assert vacancy.salary_from == 1000
    assert vacancy.salary_to == 3000
    assert vacancy.employer == "ООО"
    assert vacancy.api == "ООО_api"
