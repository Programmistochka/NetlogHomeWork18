import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
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
    for page in range(0, 5):
        page_HOST = HOST + "&page=" + str(page)
        html_text=get_text(page_HOST)
        soup_page = BeautifulSoup(html_text, features ='lxml')

        #Получение блока с информацией по всем найденным на странице вакансиям
        vacancy_bloks = soup_page.find_all('div', class_ = 'serp-item')

        #Определение параметров каждой найденной вакансии
        for vacancy in vacancy_bloks:
            print('-----')
            title = vacancy.find(class_ = 'serp-item__title').text
            print(title)
            link =  vacancy.find(class_ = 'serp-item__title')['href']
            print(link)
            company = vacancy.find(class_='vacancy-serp-item__meta-info-company').text
            print(company)
            city = vacancy.find(class_='vacancy-serp-item__info').contents[1].text
            print(city)
            zp = vacancy.find(class_='vacancy-serp-item-body__main-info').find('span', class_='bloko-header-section-3')
            if zp is None:
                zp = "Зарплата не указана"
            else:
                zp = ('').join(zp.contents)
                zp = zp.replace('\u202f','')
            print(zp)
            description = vacancy.find('div', class_="g-user-content")#.text
            if description is None:
                description = "Описания нет"
            else:
                description = vacancy.find('div', class_="g-user-content").text
            
            #Добавление информации по обработанной вакансии в результирующий словарь
            all_finded_vacancy.append({
                'title' :  title,
                'link' : link,
                'company' : company,
                'city' : city,
                'zp' : zp,
                'description' : description
            })
    print('-------------------------------')
    print(f'Всего обработано {len(all_finded_vacancy)} вакансий'
    )
    
    #### Убрать символы ASCII  в зарплатах и дру полях вакансии, возможно необходимо взять полное описание вакансии
    #а не краткое описание на главной страницы выборки

    

    

