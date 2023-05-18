"""To Test Only"""


from datetime import datetime

from config import app, db
from models import Avaliado, Usuario

AVALIADOS_TREINADOS = [
    {
        "email": "ana@mail.com",
        "nome": "Ana",
        "sobrenome": "Silva",
        "senha": "1234",
        "avaliados":
            [
            ("Carla", "Andrade", "fem", "12.8", "77", "79.8", True, "2022-01-06 17:10:24"),
            ],
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in AVALIADOS_TREINADOS:
        novo_usuario = Usuario(email=data.get("email"),
                               nome=data.get("nome"),
                               sobrenome=data.get("sobrenome"),
                               senha=data.get("senha"))
        for nome, sobrenome, sexo, peso, perna_flexionada, perna_estendida, ativo, timestamp in data.get("avaliados",
                                                                                                         []):
            novo_usuario.avaliados.append(
                Avaliado(
                    nome=nome,
                    sobrenome=sobrenome,
                    sexo=sexo,
                    peso=peso,
                    perna_flexionada=perna_flexionada,
                    perna_estendida=perna_estendida,
                    ativo=ativo,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                ),
            )

        db.session.add(novo_usuario)
    db.session.commit()
