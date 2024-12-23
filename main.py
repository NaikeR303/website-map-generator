import requests, time, concurrent.futures, random, json, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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



root_url = None
if not sys.argv[0].startswith("http"):
    printf("Дана неправильная ссылка! Для работы требуется любая ссылка формата https://exapmle.com")
    quit()
else:
    root_url = sys.argv[0]

depth = None
if not sys.argv[1].isnumeric():
    printf("Не дана глубина поиска! Она должна как миниму равняться 2\nЧем больше глубина, тем дольше поиск")
    quit()
else:
    depth = int(sys.argv[1])

do_render = False
if not sys.argv[2] == "true":
    printw("Не указано что нужно отрендерить график после завершения работы, поэтому результат будет выведен в result.txt\nДля рендера перезапустите програму со вторым аргументом как 'true'")
else:
    do_render = True

# root_url = "http://127.0.0.1:5000/Home"
# root_url = sys.argv[0]
print(f"Собираю карту сайта {root_url}. В зависимости от выбранного уровня глубины поиска это может занять от десятков минут, до часов. Пожалуйста, подождите...")

root_url = root_url.replace("www.", "")


gt_time = 60 * 5
global_timeout = False
added_urls = []

def get_url_info(url, attempts = 3, wait_min = 60, wait_max = 120):
    """Возвращает сначала заголовок страницы [0], а потом все найденные ссылки [1]. Если сайт недоступен, ничего не возвращает\n
    Делает по стандарту 3 попытки (attempts), если не получил ответ 200, ожидая от 30 (wait_min) до 60 (wait_max) секунд перед каждой попыткой. Разброс для того чтобы не было волной"""
    try:
        response = requests.get(url)
    except Exception as e:
        return [None, "Не получается связаться"]

    if url not in added_urls:
        added_urls.append(url)
    else:
        return [False, "Эта ссылка уже получена"]

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
                printw(f"Получил ошибку {bcolors.FAIL}429{bcolors.WARNING}, получая {url}. Слишком много запросов за минуту. Жду {gt_time} секунд перед продолжением...")
                
                #Ожидаю сколько-то секунд
                if global_timeout == False:
                    global_timeout = True
                    time.sleep(gt_time)
                    global_timeout = False
                else:
                    while global_timeout:
                        time.sleep()
            else:
                attempts -= 1
                if attempts <= 0:
                    printw(f"Получил ошибку {bcolors.FAIL + str(response.status_code) + bcolors.WARNING}, получая {url}...")
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
                    tree = {current_url: [info[0], {}]}

                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        subprocesses = [executor.submit(collect_urls, url, max_n, n + 1) for url in info[1]]

                        for process in concurrent.futures.as_completed(subprocesses):
                            url_tree = process.result()
                            if url_tree:
                                tree[current_url][1] = tree[current_url][1] | url_tree

                    return tree
                else:
                    if info[0] == False:
                        return []
                    else:
                        printw(f"Внимание! Вся дальнейшая ветвь для {current_url} потеряна! Код ошибки: {bcolors.FAIL + str(info[1])}")
                        printw(f"Рекомендуется перезапустить программу целиком, если это ошибка не была ожидана")
                        return {"Ошибка": [info[1], {}]}
            else:
                print(f"Домен URL {current_url} отличается от начального домена {root_url}. Пропускаю...")

            return []

dump = json.dumps(collect_urls(root_url, 10))
with open("result.txt", 'w') as file:
    file.write(dump)

printOK("Готово!")

if do_render:
    from turn_to_graph import turn_to_graph

    turn_to_graph("result.txt", False)