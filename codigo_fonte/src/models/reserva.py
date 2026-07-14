# src/models/reserva.py
from datetime import datetime
from src.models.usuario import Usuario
from src.models.laboratorio import Laboratorio

class Reserva:
    def __init__(self, id: int, usuario: Usuario, laboratorio: Laboratorio,
                 data_inicio: datetime, data_fim: datetime, status: str = "confirmada", aprovado_por: int = None, data_solicitacao: datetime = datetime.now(), motivo_rejeicao: str = None):
        self.id = id
        self.usuario = usuario
        self.laboratorio = laboratorio
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status
        self.aprovado_por = aprovado_por
        self.data_solicitacao = data_solicitacao
        self.motivo_rejeicao = motivo_rejeicao

    def conflita_com(self, outra: "Reserva") -> bool:
        if self.laboratorio.id != outra.laboratorio.id:
            return False
        return self.data_inicio < outra.data_fim and outra.data_inicio < self.data_fim