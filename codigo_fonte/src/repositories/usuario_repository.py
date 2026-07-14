# src/repositories/usuario_repository.py
from src.models.usuario import Usuario
from src.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    def __init__(self, caminho_arquivo: str = "data/usuarios.json"):
        super().__init__(caminho_arquivo)

    def salvar(self, usuario: Usuario) -> None:
        dados = self._carregar_dados()
        dados.append(self._para_dict(usuario))
        self._salvar_dados(dados)

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        dados = self._carregar_dados()
        for item in dados:
            if item["id"] == usuario_id:
                return self._para_objeto(item)
        return None

    def listar_todos(self) -> list[Usuario]:
        dados = self._carregar_dados()
        return [self._para_objeto(item) for item in dados]

    def _para_dict(self, usuario: Usuario) -> dict:
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo
        }

    def _para_objeto(self, dado: dict) -> Usuario:
        return Usuario(
            id=dado["id"],
            nome=dado["nome"],
            email=dado["email"],
            tipo=dado["tipo"]
        )