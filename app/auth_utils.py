from werkzeug.security import generate_password_hash, check_password_hash


users_db = {}
_user_id_counter = 1


def reset_user_store_for_testing():
    global _user_id_counter
    users_db.clear()
    _user_id_counter = 1

def register_user_util(username, password):
  global _user_id_counter
  if username in users_db:
    return None

  users_db[username] = {
      'id': _user_id_counter,
      'username': username,
      'password': generate_password_hash(password)
  }
  _user_id_counter += 1
  return users_db[username]

def authenticate_user_util(username, password):
  user = users_db.get(username)
  print('users_db', users_db)

  print('user inside the authenticate user', user)
  if user and check_password_hash(user['password'], password):
    return user
  return None
