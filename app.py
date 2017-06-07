from flask import Flask
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
    
class Publicacao(db.Model):
    publicacao_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    edicao_id = db.Column(db.Integer, db.ForeignKey('edicao.edicao_id'))
    
class Forum(db.Model):
    forum_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    sigla = db.Column(db.String(20))
    tipo = db.Column(db.String(20))
    edicoes = db.relationship('Edicao', backref='forum', lazy='dynamic')

class Edicao(db.Model):
    edicao_id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    qualis = db.Column(db.String(20))
    pontucacao_qualis = db.Column(db.Integer)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.forum_id'))
    local_id = db.Column(db.Integer, db.ForeignKey('local.local_id'))
    publicacoes = db.relationship('Publicacao', backref='edicao', lazy='dynamic')
    
db.create_all()

@app.route("/")
def home():
    return "Bem Vindo!"

if __name__ == "__main__":
    app.run(debug=True)
