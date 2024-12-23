import json, sys
from ete3 import Tree, TreeStyle, TextFace, NodeStyle


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

if not sys.argv[0]:
    printf("Не был задан файл для рендера! Укажите его после после скрипта")
    quit()
circle = False
if not sys.argv[1] == "true":
    printw("Не указан тип графика! Чтобы он был круглым укажите вторым параметром 'true'. Будет прямоугольным")
else:
    circle = True


def turn_to_graph(file_name, circle = False):
    printOK("Начинаю рендер графика!")

    image_name = file_name.split(".")[0]

    nested_dicts = {}

    with open("level_10_scan_test.txt", "r") as file:
        nested_dicts = json.loads(file.read())

    # print(nested_dicts)


    ts = TreeStyle()
    ts.show_branch_length = False
    ts.show_branch_support = False
    ts.show_leaf_name = False
    ts.show_scale = False
    if circle:
        ts.mode = "c"
    else:
        ts.mode = "r"

    tree = Tree(format=1)
    root_dic = list(nested_dicts.keys())[0]
    tree.name = nested_dicts[root_dic][0] + "\n" + root_dic

    root = tree

    def add_children(tree_node:Tree, dic:dict):
        for key in list(dic.keys()):
            node = tree_node.add_child(name=str(dic[key][0]) + "\n" +  key)
            add_children(node, dic[key][1])
    add_children(root, nested_dicts[root_dic][1])

    for n in tree.traverse():
        # if not n.is_leaf():
        #     n.add_face(TextFace(n.name, fsize=500), column=0)
        # print(n.name)

        if n.name == "":
            n.name = "\n"

        name, url = n.name.split("\n") 

        n.add_face(TextFace(name, fsize=15), column=0)
        n.add_face(TextFace(url, fsize=10), column=0)
        n.add_face(TextFace(" ", fsize=8), column=0)
    # print(tree)

    tree.render(f"{image_name}.png", tree_style=ts)

turn_to_graph(sys.argv[0], circle)