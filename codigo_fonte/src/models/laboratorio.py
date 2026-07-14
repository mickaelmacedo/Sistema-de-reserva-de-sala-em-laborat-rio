# src/models/laboratorio.py
class Laboratorio:
    def __init__(self, id: int, nome: str, capacidade: int, recursos: list[str] = None):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.recursos = recursos or []

    def __repr__(self):
        return f"Laboratorio({self.nome}, capacidade={self.capacidade})"