# src/repositories/reserva_repository.py
from datetime import datetime
from src.models.reserva import Reserva
from src.repositories.base_repository import BaseRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.laboratorio_repository import LaboratorioRepository

FORMATO_DATA = "%Y-%m-%dT%H:%M:%S"


class ReservaRepository(BaseRepository):
    def __init__(
        self,
        caminho_arquivo: str = "data/reservas.json",
        usuario_repository: UsuarioRepository = None,
        laboratorio_repository: LaboratorioRepository = None
    ):
        super().__init__(caminho_arquivo)
        self.usuario_repository = usuario_repository or UsuarioRepository()
        self.laboratorio_repository = laboratorio_repository or LaboratorioRepository()

    def salvar(self, reserva: Reserva) -> None:
        dados = self._carregar_dados()
        dados.append(self._para_dict(reserva))
        self._salvar_dados(dados)

    def atualizar(self, reserva: Reserva) -> None:
        dados = self._carregar_dados()
        for i, item in enumerate(dados):
            if item["id"] == reserva.id:
                dados[i] = self._para_dict(reserva)
                self._salvar_dados(dados)
                return
        raise ValueError(f"Reserva com id {reserva.id} não encontrada para atualização.")

    def buscar_por_id(self, reserva_id: int) -> Reserva | None:
        dados = self._carregar_dados()
        for item in dados:
            if item["id"] == reserva_id:
                return self._para_objeto(item)
        return None

    def listar_por_laboratorio(self, laboratorio_id: int) -> list[Reserva]:
        dados = self._carregar_dados()
        return [
            self._para_objeto(item) for item in dados
            if item["laboratorio_id"] == laboratorio_id
        ]

    def listar_por_status(self, status: str) -> list[Reserva]:
        dados = self._carregar_dados()
        return [
            self._para_objeto(item) for item in dados
            if item["status"] == status
        ]

    def listar_todos(self) -> list[Reserva]:
        dados = self._carregar_dados()
        return [self._para_objeto(item) for item in dados]

    def _para_dict(self, reserva: Reserva) -> dict:
        return {
            "id": reserva.id,
            "usuario_id": reserva.usuario.id,
            "laboratorio_id": reserva.laboratorio.id,
            "data_inicio": reserva.data_inicio.strftime(FORMATO_DATA),
            "data_fim": reserva.data_fim.strftime(FORMATO_DATA),
            "status": reserva.status,
            "aprovado_por_id": reserva.aprovado_por.id if reserva.aprovado_por else None,
            "data_solicitacao": reserva.data_solicitacao.strftime(FORMATO_DATA),
            "motivo_rejeicao": reserva.motivo_rejeicao
        }

    def _para_objeto(self, dado: dict) -> Reserva:
        usuario = self.usuario_repository.buscar_por_id(dado["usuario_id"])
        laboratorio = self.laboratorio_repository.buscar_por_id(dado["laboratorio_id"])

        if usuario is None:
            raise ValueError(f"Usuário com id {dado['usuario_id']} referenciado na reserva não existe mais.")
        if laboratorio is None:
            raise ValueError(f"Laboratório com id {dado['laboratorio_id']} referenciado na reserva não existe mais.")

        aprovado_por = None
        if dado.get("aprovado_por_id") is not None:
            aprovado_por = self.usuario_repository.buscar_por_id(dado["aprovado_por_id"])

        return Reserva(
            id=dado["id"],
            usuario=usuario,
            laboratorio=laboratorio,
            data_inicio=datetime.strptime(dado["data_inicio"], FORMATO_DATA),
            data_fim=datetime.strptime(dado["data_fim"], FORMATO_DATA),
            status=dado["status"],
            aprovado_por=aprovado_por,
            data_solicitacao=datetime.strptime(dado["data_solicitacao"], FORMATO_DATA),
            motivo_rejeicao=dado.get("motivo_rejeicao")
        )