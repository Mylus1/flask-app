from http import client
from importlib import reload
import unittest
from flask_app import app

TODOS = {
    'todo1': {'task': 'Build an API'},
    'todo2': {'task': 'Become Head Ninja'},
    'todo3': {'task': 'Retire'},
}

class TestTodo(unittest.TestCase):
    
    def setUp(self) -> None:
        reload(app)
        self.client = app.app.test_client()
    
    def test_connection(self):
        response = self.client.get("/todos")
        assert response.status_code == 200
    
    def test_todo_single_view(self):
        response = self.client.get("/todos/todo1")
        json_response = response.json
        self.assertEqual(TODOS['todo1'], json_response)
        
    def test_todo_create(self):
        response = self.client.post('/todos', json={'task' : 'Start writing tests'})
        self.assertIn('Start writing tests', response.text)
        
    def test_todo_delete_request(self):
        response = self.client.delete('/todos/todo1')
        self.assertEqual(response.status_code, 204)
        
    def test_todo_delete_actual(self):
        response = self.client.delete('todos/todo1')
        get_todos = self.client.get('/todos')
        self.assertNotIn("todo1", get_todos.text)
        
    def test_todo_full_list(self):
        response = self.client.get("/todos")
        json_response = response.json
        self.assertEqual(TODOS, json_response)
        
    def test_abort_if_todo_doesnt_exist(self):
        response = self.client.get('/todos/todo5')
        self.assertEqual(response.status_code, 404)
        
    def test_abort_if_todo_already_exists(self):
        response = self.client.post('/todos', json={"task" : "Build an API"})
        self.assertEqual(response.status_code, 422)
        
    def test_todo_update(self):
        response = self.client.put("/todos/todo1", json={'task' : 'Update some tests'})
        self.assertIn('Update some tests', response.text)
        