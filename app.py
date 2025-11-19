from flask import Flask, jsonify, request

app = Flask(__name__)

# Хранилище задач (в памяти)
tasks = []


@app.route('/')
def index():
    return "Hello from docker!"


@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        if not request.json or 'title' not in request.json:
            return jsonify({'error': 'Title is required'}), 400

        task = {
            'id': tasks[-1]['id'] + 1 if tasks else 1,  # Генерация ID
            'title': request.json['title'],
            'done': False
        }
        tasks.append(task)
        return jsonify(task), 201

    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return jsonify(task)

    if request.method == 'PUT':
        task['done'] = request.json.get('done', task['done'])
        task['title'] = request.json.get('title', task['title'])
        return jsonify(task)

    if request.method == 'DELETE':
        tasks.remove(task)
        return jsonify({'result': True})

    return None


@app.route('/version')
def version():
    """
    Возвращает текущую версию API.
    Формат ответа: JSON {'version': 'x.x.x'}
    """
    return jsonify({"version": "1.1.0"})


if __name__ == '__main__':
    app.run(debug=True)
