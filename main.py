from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False


@app.route('/blog', methods=['GET'])
def index():

    
    task_id = request.args.get('id')
    if task_id != None:
        task = Task.query.get(task_id)
        return render_template('blogpost.html', task=task)
    

    tasks = Task.query.filter_by(completed=False).all()
    
    return render_template('todos.html',title="BLOGS", 
        tasks=tasks)



@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/blog')



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    body_error = ''
    title_error = ''
    blog_body = ''
    blog_title = ''

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']

        if blog_title == '':
            title_error = "Enter a valid title"

        if blog_body == '':
            body_error = "Enter a valid body text"

    
        if title_error != '' or body_error != '':
            return render_template('addblog.html', 
            title_error=title_error, 
            body_error=body_error,
            blog_title=blog_title,
            blog_body=blog_body)
        else:
            new_blog = Task(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

        return redirect('/blog?id={0}'.format(new_blog.id))
                    
        
    return render_template('addblog.html',title="BLOGS")
    


if __name__ == '__main__':
    app.run()