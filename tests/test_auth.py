import json

def test_register_success(client):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['msg'] == 'User registered successfully'
    assert 'id' in data


def test_register_user_already_exists(client):
    client.post('/auth/register', json={
        'username': 'existinguser',
        'password': 'password123'
    })
    response = client.post('/auth/register', json={
        'username': 'existinguser',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.get_json()['msg'] == 'User already exists'


def test_register_missing_fields(client):
    response_no_user = client.post('/auth/register', json={'password': 'password123'})
    assert response_no_user.status_code == 400
    assert 'Username and Password are required' in response_no_user.get_json()['msg']

    response_no_pass = client.post('/auth/register', json={'username': 'user123'})
    assert response_no_pass.status_code == 400
    assert 'Username and Password are required' in response_no_pass.get_json()['msg']


def test_login_success(client):
    client.post('/auth/register', json={
        'username': 'loginuser',
        'password': 'loginpassword'
    })
    response = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_login_wrong_password(client):
    client.post('/auth/register', json={
        'username': 'userpass',
        'password': 'correctpassword'
    })
    response = client.post('/auth/login', json={
        'username': 'userpass',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == 'Invalid Credentials'

def test_login_nonexistent_user(client):
    response = client.post('/auth/login', json={
        'username': 'nouser',
        'password': 'anypassword'
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == 'Invalid Credentials'
