import requests, time, concurrent.futures, random, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin



root_url = "https://www.pikabu.ru"
# root_url = sys.argv[0]
print(f"Собираю карту сайта {root_url}. В зависимости от выбранного уровня глубины поиска это может занять от десятков минут, до часов. Пожалуйста, подождите...")

root_url = root_url.replace("www.", "")

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
def printOK(string):
    print(bcolors.OKGREEN + string + bcolors.ENDC)

# treeInUse = False
# url_tree = {}
added_urls = []

def get_url_info(url, attempts = 8, wait_min = 60, wait_max = 120):
    """Возвращает сначала заголовок страницы [0], а потом все найденные ссылки [1]. Если сайт недоступен, ничего не возвращает\n
    Делает по стандарту 8 попыток (attempts), если не получил ответ 200, ожидая от 30 (wait_min) до 6S0 (wait_max) секунд перед каждой попыткой. Разброс для того чтобы не было волной"""
    try:
        response = requests.get(url)
    except Exception as e:
        return [None, "Не получается связаться"]

    #Делаю повторные попытки, на тот случай, если ошибка 503 или подобная
    while attempts > 0:
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
            printOK(f"Успешно получил {url}")
            return [title, urls]
        else:
            #Чтобы избежать ограничений по количеству
            if response.status_code == 429:
                printw(f"Получил ошибку 429, получая {url}. Слишком много запросов за минуту. Жду 5 минут перед продолжением...")
                time.sleep(60 * 5)
            if response.status_code == 503:
                printw(f"Получил ошибку 503, получая {url}. Жду...")
            else:
                attempts -= 1
            time.sleep(random.randint(wait_min, wait_max))

    return [None, response.status_code]

def collect_urls(current_url, max_n = 4, n = 0, max_workers = 20, other_domains = False):
    """Собирает карту всех ссылок досупных с корневой ссылки (current_url) вызывая самого себя рекурсивно\n
    Стандартная глубина поиска (max_n) - 4, шаг (n) не трогать, он всегда 0, если ссылка корневая\n
    Количество одновременно работающих потоков (max_workers) - 20\n
    Поиск по стандарту осуществляется только для сайтов с тем же доменом, что и корневой. Для отключения этого нужно поставить other_domains на True
    """
    match n:
        #Если корневая ссылка
        case 0:
            info = get_url_info(current_url)

            if info[0]:
                if current_url not in added_urls:
                    added_urls.append(current_url)

                    tree = {current_url: [info[0], {}]}

                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        subprocesses = [executor.submit(collect_urls, url, max_n, n + 1) for url in info[1]]

                        for process in concurrent.futures.as_completed(subprocesses):
                            url_tree = process.result()
                            if url_tree:
                                tree[current_url][1] = tree[current_url][1] | url_tree
                    return tree
            else:
                printw(f"Не получилось собрать информацию с адреса {current_url} Код ошибки: {bcolors.FAIL + str(info[1])}")
                printf("Невозможно продолжить выполнение программы. Выхожу...")
                time.sleep(4)
                quit()

        case _ if n == max_n:
            # return {"...": ["...", {}]}
            return []

        case _:
            #Проверяю ссылка ли это вообще
            try:
                str(current_url).split("/")[2]
            except:
                return []
            
            #Если домен не отличается от данного в начале
            if str(current_url).split("/")[2] == str(root_url).split("/")[2] or other_domains:
                info = get_url_info(current_url)

                if info[0]:
                        if current_url not in added_urls:
                            added_urls.append(current_url)

                            tree = {current_url: [info[0], {}]}

                            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                                subprocesses = [executor.submit(collect_urls, url, max_n, n + 1) for url in info[1]]

                                for process in concurrent.futures.as_completed(subprocesses):
                                    url_tree = process.result()
                                    if url_tree:
                                        tree[current_url][1] = tree[current_url][1] | url_tree

                            return tree
                else:
                    printw(f"Внимание! Вся дальнейшая ветвь для {current_url} потеряна! Код ошибки: {bcolors.FAIL + str(info[1])}")
                    printw(f"Рекомендуется перезапустить программу целиком, если это ошибка не была ожидана")
                    return {"Ошибка": [info[1], {}]}
            else:
                print(f"Домен URL {current_url} отличается от начального домена {root_url}. Пропускаю...")

            return []

with open("gg.txt", 'w') as file:
    file.write(str(collect_urls(root_url, 3)))