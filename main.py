from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_item = db.Column(db.String(500), unique=True, nullable=False)


@app.route("/", methods=["GET", "POST"])
def home():
    todo_list = Todo.query.all()
    check = False
    if todo_list:
        check = True
    if request.method == "POST":
        new_todo = Todo(
            list_item=request.form['todo']
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('index.html', todo=todo_list, check=check)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_to_delete = Todo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
