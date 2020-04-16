from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432/todoapp'
# This links the db to our Flask app
db = SQLAlchemy(app)

migrate = Migrate(app, db) #we need to pass in our app and db instances when creating instance of Migrate

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # repr() function returns a printable representation of the given object
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# We call db.create_all() to create the above table, however commented out due to use of Migrations instead
# db.create_all()


# In this case the index() method is the controller that determines how to handle 
# behavior when user lands on the home page, in this case telling it 
# to use the index.html View and the 'data' Model
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all()
    )

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # First try and see if we can execute below, if not we can catch the exception further below

        # Get the form description through the request object's get_json() method which returns a dictionary
        # We can then use the 'description' key to get the value'
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description    
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        # Now we can return the 'description' key/value pair to the front end as a json response
        return jsonify(body)