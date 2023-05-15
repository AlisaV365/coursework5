import requests
import json
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

# объединяем списки вакансий и фильтруем
all_vacancies = []
filtered_vacancies = []


class ParsingError(Exception):
    def __str__(self):
        return 'Ошибка получения данных по API'


class Vacancy:
    def __init__(self, id_vacancy, title, url, salary_from, salary_to, employer, api):
        self.id_vacancy = id_vacancy
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer = employer
        self.api = api

    def __eq__(self, other):
        return (self.salary_from, self.salary_to) == (other.salary_from, other.salary_to)

    def __lt__(self, other):
        if not other.salary_from:
            return False
        if not self.salary_from:
            return True
        return self.salary_from < other.salary_from

    def __repr__(self):
        return f"<Vacancy id={self.id_vacancy} title={self.title} salary_from={self.salary_from} salary_to={self.salary_to} employer={self.employer} api={self.api}>"

    def get_link(self):
        return self.url

    def __str__(self):
        return f"{self.title}\nSalary: from {self.salary_from} to {self.salary_to},\nEmployer: {self.employer},\nAPI: {self.api}\nURL: {self.get_link()}"



class AbstractAPI(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @staticmethod
    def _get_request(url, header, __params):
        """Метод для выполнения запросов к API"""
        response = requests.get(url, headers=header, params=__params)
        response.raise_for_status()  # Если ответ не 200, вызовется исключение
        return response.json()


# фильтрующие слова
filter_words = []


class HeadHunterAPI(AbstractAPI):

    def __init__(self, keyword):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        self.__params = {
            "keyword": keyword,
            "page": 0,
            "per_page": 100,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        ''' Изменение зарплат в случае изпользования евро'''
        formatted_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            formatted_salary[0] = salary['from'] if salary['currency'].lower() == 'rur' else salary['from']*80
        if salary and salary['to'] and salary['to'] != 0:
            formatted_salary[1] = salary['to'] if salary['currency'].lower() == 'rur' else salary['to']*80
        return formatted_salary

    def get_request(self):
        ''' Создание запроса по API'''
        response = requests.get('https://api.hh.ru/vacancies',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_vacancies(self, pages_count=1):
        ''' Перебор вакансий в цикле согласно количеству переопределенных в main страниц'''
        while self.__params['page'] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных')
                break
            print(f'Найдено ({len(values)}) вакансий.')
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_formatted_vacancies(self):
        '''Извлечение из вакансии необходимых полей '''
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter',
            })
        return formatted_vacancies


class SuperJobAPI(AbstractAPI):

    def __init__(self, keyword):
        self.__header = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        self.__params = {
            "keyword": keyword,
            "page": 0,
            "per_page": 100,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary, currency):
        formatted_salary = None
        if salary and salary != 0:
            formatted_salary = salary if currency == 'rub' else salary * 80
        return formatted_salary

    def get_request(self):
        '''Формирование запроса вакансий через API'''
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['objects']

    def get_vacancies(self, pages_count=1):
        ''' Перебор вакансий в цикле согласно количеству переопределенных в main страниц'''
        while self.__params['page'] < pages_count:
            print(f"SuperJob, Парсинг страницы {self.__params['page'] + 1}", end=":")
            try:
                values = self.get_request()
            except ParsingError:
                print(' Ошибка получения данных')
                break
            print(f' Найдено ({len(values)}) вакансий.')
            self.__vacancies.extend(values)
            self.__params['page'] += 1



    def get_formatted_vacancies(self):
        '''Приведение запроса в удобный вид'''
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': self.get_salary(vacancy['payment_from'], vacancy['currency']),
                'salary_to': self.get_salary(vacancy['payment_to'], vacancy['currency']),
                'employer': vacancy['firm_name'],
                'api': 'Superjob'
            })
        return formatted_vacancies


# Определяем абстрактный класс для работы с файлом вакансий
class AbstractVacancyFile:
    """Абстрактный класс для записи вакансий в файл JSON"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_vacancies(self, vacancies):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(vacancies, indent=4, ensure_ascii=False))



class VacancyFile:
    '''Создание класса для работы с json файлом с вакансиями'''

    def __init__(self, keyword, vacancies_json):
        self.__filename = f'{keyword.title()}.json'
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        ''' Внесение данных о вакансиях в json файл '''
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):
        ''' Извлечение из json файла данных о вакансии с заданными параметрами '''
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        vacancies = [Vacancy(x['id'], x['title'], x['url'], x['salary_from'], x['salary_to'], x['employer'], x['api'])
                     for x in data]
        return vacancies

    def sorted_vacancies_by_salary_from_asc(self):
        ''' Сортировка вакансий по минимальным зарплатам по возрастающей'''
        vacancies = self.select()
        vacancies = sorted(vacancies)
        return vacancies

    def sorted_vacancies_by_salary_from_desc(self):
        ''' Сортировка вакансий по минимальным зарплатам по убывающей'''
        vacancies = self.select()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies

    def sorted_vacancies_by_salary_to_asc(self):
        ''' Сортировка по максимальным заррплатам'''
        vacancies = self.select()
        vacancies = sorted(vacancies, key=lambda x: x.salary_to if x.salary_to else 0)
        return vacancies
