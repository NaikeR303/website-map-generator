import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


max_n = 10
rootURL = "https://pikabu.ru"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printw(string):
    print(bcolors.WARNING + string + bcolors.ENDC)
def printf(string):
    print(bcolors.FAIL + string + bcolors.ENDC)

treeInUse = False
urlTree = {}
addedURLs = []

def get_url_info(url):
    """Возвращает сначала заголовок страницы [0], а потом все найденные ссылки [1]. Если сайт недоступен, ничего не возвращает"""
    response = requests.get(url)

    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'html.parser')
        title = html.find('title')

        urls = html.find_all('a', href=True)
        #Достаю все URL из <a>
        urls = [urljoin(url, u['href']) for u in urls]
        #Убираю www. для однообразия
        urls = list(map(lambda url: url.replace("www.", ""), urls))
        #Убираю запросы 
        urls = list(filter(lambda url: "?" not in str(url), urls))

        urls = sorted(set(urls))
        return [title, urls]
    else:
        return [None, response.status_code]

def collect_urls(currentUrl, max_n = 4, n = 0):
    match n:
        #Если корневая ссылка
        case 0:
            info = get_url_info(currentUrl)

            if info[0]:
                urlTree[currentUrl] = [info[0], {}]
                #Повторяю для каждой дочерней ссылки
                for url in info[1]:
                    collect_urls(url, max_n, n + 1)
            else:
                printw(f"Не получилось собрать информацию с адреса {currentUrl} Код ошибки: {bcolors.FAIL + str(info[1])}")
                printf("Невозможно продолжить выполнение программы. Выхожу...")
                quit()

        case _ if n == max_n:
            while True:
                if not treeInUse:
                    treeInUse = True

                    urlTree[currentUrl][1]["...", {}]

                    treeInUse = False
                    break

        case _:
            info = get_url_info(currentUrl)

            if info[0]:
                #Если домен не отличается от данного в начале
                if str(currentUrl).startswith(rootURL):

                    while True:
                        if not treeInUse:
                            treeInUse = True

                            if currentUrl not in addedURLs:
                                addedURLs.append(currentUrl)
                                urlTree[currentUrl] = [info[0], {}]
                                #Повторяю для каждой дочерней ссылки
                                for url in info[1]:
                                    collect_urls(url, max_n, n + 1)
                            else:
                                print(f"URL {currentUrl} уже присутсвует в графе. Пропускаю...")
                                
                            treeInUse = False
                            break
                else:
                    print(f"Домен URL {currentUrl} отличается от начального домена {rootURL}. Пропускаю...")
            else:
                printw(f"Внимание! Вся дальнейшая ветвь для {currentUrl} потеряна! Код ошибки: {bcolors.FAIL + str(info[1])}")
                printw(f"Рекомендуется перезапустить программу целиком")


#     try:
#         response = requests.get(currentUrl)

#         if response.status_code == 200:
#             html = BeautifulSoup(response.content, 'html.parser')
#             urls = html.find_all('a', href=True)
#             #Достаю все URL из <a>
#             urls = [urljoin(currentUrl, url['href']) for url in urls]
#             #Убираю www. для однообразия
#             urls = list(map(lambda url: url.replace("www.", ""), urls))
#             #Убираю запросы 
#             urls = list(filter(lambda url: "?" not in str(url), urls))

#             urls = sorted(set(urls))
#             return urls
#         else:
#             printw(f"Не получилось собрать ссылки с адреса {currentUrl}. Код ошибки: {bcolors.FAIL}{response.status_code}")
#             return []
#     except KeyboardInterrupt as e:
#         printw(f"Не получилось собрать ссылки с адреса {currentUrl}. Вероятно такого адреса нет, либо он недоступен. Ошибка:")
#         print(e)


# website_url = 'https://reddit.com/'  
# links = get_all_child_urls(website_url, 10)

# for link in links:
#     print(link)
