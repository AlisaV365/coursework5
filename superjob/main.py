from superjob.job_API import HeadHunterAPI, SuperJobAPI, VacancyFile

def main():
    vacancies_json = []
    keyword = input('Здраствуйте.\nВведите название вакансии: ')

    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)
    for api in (hh, sj):
        api.get_vacancies()
        vacancies_json.extend(api.get_formatted_vacancies())

    vacancies_file = VacancyFile(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            '1 - Вывести список вакансий;\n'
            '2 - Сортировать по зарплате. От наименьшего к наибольшему;\n'
            '3 - Сортировать по зарплате. От наибольшего к наименьшему;\n'
            '4 - Сортировать по максимальной зарплате;\n'
            'exit - Выход;\n'
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = vacancies_file.select()
        elif command == '2':
            vacancies = vacancies_file.sorted_vacancies_by_salary_from_asc()
        elif command == '3':
            vacancies = vacancies_file.sorted_vacancies_by_salary_from_desc()
        elif command == '4':
            vacancies = vacancies_file.sorted_vacancies_by_salary_to_asc()

        for vacancy in vacancies:
            print(vacancy, end='\n\n')

if __name__ == '__main__':
    main()
