from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def checking_teg(teg):
    if teg is None:
        return 'не указана'
    else:
        return teg.text


def get_vacancy(*args):
    headers_gen = Headers(os='win', browser='chrome')
    args_str = ' '.join(list(args))
    params = {
        'area': [1, 2],
        'text': args_str,
        'items_on_page': '100'
    }
    response = requests.get('https://spb.hh.ru/search/vacancy',
                            headers=headers_gen.generate(), params=params)
    main_hh_html = response.text
    main_soup = BeautifulSoup(main_hh_html, 'lxml')
    vacancy_block = main_soup.find('main', class_='vacancy-serp-content')
    vacancy_tegs = vacancy_block.findAll('div', class_='serp-item')

    vacancy_list = []
    for vacancy in vacancy_tegs:
        link_teg = vacancy.find('a', class_='serp-item__title')
        salary_teg = vacancy.find('span', class_='bloko-header-section-2')
        company_teg = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
        city_teg = vacancy.findAll('div', class_='bloko-text')

        link = link_teg['href']
        salary_ = checking_teg(salary_teg).replace('\u202f', ' ')
        company = checking_teg(company_teg).replace('\xa0', ' ')
        city = checking_teg(city_teg[1]).split(',')[0]

        vacancy_dict = {'Ссылка': link,
                        'Зарплата': salary_,
                        'Компания': company,
                        'Город': city
                        }
        vacancy_list.append(vacancy_dict)
    pprint(vacancy_list)
    return vacancy_list


def get_vacancy_json(vacancy):
    with open('vacancy.json', 'w', encoding='UTF-8') as file:
        json.dump(vacancy, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':

    get_vacancy_json(get_vacancy('python', 'django', 'flask'))
