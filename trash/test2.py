from flask import Flask, render_template_string

app = Flask(__name__)

# Главная страница
@app.route('/')
def home():
    return render_template_string('''
        <h1>Главная страница</h1>
        <ul>
            <li><a href="/section1">Раздел 1</a></li>
            <li><a href="/section2">Раздел 2</a></li>
            <li><a href="/section3">Раздел 3</a></li>
        </ul>
    ''')

# Раздел 1
@app.route('/section1')
def section1():
    return render_template_string('''
        <h1>Раздел 1</h1>
        <ul>
            <li><a href="/section1/subsection1">Подраздел 1.1</a></li>
            <li><a href="/section1/subsection2">Подраздел 1.2</a></li>
            <li><a href="/">Назад на главную</a></li>
        </ul>
    ''')

# Подраздел 1.1
@app.route('/section1/subsection1')
def subsection1():
    return render_template_string('''
        <h1>Подраздел 1.1</h1>
        <p>Это подробности раздела 1.1.</p>
        <a href="/section1">Назад к разделу 1</a>
    ''')

# Подраздел 1.2
@app.route('/section1/subsection2')
def subsection2():
    return render_template_string('''
        <h1>Подраздел 1.2</h1>
        <p>Это подробности раздела 1.2.</p>
        <a href="/section1">Назад к разделу 1</a>
    ''')

# Раздел 2
@app.route('/section2')
def section2():
    return render_template_string('''
        <h1>Раздел 2</h1>
        <ul>
            <li><a href="/section2/subsection1">Подраздел 2.1</a></li>
            <li><a href="/section2/subsection2">Подраздел 2.2</a></li>
            <li><a href="/">Назад на главную</a></li>
        </ul>
    ''')

# Подраздел 2.1
@app.route('/section2/subsection1')
def subsection3():
    return render_template_string('''
        <h1>Подраздел 2.1</h1>
        <p>Это подробности раздела 2.1.</p>
        <a href="/section2">Назад к разделу 2</a>
    ''')

# Подраздел 2.2
@app.route('/section2/subsection2')
def subsection4():
    return render_template_string('''
        <h1>Подраздел 2.2</h1>
        <p>Это подробности раздела 2.2.</p>
        <a href="/section2">Назад к разделу 2</a>
    ''')

# Раздел 3
@app.route('/section3')
def section3():
    return render_template_string('''
        <h1>Раздел 3</h1>
        <ul>
            <li><a href="/section3/subsection1">Подраздел 3.1</a></li>
            <li><a href="/section3/subsection2">Подраздел 3.2</a></li>
            <li><a href="/">Назад на главную</a></li>
        </ul>
    ''')

# Подраздел 3.1
@app.route('/section3/subsection1')
def subsection5():
    return render_template_string('''
        <h1>Подраздел 3.1</h1>
        <p>Это подробности раздела 3.1.</p>
        <a href="/section3">Назад к разделу 3</a>
    ''')

# Подраздел 3.2
@app.route('/section3/subsection2')
def subsection6():
    return render_template_string('''
        <h1>Подраздел 3.2</h1>
        <p>Это подробности раздела 3.2.</p>
        <a href="/section3">Назад к разделу 3</a>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
