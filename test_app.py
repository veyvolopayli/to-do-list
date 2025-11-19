import unittest
from app import app, tasks


class TestToDo(unittest.TestCase):

    # Итерация 8: Подготовка окружения перед каждым тестом
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        tasks.clear()  # Очищаем список перед каждым тестом, чтобы ID всегда начинался с 1

    # Итерация 1
    def test_app_exists(self):
        self.assertIsNotNone(app)

    # Итерация 2
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Итерация 3
    def test_tasks_list_exists(self):
        self.assertIsInstance(tasks, list)

    # Итерация 4
    def test_get_tasks_empty(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # Итерация 5
    def test_create_task(self):
        response = self.client.post('/tasks', json={'title': 'Buy milk'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(tasks), 1)

    # Итерация 6
    def test_create_task_no_title(self):
        response = self.client.post('/tasks', json={})
        self.assertEqual(response.status_code, 400)

    # Итерация 7
    def test_task_has_id(self):
        self.client.post('/tasks', json={'title': 'Task 1'})
        self.assertIn('id', tasks[-1])

    # Итерация 9
    def test_task_default_status(self):
        self.client.post('/tasks', json={'title': 'Sleep'})
        self.assertFalse(tasks[-1]['done'])

    # Итерация 10
    def test_get_single_task(self):
        self.client.post('/tasks', json={'title': 'Test One'})
        # Так как список очищается, ID будет 1
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Test One')

    # Итерация 11
    def test_get_non_existent_task(self):
        response = self.client.get('/tasks/999')
        self.assertEqual(response.status_code, 404)

    # Итерация 12
    def test_update_task(self):
        self.client.post('/tasks', json={'title': 'To Update'})
        response = self.client.put('/tasks/1', json={'done': True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tasks[0]['done'])

    # Итерация 13
    def test_delete_task(self):
        self.client.post('/tasks', json={'title': 'To Delete'})
        response = self.client.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tasks), 0)

    # Итерация 14
    def test_delete_non_existent(self):
        response = self.client.delete('/tasks/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()