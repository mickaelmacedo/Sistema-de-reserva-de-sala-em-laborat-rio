# src/services/laboratorio_service.py
from src.models.laboratorio import Laboratorio
from src.repositories.laboratorio_repository import LaboratorioRepository


class LaboratorioService:
    def __init__(self, repository: LaboratorioRepository):
        self.repository = repository

    def cadastrar_laboratorio(self, nome: str, capacidade: int, recursos: list[str] = None) -> Laboratorio:
        self._validar_nome(nome)
        self._validar_capacidade(capacidade)

        novo_laboratorio = Laboratorio(
            id=self.repository.proximo_id(),
            nome=nome.strip(),
            capacidade=capacidade,
            recursos=recursos or []
        )
        self.repository.salvar(novo_laboratorio)
        return novo_laboratorio

    def buscar_por_id(self, laboratorio_id: int) -> Laboratorio:
        laboratorio = self.repository.buscar_por_id(laboratorio_id)
        if not laboratorio:
            raise ValueError(f"Laboratório com id {laboratorio_id} não encontrado.")
        return laboratorio

    def listar_todos(self) -> list[Laboratorio]:
        return self.repository.listar_todos()

    def remover_laboratorio(self, laboratorio_id: int) -> None:
        self.buscar_por_id(laboratorio_id)
        self.repository.remover(laboratorio_id)

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome do laboratório não pode ser vazio.")

    def _validar_capacidade(self, capacidade: int) -> None:
        if capacidade <= 0:
            raise ValueError("A capacidade do laboratório deve ser maior que zero.")