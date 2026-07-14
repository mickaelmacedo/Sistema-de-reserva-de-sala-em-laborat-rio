# src/repositories/base_repository.py
import json
import os
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self._garantir_arquivo()

    def _garantir_arquivo(self) -> None:
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
        if not os.path.exists(self.caminho_arquivo):
            self._salvar_dados([])

    def _carregar_dados(self) -> list[dict]:
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def _salvar_dados(self, dados: list[dict]) -> None:
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)

    def proximo_id(self) -> int:
        dados = self._carregar_dados()
        if not dados:
            return 1
        return max(item["id"] for item in dados) + 1

    @abstractmethod
    def _para_dict(self, objeto) -> dict:
        ...

    @abstractmethod
    def _para_objeto(self, dado: dict):
        ...