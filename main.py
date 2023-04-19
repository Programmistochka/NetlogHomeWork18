import os
import datetime
import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import pprint

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return Headers(browser = "firefox", os = "win").generate()

def get_text(url):
    params={'text': 'python', 'area' : 2, 'per_page':20}
    #return requests.get('https://spb.hh.ru/search/vacancy', headers = get_headers(), params=params).text
    return requests.get(url, headers = get_headers(), params = params).text

if __name__ == "__main__":
    #Получение текста html страницы
    all_text=get_text(HOST)
    soup = BeautifulSoup(all_text, features ='lxml')
    all_finded_vacancy = []

    #Определение общего количества страниц по результатам запроса
    all_pages = int(soup.find('div', attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    print(f'По запросу найдено {all_pages}стр.')
    
    #Обработка каждой страницы
    for page in range(0, all_pages):
        page_HOST = HOST + "&page=" + str(page)
        html_text=get_text(page_HOST)
        soup_page = BeautifulSoup(html_text, features ='lxml')

        #Получение блока с информацией по всем найденным на странице вакансиям
        vacancy_bloks = soup_page.find_all('div', class_ = 'serp-item')

        #Определение параметров каждой найденной вакансии
        for vacancy in vacancy_bloks:
            title = vacancy.find(class_ = 'serp-item__title').text
            link =  vacancy.find(class_ = 'serp-item__title')['href']
            company = vacancy.find(class_='vacancy-serp-item__meta-info-company').text
            city = vacancy.find(class_='vacancy-serp-item__info').contents[1].text
            zp = vacancy.find(class_='vacancy-serp-item-body__main-info').find('span', class_='bloko-header-section-3')
            if zp is None:
                zp = "Зарплата не указана"
            else:
                zp = ('').join(zp.contents)
                zp = zp.replace('\u202f','')

            #Для просмотра полного описания вакансии необходимо пройти по ссылке
            vacancy_html=get_text(link)
            soup_vacancy = BeautifulSoup(vacancy_html, features ='lxml')
            whole_description = soup_vacancy.find('div', class_={'vacancy-section'}).text

            #Отбор только тех вакансий, у которых в описании есть слова "Django и Flask"
            rez_search_django = re.findall('Django', whole_description, flags=re.I)
            rez_search_flask = re.findall('Flask', whole_description, flags=re.I)
            if rez_search_django != [] and rez_search_flask != []: 
                #Добавление информации по обработанной вакансии в результирующий словарь
                all_finded_vacancy.append({
                    'title' :  title,
                    'link' : link,
                    'company' : company,
                    'city' : city,
                    'zp' : zp
                    #'description': whole_description
                })
    print('-------------------------------')
    print(f'Всего получено вакансий, содержащих слова Django и Flask в описании: {len(all_finded_vacancy)}')

    #Запись в файл json результата: информации о каждой вакансии - название, ссылка, вилка зп, название компании, город
    current_path = os.getcwd() 
    folder_name = 'reports'
    time_creation = str(datetime.datetime.now())
    time_creation = time_creation[0:10].replace('-','') + '_' + time_creation[11:19].replace(':','-') 
    file_name = 'report_' + time_creation + '.json'
    full_path = os.path.join(current_path, folder_name, file_name)
    with open(full_path, 'a') as file:
        json.dump(all_finded_vacancy, file, ensure_ascii = False) 
            
    print(f'Результаты можно посмотреть в файле: {file_name} в каталоге reports')