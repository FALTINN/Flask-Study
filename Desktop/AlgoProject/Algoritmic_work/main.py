from flask import *
import db


def index():
    if request.method == 'POST':
        name = request.form.get("name")
        text = request.form.get("text")
        contact = request.form.get("contact")
        salary = request.form.get("salary")
        db.insert(db.con, f'INSERT INTO `status` (`text`) VALUES ("{name}, ваша заявка ещё не принята. Не просмотрено")')
        present_id = db.query(db.con, 'SELECT * FROM status where `id` = (SELECT MAX(`id`) FROM status)')
        present_id = present_id[0][0]
        db.insert(db.con, f'INSERT INTO `data` (`sender`, `text`, `contact`, `salary`, `status_id`) VALUES ("{name}", "{text}", "{contact}", "{salary}", "{present_id}")')
        session['name'] = name
    db.debug(db.con, "START")
    form = ''
    if 'name' in session.keys():
        form = f"{session['name']}, спасибо. Мы обрабатываем вашу вакансию"
    else:
        form = Markup(render_template("form.html"))
    return render_template("index.html", form=form)

def table_from():
    db.debug(db.con, "Vacancy")
    table = ''
    if 'name' in session.keys():
        table_value = db.query(
        db.con, f'''SELECT data.id, `sender`, data.text, `contact`, `salary`, status.text, status.id
                From data
                INNER JOIN status ON data.status_id = status.id
                where `sender` = "{session['name']}"'''
    )
        db.insert(db.con, f"UPDATE status SET text=\"{session['name']}, ваша заявка ещё не принята. Просмотрено\" WHERE `id` = {table_value[0][6]}")
        form = Markup(render_template("top_list.html"))
        form += Markup(render_template("table_be.html", table_value=table_value))
    else:
        form = f"Уважаемый юзер, вы не подавали заявку"
    return render_template("table_form.html", table=form)

def all_table():
    table_value = db.query(
        db.con, f'''SELECT data.id, `sender`, data.text, `contact`, `salary`, status.text, status.id
                From data
                INNER JOIN status ON data.status_id = status.id
                ORDER BY data.id'''
    )
    present_id = db.query(db.con, 'SELECT id FROM status where `id` = (SELECT MAX(`id`) FROM status)')
    forms = Markup(render_template("top_list.html"))
    for i in range(0, present_id[0][0]-1):
        form = Markup(render_template("list_table.html", table_value=table_value[i])) 
        forms += form  
    return render_template("table_form.html", table=forms) 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secretnik'
app.add_url_rule("/", 'index', index, methods=['GET', 'POST'])
app.add_url_rule("/vacancy", 'table_from', table_from)
app.add_url_rule("/list_vacancy", 'all_table', all_table)

app.run()