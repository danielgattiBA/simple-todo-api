import pytest
from app import app, todos

# Adicione pytest ao requirements.txt ou instale: pip install pytest

@pytest.fixture
def client():
    # Configura o app para testes
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Limpa as tarefas em memória após cada teste
    todos.clear()

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"API de Tarefas está online!" in response.data

def test_create_todo(client):
    response = client.post('/todos', json={'title': 'Comprar Leite'})
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Comprar Leite'
    assert not response.json['done']

def test_get_todos_empty(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_get_todos_with_items(client):
    client.post('/todos', json={'title': 'Tarefa 1'})
    client.post('/todos', json={'title': 'Tarefa 2'})
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['title'] == 'Tarefa 1'
    assert response.json[1]['title'] == 'Tarefa 2'

def test_get_single_todo(client):
    create_response = client.post('/todos', json={'title': 'Tarefa Única'})
    todo_id = create_response.json['id']
    
    get_response = client.get(f'/todos/{todo_id}')
    assert get_response.status_code == 200
    assert get_response.json['title'] == 'Tarefa Única'

def test_update_todo(client):
    create_response = client.post('/todos', json={'title': 'Tarefa a Atualizar'})
    todo_id = create_response.json['id']
    
    update_response = client.put(f'/todos/{todo_id}', json={'title': 'Tarefa Atualizada', 'done': True})
    assert update_response.status_code == 200
    assert update_response.json['title'] == 'Tarefa Atualizada'
    assert update_response.json['done'] == True

def test_delete_todo(client):
    create_response = client.post('/todos', json={'title': 'Tarefa a Deletar'})
    todo_id = create_response.json['id']
    
    delete_response = client.delete(f'/todos/{todo_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['result'] == True
    
    get_response = client.get(f'/todos/{todo_id}')
    assert get_response.status_code == 404 # Garante que foi deletado
