# Курсовой проект по ООП “Парсер вакансий”

## ## Задание

Напишите программу, которая будет получать информацию о вакансиях с разных платформ в России, сохранять ее в файл и 
позволять удобно работать с ней (добавлять, фильтровать, удалять).

## Требования к реализации

1. Создать абстрактный класс для работы с API сайтов с вакансиями. Реализовать классы, наследующиеся от абстрактного 
   класса, для работы с конкретными платформами. Классы должны уметь подключаться к API и получать вакансии.
2. Создать класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты, такие как название вакансии,
   ссылка на вакансию, зарплата, краткое описание или требования и т.п. (не менее четырех) Класс должен поддерживать 
   методы сравнения вакансий между собой по зарплате и валидировать данные, которыми инициализируются его атрибуты.
3. Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл, получения данных 
   из файла по указанным критериям и удаления информации о вакансиях. Создать класс для сохранения информации о 
   вакансиях в JSON-файл. Дополнительно, по желанию, можно реализовать классы для работы с другими форматами, например 
   с CSV- или Excel-файлом, с TXT-файлом.
4. Создать функцию для взаимодействия с пользователем. Функция должна взаимодействовать с пользователем через консоль. 
   Самостоятельно придумать сценарии и возможности взаимодействия с пользователем. Например, позволять пользователю 
   указать, с каких платформ он хочет получить вакансии, ввести поисковый запрос, получить топ N вакансий по зарплате, 
   получить вакансии в отсортированном виде, получить вакансии, в описании которых есть определенные ключевые слова, 
   например "postgres" и т.п.
5. Объединить все классы и функции в единую программу.

## Требования к реализации в парадигме ООП

1. Абстрактный класс и классы для работы с API сайтов с вакансиями должны быть реализованы в соответствии с принципом 
   наследования.
2. Класс для работы с вакансиями должен быть реализован в соответствии с принципом инкапсуляции и поддерживать методы 
   сравнения вакансий между собой по зарплате.
3. Классы и другие сущности в проекте должны удовлетворять минимум первым двум требованиям принципов SOLID.

-   Данный проект предствляет из себя программу (парсинг), которая получает список вакансий с сайтов SuperJob и HeadHunter в соответствии с введенным пользователем ключевым словом, а затем обрабатывает и сортирует список вакансий. Программа предлагает пользователю отсортировать список вакансий в соответствии с зарплатой, а также предоставляет возможность вывести список вакансий.
main.py:
1. Импортируются классы HeadHunterAPI, SuperJobAPI и VacancyFile из модуля superjob.job_API.
2. Определяется функция main(), которая запрашивает у пользователя название вакансии, инициализирует классы HeadHunterAPI и SuperJobAPI с ключевым словом введенным пользователем, извлекает список вакансий с каждого API, форматирует списки вакансий, объединяет их в один список, а затем создает объект VacancyFile и записывает список вакансий в файл.
3. Затем программа предлагает пользователю отсортировать список вакансий по зарплате и выводит список вакансий в соответствии с выбранной сортировкой.

job_API.py:
1. Импортируются модули requests, json, os, абстрактный класс ABC и метод load_dotenv из модуля dotenv.
2. Определяется класс ParsingError для обработки ошибок в методах парсинга.
3. Определяется класс Vacancy, который хранит информацию о вакансии и поддерживает методы сравнения, получения ссылки на вакансию и преобразования в строку.
4. Определяется абстрактный класс AbstractAPI с абстрактным методом get_vacancies.
5. Объявляются фильтрующие слова filter_words.
6. Определяется класс HeadHunterAPI, который реализует механизм получения списка вакансий с HeadHunter.
7. Класс HeadHunterAPI содержит приватные атрибуты header и params для запросов к API, а также публичный метод get_vacancies, который запрашивает список вакансий с API HeadHunter и фильтрует данные в соответствии с фильтрующими словами.
8. Определяется класс SuperJobAPI, который реализует механизм получения списка вакансий с SuperJob.
9. Класс SuperJobAPI содержит приватные атрибуты header и params для запросов к API, а также публичный метод get_vacancies, который запрашивает список вакансий с API SuperJob и фильтрует данные в соответствии с фильтрующими словами.
10. Определяется класс VacancyFile, который реализует механизм записи списка вакансий в файл и чтения списка вакансий из файла.