"""Esta applicação cria ambiente back-end em Python onde efetua operações
 de leitura, criação, atualização e exclusão em tabela relacional"""
# app.py

from flask import render_template
from models import Usuario
import config
import usuarios

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    """
    Rota inicial
    :return: Página em formato html
    """
    todos_usuarios = usuarios.read_all()
    return render_template("index.html", todos_usuarios=todos_usuarios)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
