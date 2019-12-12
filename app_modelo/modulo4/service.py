
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/demo1_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/db_projeto_modelo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)


# Modelo Class/Model
class Modelo(db.Model):

    __tablename__ = 'modelo_mod'
    __table_args__ = {'extend_existing': True}

    id = db.Column("id_modelo", db.Integer, primary_key=True)
    sigla = db.Column("ds_sigla_mod", db.String(45), nullable=False)
    nome = db.Column("ds_nome_mod", db.String(100), nullable=False)

    def __init__(self, sigla, nome):
      self.sigla = sigla
      self.nome = nome

    def __repr__(self):
        return f"Modelo('{self.sigla}', '{self.nome}')"


# Modelo Schema
class ModeloSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sigla', 'nome')


# Init schema
modelo_schema = ModeloSchema(strict=True)
modelos_schema = ModeloSchema(many=True, strict=True)


# Create a Modelo
@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


# Create a Modelo
@app.route('/modelo', methods=['POST'])
def add_modelo():
    sigla = request.json['sigla']
    nome = request.json['nome']

    new_modelo = Modelo(sigla, nome)

    db.session.add(new_modelo)
    db.session.commit()

    return modelo_schema.jsonify(new_modelo)


# Get All Modelos
@app.route('/modelo', methods=['GET'])
def get_modelos():
    all_modelos = Modelo.query.all()
    result = modelos_schema.dump(all_modelos)
    return jsonify(result.data)


# Get Single Modelo
@app.route('/modelo/<id>', methods=['GET'])
def get_modelo(id):
    modelo = Modelo.query.get(id)
    return modelo_schema.jsonify(modelo)


# Update a Modelo
@app.route('/modelo/<id>', methods=['PUT'])
def update_modelo(id):
    modelo = Modelo.query.get(id)

    sigla = request.json['sigla']
    nome = request.json['nome']

    modelo.sigla = sigla
    modelo.nome = nome

    db.session.commit()

    return modelo_schema.jsonify(modelo)


# Delete Modelo
@app.route('/modelo/<id>', methods=['DELETE'])
def delete_modelo(id):
    modelo = Modelo.query.get(id)
    db.session.delete(modelo)
    db.session.commit()

    return modelo_schema.jsonify(modelo)


# Run Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
