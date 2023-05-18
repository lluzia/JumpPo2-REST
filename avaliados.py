"""Define as funções : Ler, Criar, Atualizar e Excluir avaliados na tabela."""

from flask import abort, make_response
from config import db
from models import Avaliado, Usuario, avaliado_schema, AvaliadoSchema


def read_all():
    """
    Lista todos os avaliados cadastrados na tabela
    :return: Lista de avaliados
    """
    avaliados = Avaliado.query.all()
    avaliado_schema = AvaliadoSchema(many=True)
    return avaliado_schema.dump(avaliados)


def read_one(avaliado_id):
    """
    Lista um avaliado específico da tabela
    :param avaliado_id: id do avaliado a ser buscado na tabela.
    :return: avaliado existente conforme ID ou aborta a função caso avaliado inexistente.
    """
    avaliado = Avaliado.query.get(avaliado_id)

    if avaliado is not None:
        return avaliado_schema.dump(avaliado)
    else:
        abort(404, "Avaliado com ID {avaliado_id} não encontrado")


def update(avaliado_id, avaliado):
    """
    Atualiza avaliado já registrado.
    :param avaliado_id: id do avaliado a ser buscado na tabela
    :param avaliado: object do referido avaliado
    :return: atributos do avaliado a ser alterado ou aborta a função caso avaliado inexistente.
    """
    avaliado_existe = Avaliado.query.get(avaliado_id)

    if avaliado_existe:
        avaliado_a_atualizar = avaliado_schema.load(avaliado, session=db.session)
        avaliado_existe.nome = avaliado_a_atualizar.nome
        avaliado_existe.sobrenome = avaliado_a_atualizar.sobrenome
        avaliado_existe.sexo = avaliado_a_atualizar.sexo
        avaliado_existe.peso = avaliado_a_atualizar.peso
        avaliado_existe.perna_flexionada = avaliado_a_atualizar.perna_flexionada
        avaliado_existe.estendida = avaliado_a_atualizar.perna_estendida
        db.session.merge(avaliado_existe)
        db.session.commit()
        return avaliado_schema.dump(avaliado_existe), 201
    else:
        abort(404, "Avaliado com ID {avaliado_id} não encontrado")


def delete(avaliado_id):
    """
    Exclui avaliado já registrado.
    :param avaliado_id: id do avaliado a ser excluído da tabela
    """
    avaliado_existe = Avaliado.query.get(avaliado_id)

    if avaliado_existe:
        db.session.delete(avaliado_existe)
        db.session.commit()
        return make_response("{avaliado_id} excluído com sucesso", 204)
    else:
        abort(404, "Avaliado com ID {avaliado_id} não encontrado")


def create(avaliado, usuario_atual):
    """
    Inclui avaliado na tabela.
    :param avaliado: object avaliado
    :param usuario_atual: refere-se ao usuario ao qual o avaliado pertence ou aborta função caso o usuario não exista.
    """
    usuario_id = usuario_atual
    usuario = Usuario.query.filter(Usuario.id == usuario_id).one_or_none()

    if usuario:
        novo_avaliado = avaliado_schema.load(avaliado, session=db.session)
        usuario.avaliados.append(novo_avaliado)
        db.session.commit()
        return avaliado_schema.dump(novo_avaliado), 201
    else:
        abort(404, "Usuario {usuario_id} não encontrado")
