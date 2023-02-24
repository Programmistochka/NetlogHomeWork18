import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return Headers(browser = "firefox", os = "win").generate()

def get_text(url):
    return requests.get(url, headers = get_headers()).text


if __name__ == "__main__":
    get_text(HOST)

    html_text=get_text(HOST)
    soup = BeautifulSoup(html_text, features ='lxml')

    vacancy_bloks = soup.find('div', class_ = 'vacancy-serp-content').find_all('div', class_ = 'serp-item')
    
    print(len(vacancy_bloks))

    for vacancy in vacancy_bloks:
        print('-----')
        print(vacancy)
        print('-----')
        title = vacancy.find(class_ = 'serp-item__title').text
        print(title)
        link =  vacancy.find(class_ = 'serp-item__title')['href']
        print(link)
        company = vacancy.find(class_='vacancy-serp-item__meta-info-company').text
        print(company)
        zp = vacancy.find(class_='vacancy-serp-item-body__main-info').find('span', class_='bloko-header-section-3')
        if zp is None:
            zp = "Зарплата не указана"
        else:
            zp = (' ').join(zp.contents)
        print(zp)

