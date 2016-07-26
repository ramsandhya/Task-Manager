from flask import Flask, request, render_template, redirect
import pg

db = pg.DB(dbname='taskmanager')

app = Flask('TaskManagerApp')

@app.route('/')
def tasks():
    query = db.query('''
        select
            tasks.id,
            tasks.name,
            tasks.complete
        from tasks
        order by
        tasks.name
    ''')
    tasks = query.namedresult()
    return render_template('todolist.html', title='Your tasks', tasks = tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    db.insert('tasks', name=task_name, complete='False')
    return redirect('/')

@app.route('/edit_task', methods=['POST'])
def edit_task():
    checked_tasks = request.form.keys()
    # print checked_tasks
    action_item = len(checked_tasks) - 1
    # print checked_tasks[action_item]
    for task in checked_tasks:
        if task != 'Complete' and task != 'Delete':
            if checked_tasks[action_item] == 'Complete':
                strike(task)
                db.update('tasks', {'id': task, 'complete': True})
            elif checked_tasks[action_item] == 'Delete':
                db.delete('tasks', {'id':task})
    return redirect('/')
    # task_id = request.form['task.id']
    # for task in tasks:
    #     print task
def strike(anytask):
    result = ''
    for c in anytask:
        result = result + c + '\u0336'
    return result



app.debug = True

if __name__ == "__main__":
    app.run(debug=True)

# html = '<ol>'
# for task in query.namedresult():
#     html += '<li>%s - %r</li>' % (task.name, task.complete)
# html += '</ol>'
# return html
