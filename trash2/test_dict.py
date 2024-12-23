import random
from ete3 import Tree, TreeStyle, TextFace, NodeStyle

def generate_nested_dicts(parent_name, max_depth, current_depth=0):
    """
    Рекурсивно генерирует вложенные словари с 5% шансом добавления дочерних словарей.

    :param parent_name: Имя текущего словаря.
    :param max_depth: Максимальная глубина вложенности.
    :param current_depth: Текущая глубина рекурсии.
    :return: Сгенерированный словарь.
    """
    if current_depth >= max_depth:
        return {}

    children = {}
    for child_name in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if random.random() <= 0.05:  # 5% шанс на создание дочернего словаря
            child_full_name = parent_name + child_name
            children[child_full_name] = generate_nested_dicts(
                child_full_name, max_depth, current_depth + 1
            )

    return children




# Генерация от 1 до 20 начальных родительских словарей
num_parents = random.randint(1, 20)
nested_dicts = {}

for i in range(num_parents):
    parent_name = chr(65 + i)  # Генерация имён A, B, C, ...
    nested_dicts[parent_name] = generate_nested_dicts(parent_name, max_depth=5)


nested_dicts2 = nested_dicts
nested_dicts = {}
nested_dicts["home"] = nested_dicts2


# Для проверки структуры
import pprint
pprint.pprint(nested_dicts)



ts = TreeStyle()
ts.show_branch_length = False  # Disable branch length display
ts.show_branch_support = False  # Disable branch support display (if any)
ts.show_leaf_name = False
ts.show_scale = False
ts.mode = "c"  # for rectangular layout

tree = Tree(format=1)
tree.name = list(nested_dicts.keys())[0]

root = tree

def add_children(tree_node:Tree, dic:dict):
    for key in list(dic.keys()):
        node = tree_node.add_child(name=key)
        add_children(node, dic[key])
add_children(root, nested_dicts[list(nested_dicts.keys())[0]])

for n in tree.traverse():
    # if not n.is_leaf():
    #     n.add_face(TextFace(n.name, fsize=500), column=0)
    n.add_face(TextFace(n.name, fsize=500), column=0)
print(tree)

tree.render("render.png", tree_style=ts, w=4000, h=4000)