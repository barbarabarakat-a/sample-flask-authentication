from flask_sqlalchemy import SQLAlchemy #essa classe e que vai fazer a conexao com o banco de dados
#from models.user import User - nao pode usar esse metodo, porque vai dar uma importacao circular. (app importa user e user importa app)
#O comentario acima e se caso todos esses imports estivessem no arquivo app.py
#Movemos o flaskalchemy e o db(sem o app como parametro) para que nao de a importacao circular

db = SQLAlchemy() #Com essa variavel voce cria uma instancia da SQLAlchemy, ou seja vai ser um objeto. AQUI E AONDE A CONEXAO VAI EXISTIR
