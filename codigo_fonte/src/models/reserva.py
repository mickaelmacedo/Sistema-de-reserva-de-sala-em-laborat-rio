# src/models/reserva.py
from datetime import datetime
from src.models.usuario import Usuario
from src.models.laboratorio import Laboratorio

class Reserva:
    def __init__(self, id: int, usuario: Usuario, laboratorio: Laboratorio,
                 data_inicio: datetime, data_fim: datetime, status: str = "confirmada"):
        self.id = id
        self.usuario = usuario
        self.laboratorio = laboratorio
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status

    def conflita_com(self, outra: "Reserva") -> bool:
        if self.laboratorio.id != outra.laboratorio.id:
            return False
        return self.data_inicio < outra.data_fim and outra.data_inicio < self.data_fim