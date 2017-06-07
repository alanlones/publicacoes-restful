from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/publicacoes2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@devtools:3306/publicacoes'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/publicacoes' #estagio
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


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
        return {'edicao_id':self.edicao_id, 'ano':self.ano, 'qualis':self.qualis, 'pontuacao_qualis':self.pontuacao_qualis}

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

##### LOCAL #####

@app.route("/locais", methods=['GET'])
def get_locais():
    locais = Local.query.filter().all()
    locais_json = []
    for local in locais:
        locais_json.append(local.toJson())
    return jsonify(locais_json)

@app.route('/locais/<int:local_id>', methods=['GET'])
def get_local(local_id):
    local = Local.query.filter_by(local_id=local_id).first()
    return jsonify(local.toJson())

@app.route('/locais/<int:local_id>', methods=['PUT'])
def update_local(local_id):
    if not request.json:
        abort(400)

    cidade = request.json['cidade']
    pais = request.json['pais']

    local = Local.query.filter_by(local_id=local_id).first()
    local.cidade = cidade;
    local.pais = pais;

    db.session.add(local)
    db.session.commit()

    return get_local(local_id)



##### AUTOR #####

@app.route("/autores", methods=['GET'])
def get_autores():
    autores = Autor.query.filter().all()
    autores_json = []
    for autor in autores:
        autores_json.append(autor.toJson())
    return jsonify(autores_json)

@app.route("/autores/<int:autor_id>", methods=['GET'])
def get_autor(autor_id):
    autor = Autor.query.filter_by(autor_id=autor_id).first()
    return jsonify(autor.toJson())

@app.route('/autores/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    if not request.json:
        abort(400)

    cpf = request.json['cpf']
    nome = request.json['nome']
    nome_citacao = request.json['nome_citacao']

    autor = Autor.query.filter_by(autor_id=autor_id).first()
    autor.cpf = cpf
    autor.nome = nome
    autor.nome_citacao = nome_citacao

    db.session.add(autor)
    db.session.commit()

    return get_autor(autor_id)

@app.route('/autores', methods=['POST'])
def create_autor():
	if not request.json:
		abort(400)

	autor = Autor(cpf=request.json['cpf'],
	nome=request.json['nome'],
	nome_citacao=nome_citacao.json['nome_citacao'])
	
	db.session.add(autor)
	db.session.commit()
	
	return get_autores()

@app.route('/autores/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
	autor = Autor.query.filter_by(autor_id=autor_id).first()
	db.session.delete(autor)
	db.session.commit()

	return jsonify({'result': True})


@app.route("/autores/<int:autor_id>/resumo", methods=['GET'])
def get_resumo_autor(autor_id):
    autor = Autor.query.filter_by(autor_id=autor_id).first()

    r = db.engine.execute('SELECT P.TITULO, ED.QUALIS FROM AUTOR A INNER JOIN pub_autores PA ON A.AUTOR_ID = PA.autor_id INNER JOIN PUBLICACAO P ON PA.publicacao_id = P.PUBLICACAO_ID INNER JOIN EDICAO ED ON P.EDICAO_ID = ED.EDICAO_ID WHERE A.AUTOR_ID = {}'.format(autor_id))

    rjson = []

    for i in r:
    	rjson.append({'titulo':i[0], 'qualis':i[1]})

    return jsonify(rjson)


@app.route("/autores/<int:autor_id>/pontuacao", methods=['GET'])
def get_pontuacao_autor(autor_id):
    autor = Autor.query.filter_by(autor_id=autor_id).first()

    r = db.engine.execute('SELECT SUM(ED.PONTUACAO_QUALIS) FROM AUTOR A INNER JOIN pub_autores PA ON A.AUTOR_ID = PA.autor_id INNER JOIN PUBLICACAO P ON PA.publicacao_id = P.PUBLICACAO_ID INNER JOIN EDICAO ED ON P.EDICAO_ID = ED.EDICAO_ID WHERE A.AUTOR_ID = {}'.format(autor_id))

    rjson = []

    for i in r:
    	rjson.append({'pontuacaoQualis' : int(i[0])})

    return jsonify(rjson)



##### PUBLICACAO #####

@app.route("/publicacoes", methods=['GET'])
def get_publicacoes():
    publicacoes = Publicacao.query.filter().all()
    pub_json = []
    for pub in publicacoes:
        pub_json.append(pub.toJson())
    return jsonify(pub_json)

@app.route("/publicacoes/<int:publicacao_id>", methods=['GET'])
def get_publicacao(publicacao_id):
    publicacao = Publicacao.query.filter_by(publicacao_id=publicacao_id).first()
    return jsonify(publicacao.toJson())

@app.route('/publicacoes/<int:publicacao_id>', methods=['PUT'])
def update_publicacao(publicacao_id):
    if not request.json:
        abort(400)

    titulo = request.json['titulo']

    publicacao = Publicacao.query.filter_by(publicacao_id=publicacao_id).first()
    publicacao.titulo = titulo;

    db.session.add(publicacao)
    db.session.commit()

    return get_publicacao(publicacao_id)

@app.route('/publicacoes', methods=['POST'])
def create_publicacao():
	if not request.json:
		abort(400)

	publicacao = Publicacao(titulo=request.json['titulo'])

	for autor_id in request.json['autores']:
		publicacao.autores.append(Autor.query.filter_by(autor_id=autor_id).first())

	edicao_id = request.json['edicao_id']

	publicacao.edicao = Edicao.query.filter_by(edicao_id=edicao_id).first()
	
	db.session.add(publicacao)
	db.session.commit()
	
	return get_publicacoes()

@app.route('/publicacoes/<int:publicacao_id>', methods=['DELETE'])
def delete_publicacao(publicacao_id):
    publicacao = Publicacao.query.filter_by(publicacao_id=publicacao_id).first()
    
    db.session.delete(publicacao)
    db.session.commit()

    return jsonify({'result': True})

@app.route('/publicacoes/<int:publicacao_id>/resumo', methods=['GET'])
def get_resumo_pub(publicacao_id):
	publicacao = Publicacao.query.filter_by(publicacao_id=publicacao_id).first()

	nomes_citacao = []

	for autor in publicacao.autores:
		nomes_citacao.append(autor.nome_citacao)

	pub_resumo = {
		'titulo' : publicacao.titulo,
		'ano' : publicacao.edicao.ano,
		'autores' : nomes_citacao
	}

	return jsonify(pub_resumo)

##### EDICAO #####

@app.route("/edicoes", methods=['GET'])
def get_edicoes():
    edicoes = Edicao.query.filter().all()
    edicoes_json = []
    for edicao in edicoes:
        edicoes_json.append(edicao.toJson())
    return jsonify(edicoes_json)

@app.route("/edicoes/<int:edicao_id>", methods=['GET'])
def get_edicao(edicao_id):
    edicao = Edicao.query.filter_by(edicao_id=edicao_id).first()
    return jsonify(edicao.toJson())

##### FORUM #####

@app.route("/foruns", methods=['GET'])
def get_foruns():
    foruns = Forum.query.filter().all()
    foruns_json = []
    for forum in foruns:
        foruns_json.append(forum.toJson())
    return jsonify(foruns_json)

@app.route("/foruns/<int:forum_id>", methods=['GET'])
def get_forum(forum_id):
    forum = Forum.query.filter_by(forum_id=forum_id).first()
    return jsonify(forum.toJson())

if __name__ == "__main__":
    app.run(debug=True)
