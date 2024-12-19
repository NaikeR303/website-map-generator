import requests, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


rootURL = "https://cyberleninka.ru"

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

# treeInUse = False
# urlTree = {}
addedURLs = []

def get_url_info(url):
    """Возвращает сначала заголовок страницы [0], а потом все найденные ссылки [1]. Если сайт недоступен, ничего не возвращает"""
    response = requests.get(url)

    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'html.parser')
        try: 
            title = html.find('title').get_text()
        except:
            title = "None"

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
                if currentUrl not in addedURLs:
                    addedURLs.append(currentUrl)

                    tree = {currentUrl: [info[0], {}]}

                    for url in info[1]:
                        urlTree = collect_urls(url, max_n, n + 1)
                        if urlTree:
                            tree[currentUrl][1] = tree[currentUrl][1] | urlTree

                    return tree
            else:
                printw(f"Не получилось собрать информацию с адреса {currentUrl} Код ошибки: {bcolors.FAIL + str(info[1])}")
                printf("Невозможно продолжить выполнение программы. Выхожу...")
                time.sleep(4)
                quit()

        case _ if n == max_n:
            # return {"...": ["...", {}]}
            return []

        case _:
            #Если домен не отличается от данного в начале
            #Ещё убираю 'javascript:void(0)' т.к. это ссылка на скрипт
            if currentUrl != "javascript:void(0)" or str(currentUrl).split("/")[2] == str(rootURL).split("/")[2]:
                info = get_url_info(currentUrl)

                if info[0]:
                        if currentUrl not in addedURLs:
                            addedURLs.append(currentUrl)

                            tree = {currentUrl: [info[0], {}]}

                            for url in info[1]:
                                urlTree = collect_urls(url, max_n, n + 1)
                                if urlTree:
                                    tree[currentUrl][1] = tree[currentUrl][1] | urlTree

                            return tree
                else:
                    printw(f"Внимание! Вся дальнейшая ветвь для {currentUrl} потеряна! Код ошибки: {bcolors.FAIL + str(info[1])}")
                    printw(f"Рекомендуется перезапустить программу целиком")
                    return {"Ошибка": [info[1], {}]}
            else:
                print(f"Домен URL {currentUrl} отличается от начального домена {rootURL}. Пропускаю...")

            return []

print(collect_urls(rootURL, 2))


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
