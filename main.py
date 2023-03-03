import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import pprint

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return Headers(browser = "firefox", os = "win").generate()

def get_text(url):
    return requests.get(url, headers = get_headers(), params={'count' : 50}).text


if __name__ == "__main__":
    get_text(HOST)
all_finded_vacancy = []

all_pages = range(2)
for page in all_pages:
    page_HOST = HOST + "&page=" + str(page) + "&items_on_page=50"
    print('***********'+str(page)+'**************')
    html_text=get_text(page_HOST)
    soup = BeautifulSoup(html_text, features ='lxml')

    # pages = soup.find('a', {'data-qa': 'pager-next'})
    # print(pages)
    # pages = soup.find('a', {'class': 'pager'})
    # print(pages)
    # q_pages = soup.find('div', class_ = 'pager').get_text()
    # print(q_pages)

    vacancy_bloks = soup.find_all('div', class_ = 'serp-item')
    
    print(len(vacancy_bloks))

   

    for vacancy in vacancy_bloks:
        print('-----')
        #print(vacancy)
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
        print(zp)
        description = vacancy.find('div', class_="g-user-content").text

        all_finded_vacancy.append({
            'title' :  title,
            'link' : link,
            'company' : company,
            'city' : city,
            'zp' : zp,
            'description' : description
        })
print(all_finded_vacancy)
print(len(all_finded_vacancy))
    
    #### Убрать символы ASCII  в зарплатах и дру полях вакансии, возможно необходимо взять полное описание вакансии
    #а не краткое описание на главной страницы выборки

    ### Как вычислить количество страниц и изменить количество вакансий выдаваемых в запросе

    

