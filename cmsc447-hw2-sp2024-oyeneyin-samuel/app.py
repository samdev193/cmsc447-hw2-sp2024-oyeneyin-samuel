from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('todolist.db')
curr = conn.cursor()
curr.execute("""CREATE TABLE IF NOT EXISTS todo_list(fname text, id integer, points integer)""")
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    conn = sqlite3.connect('todolist.db')
    curr = conn.cursor()
    curr.execute('''SELECT * FROM todo_list''')
    items = curr.fetchall()
    target_item = ""
    if request.method == 'POST':
        id = request.form['search']
        curr.execute('''SELECT fname, id, points FROM todo_list WHERE id=(?)''', (id,))
        results = curr.fetchall()
        if results:
            target_item = list(results[0])
        else:
            target_item = ""
    conn.close()
    return render_template('index.html', items=items, target_item=target_item)


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']  # pulling from a specific form.
    id = int(request.form['id'])
    points = int(request.form['points'])
    conn = sqlite3.connect('todolist.db')
    curr = conn.cursor()
    curr.execute('''INSERT INTO todo_list (fname, id, points) VALUES (?, ?, ?)''', (name, id, points))
    conn.commit()
    curr.close()
    return redirect('/')


@app.route('/updateName', methods=['POST'])
def updateName():
    new_name = request.form['new name']
    id = request.form['id']
    conn = sqlite3.connect('todolist.db')
    curr = conn.cursor()
    curr.execute('''UPDATE todo_list SET fname=(?) WHERE id=(?)''', (new_name, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/updatePoints', methods=['POST'])
def updatePoints():
    new_points = request.form['new points']
    id = request.form['id']
    conn = sqlite3.connect('todolist.db')
    curr = conn.cursor()
    curr.execute('''UPDATE todo_list SET points=(?) WHERE id=(?)''', (new_points, id))
    conn.commit()
    conn.close()
    return redirect('/')
@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    id = int(request.form['id'])
    points = int(request.form['points'])
    conn = sqlite3.connect('todolist.db')
    curr = conn.cursor()
    curr.execute('''DELETE FROM todo_list WHERE fname=(?) AND id=(?) AND points=(?)''', (name, id, points))
    conn.commit()
    curr.close()
    return redirect('/')


if __name__ == '__main__':
    app.run()
