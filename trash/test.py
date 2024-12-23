import networkx as nx
import matplotlib.pyplot as plt

# Пример данных с глубокой вложенностью
# data = {
#     "g": ["g", {
#         "n": ["n", {
#             "u": ["u", {
#                 "v": ["v", {
#                     "w": ["w", {}]
#                 }]
#             }]
#         }],
#         "x": ["x", {
#             "y": ["y", {
#                 "z": ["z", {}]
#             }]
#         }]
#     }]
# }
with open("gg.txt", 'r') as  file:
    data = file.read()
# Функция для обхода структуры и создания графа
def add_edges(graph, parent, structure):
    if isinstance(structure, dict):
        for key, value in structure.items():
            graph.add_edge(parent, key)  # Добавляем ребро между родителем и текущим узлом
            add_edges(graph, key, value[1])  # Рекурсивно добавляем связи для вложенных данных
    elif isinstance(structure, list):
        for item in structure:
            add_edges(graph, parent, item[1])

# Создаем пустой граф
G = nx.DiGraph()

# Добавляем узлы и связи из данных
add_edges(G, "https://www.reddit.com", data["https://www.reddit.com"][1])

# Определяем цвета для узлов, где узел 'y' будет зелёным
node_colors = ['green' if node == 'y' else 'lightblue' for node in G.nodes]

# Автоматически регулируем размер изображения в зависимости от числа узлов
num_nodes = len(G.nodes)
figsize = (max(8, num_nodes / 2), max(6, num_nodes / 3))  # Устанавливаем размер, зависимый от количества узлов

# Используем spring_layout для упорядоченного расположения узлов
pos = nx.spring_layout(G, seed=42, k=0.5)  # 'k' контролирует плотность расположения

# Визуализируем граф с упорядоченными узлами
plt.figure(figsize=figsize)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=12, font_weight='bold', arrows=True)

# Сохраняем граф в файл (например, в формате PNG)
plt.savefig("dynamic_size_graph4.png", format="PNG", dpi=100)

# Показываем граф (если нужно)
plt.show()


# g = {"g": 12}
# b = {"b": 13}

# print(g | b)