from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models.user import User
from database import db
from flask import Flask, request, jsonify
import bcrypt


app = Flask(__name__)  # atraves do Flask eu posso criar a aplicacao
# Configuracoes:
# A primeira: relacionada ao flask / vai precisar disso para autenticacao
app.config['SECRET_KEY'] = "your_secret_key"
# A segunda: e aonde o seu banco de dados vai ficar, e como se conectar atraves dele.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

# Inicializacoes
db.init_app(app)  # db = SQLAlchemy(app) - Com essa variavel voce cria uma instancia da SQLAlchemy, ou seja vai ser um objeto. AQUI E AONDE A CONEXAO VAI EXISTIR
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # a view que vai ser utilizada para login:

# Carrega a sessao do usuario:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Rota de login:
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # recuperar o que o usuario mandou
    #print("Recebido:", data) debug
    username = data.get("username")  # recebendo as credenciais
    password = data.get("password")  # recebendo as credenciais

# LOGICA DA AUTENTICACAO:
    # Querying records: e um atributo chamado query que permite a busca. Metodo dentro do query: get() or filter()
    if username and password:
        # login
        
        user = User.query.filter_by(username=username).first() #retorna uma lista, mas precisamos so de um username, entao adicionar o first(), se nao, usamos o all()
       
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)  # para fazer a autenticacao
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticacao realizada com sucesso"})

    return jsonify({"message": "Credenciais invalidas"}), 400

#Rota de Logout:
@app.route('/logout', methods=['GET'])
@login_required #para proteger de usuarios nao autenticados
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

#Rota de Cadastrado:
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados invalidos"}), 400

#Rota de visualizacao:
@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuario nao encontrado"}), 404

#Rota de Update
@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({"message":"Operacao nao permitida"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuario {id_user} atualizado com sucesso"})
    
    return jsonify({"message": "Usuario nao encontrado"}), 404

#Rota de Delete
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operacao nao permitida"}), 403
    if id_user == current_user.id:  #verificar se ele quer apagar o usuario autenticado
        return jsonify({"message": "delecao nao permitida"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuario {id_user} deletado com sucesso"})
    
    return jsonify({"message": "Usuario nao encontrado"}), 404



# #Criar rota, metodo simples para testar se a rota esta funcionando, o metodo vai ser so o GET para que possamos recuperar a informacao
# @app.route("/hello-world", methods=['GET'])
# def hello_world():
#     return "Hello World!"



# para executar, precisamos saber se ele esta sendo executado manualmente.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # modo debug


# terminal -> falsk shell (e um comando que eu vou rodar para justamente conseguir entrar dentro da minha aplicacao do flask, e entao eu vou fazer a criacao do
# meu banco de dados na mao) -> db.create_all() (vai criar o banco de dados)  -> db.session(objeto) -> db.session.commit()(ele vai pegar tudo que voce fez naquela sessao e executar)
# -> exit() (fechar o shell) .: agora temos uma pasta instance com o banco de dados
# Session <- conexao ativa (e aonde eu consigo dar os comandos)
