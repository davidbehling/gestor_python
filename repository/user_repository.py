from database import session
from models.user import User

def create_user(name):
    user = User(name=name)
    session.add(user)
    session.commit()
    return user

def list_users():
    return session.query(User).order_by(User.name.asc()).all()

def find_user_id(id):
    return session.query(User).filter_by(id=id).first()

def update_user(id, new_name):
    user = find_user_id(id)
    user.name = new_name
    session.commit()

def delete_user(id):
    user = find_user_id(id)
    session.delete(user)
    session.commit()
