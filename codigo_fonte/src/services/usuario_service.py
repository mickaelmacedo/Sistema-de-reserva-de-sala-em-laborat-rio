# src/services/usuario_service.py
import re
from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository

TIPOS_VALIDOS = ("aluno", "professor", "admin")


class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def cadastrar_usuario(self, nome: str, email: str, tipo: str) -> Usuario:
        self._validar_nome(nome)
        self._validar_email(email)
        self._validar_tipo(tipo)

        email_normalizado = email.strip().lower()
        ja_existe = any(
            usuario.email.lower() == email_normalizado
            for usuario in self.repository.listar_todos()
        )
        if ja_existe:
            raise ValueError(f"Já existe um usuário cadastrado com o e-mail '{email}'.")

        novo_usuario = Usuario(
            id=self.repository.proximo_id(),
            nome=nome.strip(),
            email=email_normalizado,
            tipo=tipo
        )
        self.repository.salvar(novo_usuario)
        return novo_usuario

    def listar_todos(self) -> list[Usuario]:
        return self.repository.listar_todos()

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome do usuário não pode ser vazio.")

    def _validar_email(self, email: str) -> None:
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(padrao, email.strip()):
            raise ValueError(f"E-mail inválido: '{email}'.")

    def _validar_tipo(self, tipo: str) -> None:
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo de usuário inválido: '{tipo}'. Use um dos: {TIPOS_VALIDOS}.")