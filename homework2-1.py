import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from pprint import pprint

main_url = 'https://hh.ru'
page_param = 0
all_vacancies = []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.67 Safari/537.36'}
for i in range(0, 9):

    params = {'text': 'Data science', 'from': 'suggest_post', 'fromSearchLine': 'true', 'area': 1, 'page': page_param,
              'hhtmFrom': 'vacancy_search_list'}

    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)

    soup = bs(response.text, 'html.parser')

    vacancies_compensations = soup.find_all('div', {'class': 'vacancy-serp-item'})

    print(len(vacancies_compensations))
    pprint(vacancies_compensations)

    for vacancy in vacancies_compensations:
        vacancy_info = {}
        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        vacancy_link = vacancy.find_all('a')[0]['href']
        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary == None:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            salary_split = salary.split()
            if len(salary_split) == 6:
                salary_min = int(salary_split[0] + salary_split[1])
                salary_max = int(salary_split[3] + salary_split[4])
                currency = salary_split[5]
            elif len(salary_split) == 4:
                if salary_split[0] == 'от':
                    salary_min = int(salary_split[1] + salary_split[2])
                    salary_max = None
                    currency = salary_split[3]
                else:
                    salary_min = None
                    salary_max = int(salary_split[1] + salary_split[2])
                    currency = salary_split[3]

        vacancy_info['name'] = vacancy_name
        vacancy_info['link'] = vacancy_link
        vacancy_info['min_salary'] = salary_min
        vacancy_info['max_salary'] = salary_max
        vacancy_info['currency'] = currency
        all_vacancies.append(vacancy_info)

    page_param = page_param + 1


df = pd.DataFrame(all_vacancies)
df.to_csv('vac.csv', header=False)
