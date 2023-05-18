"""Define as funções : Ler, Criar, Atualizar e Excluir Treinador/Usuário na tabela."""

from flask import abort, make_response

from config import db
from models import Usuario, usuarios_schema, usuario_schema, UsuarioSchema


def read_all():
    """
    Lista todos os usuário cadastrados na tabela
    :return: Lista de avaliados
    """
    usuarios = Usuario.query.all()
    usuario_schema = UsuarioSchema(many=True)
    return usuario_schema.dump(usuarios)


def create(usuario):
    """
    Inclui avaliado na tabela.
    :param usuario: object avaliado
    """
    email = usuario.get("email")
    usuario_existe = Usuario.query.filter(Usuario.email == email).one_or_none()

    if usuario_existe is None:
        novo_usuario = usuario_schema.load(usuario, session=db.session)
        db.session.add(novo_usuario)
        db.session.commit()
        return usuario_schema.dump(novo_usuario), 201
    else:
        abort(406, "Usuário com email: {email} já está cadastrado")


def read_one(email):
    """
    Lista um usuário específico da tabela
    :param email: e-mail do usuário a ser buscado na tabela.
    :return: usuário existente conforme e-mail ou aborta a função caso usuário inexistente.
    """
    usuario = Usuario.query.filter(Usuario.email == email).one_or_none()
    if usuario is not None:
        return usuario_schema.dump(usuario)
    else:
        abort(404, f"Usuário com email : {email} não foi encontrado")


def update(email, usuario):
    """
    Atualiza usuário já registrado.
    :param email: e-mail do usuário a ser buscado na tabela
    :param usuario: object do referido usuário
    :return: atributos do usuário a ser alterado ou aborta a função caso usuário inexistente.
    """
    usuario_existe = Usuario.query.filter(Usuario.email == email).one_or_none()

    if usuario_existe:
        usuario_a_autualizar = usuario_schema.load(usuario, session=db.session)
        usuario_existe.nome = usuario_a_autualizar.nome
        usuario_existe.sobrenome = usuario_a_autualizar.sobrenome
        usuario_existe.senha = usuario_a_autualizar.senha
        db.session.merge(usuario_existe)
        db.session.commit()
        return usuario_schema.dump(usuario_existe), 201
    else:
        abort(404, " Usuário com e-mail: {email} não encontrado")


def delete(email):
    """
    Exclui usuário já registrado.
    :param email: e-mail do usuário a ser excluído da tabela
    """
    usuario_existe = Usuario.query.filter(Usuario.email == email).one_or_none()

    if usuario_existe:
        db.session.delete(usuario_existe)
        db.session.commit()
        return make_response("Usuário: {email} excluido com sucesso", 200)
    else:
        abort(404, " Usuário com e-mail: {email} não encontrado")
