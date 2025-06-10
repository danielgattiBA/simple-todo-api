from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Simplesmente armazenamos as tarefas em memória
todos = {}

@app.route('/')
def health_check():
    return "API de Tarefas está online!", 200

@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or not 'title' in request.json:
        return jsonify({"error": "O campo 'title' é obrigatório."}), 400
    
    todo_id = str(uuid.uuid4())
    todo = {
        'id': todo_id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    todos[todo_id] = todo
    return jsonify(todo), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(list(todos.values()))

@app.route('/todos/<string:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Tarefa não encontrada."}), 404

@app.route('/todos/<string:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        return jsonify({"error": "Tarefa não encontrada."}), 404
    
    if not request.json:
        return jsonify({"error": "Dados inválidos."}), 400
    
    todo['title'] = request.json.get('title', todo['title'])
    todo['description'] = request.json.get('description', todo['description'])
    todo['done'] = request.json.get('done', todo['done'])
    return jsonify(todo)

@app.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todos.pop(todo_id, None):
        return jsonify({"result": True}), 200
    return jsonify({"error": "Tarefa não encontrada."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
