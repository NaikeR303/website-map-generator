from flask import Flask, render_template_string, request, redirect
import random, json


def generate_random_dicts(min_parents=1, max_parents=20, m_depth=4, child_node_chance=0.05):
    def generate_nested_dicts(parent_name, max_depth, curr_depth=0, child_node_chance = 0.05):
        """
        Рекурсивно генерирует вложенные словари с каким-то шансом добавления дочерних словарей.
        """
        if curr_depth >= max_depth:
            return {}

        children = {}
        for child_name in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if random.random() <= child_node_chance:
                child_full_name = parent_name + child_name
                children[child_full_name] = generate_nested_dicts(child_full_name, max_depth, curr_depth + 1, child_node_chance=child_node_chance)

        return children

    # Генерация от 1 до 20 начальных родительских словарей
    num_parents = random.randint(min_parents, max_parents)
    nested_dicts = {}

    for i in range(num_parents):
        parent_name = chr(65 + i)  # Генерация имён A, B, C и т.д. (используя ASCII)
        nested_dicts[parent_name] = generate_nested_dicts(parent_name, max_depth=m_depth, child_node_chance=child_node_chance)

    return {"Home": nested_dicts}


# with open("txt.txt", "w") as file:
#     file.write(json.dumps(generate_random_dicts()))



all_paths = generate_random_dicts()
print(all_paths)


app = Flask(__name__)

# Главная страница
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    path_split = path.split("/")

    def find_nested(all_paths, path_split):
        for key in path_split:
            if key in all_paths:
                all_paths = all_paths[key]
            else:
                return None
            
        return all_paths

    children = find_nested(all_paths, path_split)

    if children != None:
        path = path.replace("/Home/Home", "/Home")
        return render_template_string(f"""
            <head><title>Каталог {path_split[-1]}</title></head>
            <h1>Каталог {path_split[-1]}</h1>

            <p>Подкаталоги {path_split[-1]}</p>        
            """ + 
            "".join(list(map(lambda x: f'<li><a href="/{path}/{x}">Каталог {x}</a></li>\n', children))) + 
            '<p></p><li><a href="/Home">Обратно</a></li>')
    else:
        return redirect("/Home")
        # return "nope"


if __name__ == '__main__':
    app.run(debug=True)
