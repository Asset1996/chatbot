# from datetime import datetime
# from app import db

# class Users(db.Model):
#     # Создаем таблицу пользователей
#     __tablename__ = 'support_user'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(250), index=True, unique=True)

#     def find_user_in_db(email):
#         user = db.session.query(Users).filter(Users.email == f'{email}').all()
#         return user

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<User {}>'.format(self.email)