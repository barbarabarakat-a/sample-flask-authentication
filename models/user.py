from database import db 
from flask_login import UserMixin #para a atutenticacao funcionar


#primeiro mapeamento: do usuario
class User(db.Model, UserMixin): #Ela vai ser herdada de uma outra classe do db model. Esse model vai dar base para o flaskalchemy saber que e algo mapeavel.
    #id(int), username(str), password(str), role(text) = precisa definir uma coluna
    id = db.Column(db.Integer, primary_key=True) #chave primaria: e uma chave que identifica os itens na tabela. unica
    username = db.Column(db.String(80), nullable=False, unique=True) #entre parenteses esta a quantidade de caracteres que o usuario pode armazenar no username. demilitacao - depois da virgula esta a condicao se eu aceito um valor nulo, por exemplo sem nenhum valor 
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

#modelagem do usuario: conceito que permite que possamos fazer a autenticacao atraves do usuario