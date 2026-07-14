# src/repositories/laboratorio_repository.py
from src.models.laboratorio import Laboratorio
from src.repositories.base_repository import BaseRepository


class LaboratorioRepository(BaseRepository):
    def __init__(self, caminho_arquivo: str = "data/laboratorios.json"):
        super().__init__(caminho_arquivo)

    def salvar(self, laboratorio: Laboratorio) -> None:
        dados = self._carregar_dados()
        dados.append(self._para_dict(laboratorio))
        self._salvar_dados(dados)

    def atualizar(self, laboratorio: Laboratorio) -> None:
        dados = self._carregar_dados()
        for i, item in enumerate(dados):
            if item["id"] == laboratorio.id:
                dados[i] = self._para_dict(laboratorio)
                self._salvar_dados(dados)
                return
        raise ValueError(f"Laboratório com id {laboratorio.id} não encontrado para atualização.")

    def remover(self, laboratorio_id: int) -> None:
        dados = self._carregar_dados()
        dados_filtrados = [item for item in dados if item["id"] != laboratorio_id]
        if len(dados_filtrados) == len(dados):
            raise ValueError(f"Laboratório com id {laboratorio_id} não encontrado para remoção.")
        self._salvar_dados(dados_filtrados)

    def buscar_por_id(self, laboratorio_id: int) -> Laboratorio | None:
        dados = self._carregar_dados()
        for item in dados:
            if item["id"] == laboratorio_id:
                return self._para_objeto(item)
        return None

    def listar_todos(self) -> list[Laboratorio]:
        dados = self._carregar_dados()
        return [self._para_objeto(item) for item in dados]

    def _para_dict(self, laboratorio: Laboratorio) -> dict:
        return {
            "id": laboratorio.id,
            "nome": laboratorio.nome,
            "capacidade": laboratorio.capacidade,
            "recursos": laboratorio.recursos
        }

    def _para_objeto(self, dado: dict) -> Laboratorio:
        return Laboratorio(
            id=dado["id"],
            nome=dado["nome"],
            capacidade=dado["capacidade"],
            recursos=dado.get("recursos", [])
        )