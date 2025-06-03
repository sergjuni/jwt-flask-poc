import pytest
from app import create_app
from app.auth_utils import reset_user_store_for_testing


@pytest.fixture(scope='function')
def app():
    """Cria e configura uma nova instância da app para cada teste."""
    reset_user_store_for_testing()
    app_instance = create_app()
    app_instance.config.update({
        "TESTING": True,
        # "JWT_SECRET_KEY": "test-jwt-secret-key"
    })

    yield app_instance # Fornece a instância do app para o teste


@pytest.fixture
def client(app):
    """Um cliente de teste para a app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Um runner para testar comandos CLI do Flask (não usaremos agora, mas é útil)."""
    return app.test_cli_runner()

@pytest.fixture
def auth_token(client):
    """
    Registra um usuário de teste, faz login e retorna um token de acesso.
    Usa o 'client' fixture, que por sua vez usa o 'app' fixture (com o reset).
    """
    client.post('/auth/register', json={
        'username': 'testuser_fixture',
        'password': 'password123'
    })
    response = client.post('/auth/login', json={
        'username': 'testuser_fixture',
        'password': 'password123'
    })
    data = response.get_json()
    assert 'access_token' in data
    return data['access_token']