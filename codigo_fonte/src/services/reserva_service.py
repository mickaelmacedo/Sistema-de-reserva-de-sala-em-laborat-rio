# src/services/reserva_service.py
from datetime import datetime
from src.models.reserva import Reserva
from src.models.usuario import Usuario
from src.models.laboratorio import Laboratorio
from src.repositories.reserva_repository import ReservaRepository


class ReservaService:
    def __init__(self, repository: ReservaRepository):
        self.repository = repository

    def solicitar_agendamento(
        self, professor: Usuario, laboratorio: Laboratorio,
        inicio: datetime, fim: datetime
    ) -> Reserva:
        self._validar_permissao_professor(professor)
        self._validar_periodo(inicio, fim)

        nova_reserva = Reserva(
            id=self.repository.proximo_id(),
            usuario=professor,
            laboratorio=laboratorio,
            data_inicio=inicio,
            data_fim=fim,
            status="pendente"
        )
        self.repository.salvar(nova_reserva)
        return nova_reserva

    def aprovar_solicitacao(self, admin: Usuario, reserva_id: int) -> Reserva:
        self._validar_permissao_admin(admin)
        reserva = self._buscar_pendente(reserva_id)

        self._validar_conflito(reserva)

        reserva.status = "aprovada"
        reserva.aprovado_por = admin
        self.repository.atualizar(reserva)
        return reserva

    def rejeitar_solicitacao(self, admin: Usuario, reserva_id: int, motivo: str) -> Reserva:
        self._validar_permissao_admin(admin)
        if not motivo or not motivo.strip():
            raise ValueError("É necessário informar o motivo da rejeição.")

        reserva = self._buscar_pendente(reserva_id)

        reserva.status = "rejeitada"
        reserva.aprovado_por = admin
        reserva.motivo_rejeicao = motivo.strip()
        self.repository.atualizar(reserva)
        return reserva

    def cancelar_reserva(self, admin: Usuario, reserva_id: int) -> Reserva:
        self._validar_permissao_admin(admin)
        reserva = self.repository.buscar_por_id(reserva_id)

        if not reserva:
            raise ValueError(f"Reserva com id {reserva_id} não encontrada.")
        if reserva.status == "cancelada":
            raise ValueError(f"A reserva {reserva_id} já está cancelada.")
        if reserva.status not in ("pendente", "aprovada"):
            raise ValueError(f"Não é possível cancelar uma reserva com status '{reserva.status}'.")

        reserva.status = "cancelada"
        self.repository.atualizar(reserva)
        return reserva

    def listar_solicitacoes_pendentes(self) -> list[Reserva]:
        return self.repository.listar_por_status("pendente")

    def _buscar_pendente(self, reserva_id: int) -> Reserva:
        reserva = self.repository.buscar_por_id(reserva_id)
        if not reserva:
            raise ValueError(f"Reserva com id {reserva_id} não encontrada.")
        if reserva.status != "pendente":
            raise ValueError(f"A reserva {reserva_id} já foi processada (status atual: '{reserva.status}').")
        return reserva

    def _validar_permissao_professor(self, usuario: Usuario) -> None:
        if usuario.tipo not in ("professor", "admin"):
            raise ValueError("Apenas professores podem solicitar agendamento de laboratório.")

    def _validar_permissao_admin(self, usuario: Usuario) -> None:
        if usuario.tipo != "admin":
            raise ValueError("Apenas administradores podem realizar esta ação.")

    def _validar_periodo(self, inicio: datetime, fim: datetime) -> None:
        if inicio >= fim:
            raise ValueError("A data de início deve ser anterior à data de término.")
        if inicio < datetime.now():
            raise ValueError("Não é possível solicitar agendamento em horários passados.")

    def _validar_conflito(self, reserva: Reserva) -> None:
        reservas_aprovadas = [
            r for r in self.repository.listar_por_laboratorio(reserva.laboratorio.id)
            if r.status == "aprovada" and r.id != reserva.id
        ]
        for outra in reservas_aprovadas:
            if reserva.conflita_com(outra):
                raise ValueError(
                    f"Conflito de horário: o laboratório '{reserva.laboratorio.nome}' "
                    f"já está aprovado para outro período que se sobrepõe a este."
                )