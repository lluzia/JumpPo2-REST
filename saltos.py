"""Define as funções : Ler, Criar, Atualizar e Excluir saltos na tabela."""

from flask import abort, make_response

from config import db
from models import Salto, SaltoSchema, salto_schema, Avaliado


def read_all():
    """
    Lista todos os saltos cadastrados na tabela
    :return: Lista de saltos
    """
    saltos = Salto.query.all()
    salto_schema = SaltoSchema(many=True)
    return salto_schema.dump(saltos)


def create(salto, avaliado_atual):
    """
    Inclui avaliado na tabela.
    :param salto: object salto
    :param avaliado_atual: refere-se ao avaliado ao qual o salto pertence ou aborta função caso o avaliado não exista.
    """

    avaliado_id = avaliado_atual
    avaliador_existe = Avaliado.query.filter(Avaliado.id == avaliado_id).one_or_none()

    if avaliador_existe:
        novo_salto = salto_schema.load(salto, session=db.session)
        avaliador_existe.saltos.append(novo_salto)
        db.session.commit()
        return salto_schema.dump(novo_salto), 201
    else:
        abort(406, "Avaliador com id: {avaliador} não encontrado" )



def read_one(salto_id):
    """
    Lista um salto específico da tabela
    :param salto_id: id do salto a ser buscado na tabela.
    :return: salto existente conforme ID ou aborta a função caso salto inexistente.
    """
    salto = Salto.query.get(salto_id)

    if salto is not None:
        return salto_schema.dump(salto)
    else:
        abort(404, "Salto com ID {salto_id} não encontrado")


def update(salto_id, salto):
    """
    Atualiza salto já registrado.
    :param salto_id: id do salto a ser buscado na tabela
    :param salto: object do referido salto
    :return: atributos do salto a ser alterado ou aborta a função caso salto inexistente.
    """
    salto_existe = Salto.query.get(salto_id)

    if salto_existe:
        salto_a_atualizar = salto_schema.load(salto, session=db.session)
        salto_existe.altura_salto = salto_a_atualizar.altura_salto
        salto_existe.tempo_voo = salto_a_atualizar.tempo_voo
        salto_existe.forca_media = salto_a_atualizar.forca_media
        salto_existe.potencia_media = salto_a_atualizar.potencia_media
        salto_existe.veloc_media = salto_a_atualizar.veloc_media
        salto_existe.ativo = salto_a_atualizar.ativo
        db.session.merge(salto_existe)
        db.session.commit()
        return salto_schema.dump(salto_existe), 201
    else:
        abort(404, f"Salto com ID {salto_id} não encontrado")


def delete(salto_id):
    """
    Exclui salto já registrado.
    :param salto_id: id do salto a ser excluído da tabela
    """
    salto_existe = Salto.query.get(salto_id)

    if salto_existe:
        db.session.delete(salto_existe)
        db.session.commit()
        return make_response("{salto_id} excluído com sucesso", 204)
    else:
        abort(404, f"Salto com ID {salto_id} não encontrado")
