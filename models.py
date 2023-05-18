"""
    Este arquivo define as classes a serem criadas para a tabela, bem como seus atributos e relações.
"""
from datetime import datetime
from marshmallow_sqlalchemy import fields
from config import db, ma


class Salto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avaliado_id = db.Column(db.Integer, db.ForeignKey('avaliado.id'))
    altura_salto = db.Column(db.Numeric(10, 2), nullable=False)
    tempo_voo = db.Column(db.Numeric(10, 2), nullable=False)
    forca_media = db.Column(db.Numeric(10, 2), nullable=False)
    potencia_media = db.Column(db.Numeric(10, 2), nullable=False)
    veloc_media = db.Column(db.Numeric(10, 2), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SaltoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Salto
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Avaliado(db.Model):
    __tablename__ = "avaliado"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    nome = db.Column(db.String, nullable=False)
    sobrenome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.String, nullable=False)
    peso = db.Column(db.Numeric(10, 2), nullable=False)
    perna_flexionada = db.Column(db.Numeric(10, 2), nullable=False)
    perna_estendida = db.Column(db.Numeric(10, 2), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    saltos = db.relationship(
        Salto,
        backref="avaliado",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Salto.timestamp)",
    )


class AvaliadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Avaliado
        load_instance = True
        sqla_session = db.session
        include_fk = True

        saltos = fields.Nested(SaltoSchema, many=True)


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    sobrenome = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    avaliados = db.relationship(
        Avaliado,
        backref="usuario",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Avaliado.timestamp)",
    )


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        sqla_session = db.session
        include_relationships = True

        avaliados = fields.Nested(AvaliadoSchema, many=True)


salto_schema = SaltoSchema()
avaliado_schema = AvaliadoSchema()
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
