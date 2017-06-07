from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@devtools:3306/publicacoes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Local(db.Model):
    local_id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(40))
    pais = db.Column(db.String(40))
    edicoes = db.relationship('Edicao', backref='local', lazy='dynamic')

    def __repr__(self):
        return str({'local_id': self.local_id, 'cidade': self.cidade, 'pais': self.pais})

pub_autores = db.Table('pub_autores',
    db.Column('publicacao_id', db.Integer, db.ForeignKey('publicacao.publicacao_id')),
    db.Column('autor_id', db.Integer, db.ForeignKey('autor.autor_id'))
)

class Autor(db.Model):
    autor_id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11))
    nome = db.Column(db.String(100))
    nome_citacao = db.Column(db.String(40))
    publicacoes = db.relationship('Publicacao', secondary=pub_autores, backref=db.backref('autores', lazy='dynamic'))

    def __repr__(self):
        return {'autor_id': self.autor_id, 'cpf': self.cpf, 'nome': self.nome, 'nome_citacao': self.nome_citacao}

class Publicacao(db.Model):
    publicacao_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    edicao_id = db.Column(db.Integer, db.ForeignKey('edicao.edicao_id'))

    def __repr__(self):
        return {'publicacao_id': self.publicacao_id, 'titulo': self.titulo}

class Forum(db.Model):
    forum_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    sigla = db.Column(db.String(20))
    tipo = db.Column(db.String(20))
    edicoes = db.relationship('Edicao', backref='forum', lazy='dynamic')

    def __repr__(self):
        return {'forum_id':self.forum_id, 'nome':self.nome, 'sigla':self.sigla, 'tipo':self.tipo}

class Edicao(db.Model):
    edicao_id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    qualis = db.Column(db.String(20))
    pontucacao_qualis = db.Column(db.Integer)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.forum_id'))
    local_id = db.Column(db.Integer, db.ForeignKey('local.local_id'))
    publicacoes = db.relationship('Publicacao', backref='edicao', lazy='dynamic')

    def __repr__(self):
        return {'edicao_id':self.edicao_id, 'ano':self.ano, 'qualis':self.qualis, 'pontucacao_qualis':self.pontucacao_qualis}

db.create_all()

@app.route("/")
def home():
    return "Bem Vindo!"

@app.route("/locais", methods=['GET'])
def get_locais():
    rio = Local(cidade='Rio de Janeiro', pais='Brasil')
    return jsonify(str(rio))

if __name__ == "__main__":
    app.run(debug=True)
