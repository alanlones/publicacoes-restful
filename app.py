from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/publicacoes6'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@devtools:3306/publicacoes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Local(db.Model):
    local_id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(40))
    pais = db.Column(db.String(40))
    edicoes = db.relationship('Edicao', backref='local', lazy='dynamic')

    def toJson(self):
        return {'local_id': self.local_id, 'cidade': self.cidade, 'pais': self.pais}

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

    def toJson(self):
        return {'autor_id': self.autor_id, 'cpf': self.cpf, 'nome': self.nome, 'nome_citacao': self.nome_citacao}


class Publicacao(db.Model):
    publicacao_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    edicao_id = db.Column(db.Integer, db.ForeignKey('edicao.edicao_id'))

    def toJson(self):
        return {'publicacao_id': self.publicacao_id, 'titulo': self.titulo}


class Forum(db.Model):
    forum_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    sigla = db.Column(db.String(20))
    tipo = db.Column(db.String(20))
    edicoes = db.relationship('Edicao', backref='forum', lazy='dynamic')

    def toJson(self):
        return {'forum_id':self.forum_id, 'nome':self.nome, 'sigla':self.sigla, 'tipo':self.tipo}


class Edicao(db.Model):
    edicao_id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    qualis = db.Column(db.String(20))
    pontuacao_qualis = db.Column(db.Integer)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.forum_id'))
    local_id = db.Column(db.Integer, db.ForeignKey('local.local_id'))
    publicacoes = db.relationship('Publicacao', backref='edicao', lazy='dynamic')

    def toJson(self):
        return {'edicao_id':self.edicao_id, 'ano':self.ano, 'qualis':self.qualis, 'pontucacao_qualis':self.pontucacao_qualis}

def rollback_bd():
    db.drop_all()
    db.create_all()

    local1 = Local(cidade='Rio de Janeiro', pais='Brasil')
    local2 = Local(cidade='New York', pais="United States")

    forum1 = Forum(nome="Sensors to Cloud Architectures Workshop", sigla="SCAW", tipo="journal")
    forum2 = Forum(nome="International Symposium on Integrated Network Management", sigla="IM", tipo="journal")

    edicao1 = Edicao(ano="2016", qualis="B1", pontuacao_qualis="20", local=local1, forum=forum1)
    edicao2 = Edicao(ano="2014", qualis="B2", pontuacao_qualis="16", local=local2, forum=forum2)

    pub1 = Publicacao(
        titulo="A Cloud-based Architecture for the Internet of Things Targeting Industrial Engine Remote Monitoring",
        edicao=edicao1)
    pub2 = Publicacao(titulo="ResearchOps: The case for DevOps in scientific applications",
                      edicao=edicao2)

    leo = Autor(cpf="12345678900", nome="Leonardo Guerreiro Azevedo", nome_citacao="AZEVEDO, L.G.")
    kate = Autor(cpf="12345678911", nome="Kate Cerqueira Revoredo", nome_citacao="REVOREDO, K.C.")
    flavia = Autor(cpf="12345678922", nome="Flávia Maria Santoro", nome_citacao="SANTORO, F.M.")
    gleison = Autor(cpf="12345678933", nome="Gleison do Santos Souza", nome_citacao="SOUZA, G.S.")

    db.session.add(local1)
    db.session.add(local2)
    db.session.add(forum1)
    db.session.add(forum2)
    db.session.add(edicao1)
    db.session.add(edicao2)
    db.session.add(pub1)
    db.session.add(pub2)
    db.session.add(leo)
    db.session.add(kate)
    db.session.add(gleison)
    db.session.add(flavia)

    db.session.commit()

    pub1.autores.append(leo)
    pub1.autores.append(kate)
    pub2.autores.append(gleison)
    pub2.autores.append(flavia)
    pub2.autores.append(leo)

    db.session.commit()


rollback_bd()



@app.route("/")
def home():
    return "1337 SOA"

## GET ##

@app.route("/locais", methods=['GET'])
def get_locais():
    locais = Local.query.filter().all()
    return jsonify(str(locais))

@app.route("/locais/<int:local_id>", methods=['GET'])
def get_local(local_id):
    local = Local.query.filter_by(local_id=local_id).first()
    return jsonify(str(local))

@app.route("/autores", methods=['GET'])
def get_autores():
    autores = Autor.query.filter().all()
    return jsonify(str(autores))

@app.route("/autores/<int:autor_id>", methods=['GET'])
def get_autor(autor_id):
    autor = Autor.query.filter_by(autor_id=autor_id).first()
    return jsonify(str(autor))

@app.route("/publicacoes", methods=['GET'])
def get_publicacoes():
    publicacoes = Publicacao.query.filter().all()
    return jsonify(str(publicacoes))

@app.route("/publicacoes/<int:publicacao_id>", methods=['GET'])
def get_publicacao(publicacao_id):
    publicacao = Publicacao.query.filter_by(publicacao_id=publicacao_id).first()
    return jsonify(str(publicacao))

@app.route("/edicoes", methods=['GET'])
def get_edicoes():
    edicoes = Edicao.query.filter().all()
    return jsonify(str(edicoes))

@app.route("/edicoes/<int:edicao_id>", methods=['GET'])
def get_edicao(edicao_id):
    edicao = Edicao.query.filter_by(edicao_id=edicao_id).first()
    return jsonify(str(edicao))

@app.route("/foruns", methods=['GET'])
def get_foruns():
    foruns = Forum.query.filter().all()
    return jsonify(str(foruns))

@app.route("/foruns/<int:forum_id>", methods=['GET'])
def get_forum(forum_id):
    forum = Forum.query.filter_by(forum_id=forum_id).first()
    return jsonify(str(forum))

if __name__ == "__main__":
    app.run(debug=True)
