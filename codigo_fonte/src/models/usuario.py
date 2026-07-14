# src/models/usuario.py
class Usuario:
    def __init__(self, id: int, nome: str, email: str, tipo: str = "aluno"):
        self.id = id
        self.nome = nome
        self.email = email
        self.tipo = tipo  # "aluno", "professor", "admin"

    def __repr__(self):
        return f"Usuario({self.nome}, {self.tipo})"