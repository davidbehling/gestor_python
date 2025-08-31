from database import session
from models.category import Category

def create_category(name, expense):
    category = Category(name=name, expense=expense)
    session.add(category)
    session.commit()
    return category

def list_categories(expense=None):
    query = session.query(Category).order_by(Category.name.asc())

    if expense != None:
      query = query.filter_by(expense=expense)

    query = query.order_by(Category.name.asc())

    return query.all()

def find_category_id(id):
    return session.query(Category).filter_by(id=id).first()

def update_category(id, new_name):
    category = find_category_id(id)
    category.name = new_name
    session.commit()

def delete_category(id):
    category = find_category_id(id)
    session.delete(category)
    session.commit()
    
    
