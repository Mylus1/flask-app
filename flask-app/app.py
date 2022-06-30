from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import requests

app = Flask(__name__)
api = Api(app)
response = requests.get('http://127.0.0.1:5000/TodoList')
todo_json = response.json()

TODOS = {
    'todo1': {'task': 'Build an API'},
    'todo2': {'task': 'Become Head Ninja'},
    'todo3': {'task': 'Retire'},
}
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message=f"Todo {todo_id} doesn't exist")
        
parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = f"todo{todo_id}"
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

@app.route('/TodoList')
def list_todos():
    return TODOS

@app.route('/Todo')
def list_todo():
    pass

if __name__ == '__main__':
    app.run(debug=True)