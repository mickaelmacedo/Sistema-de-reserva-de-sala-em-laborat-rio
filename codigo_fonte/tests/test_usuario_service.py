import pytest

from src.services.usuario_service import UsuarioService


class FakeUsuarioRepository:
    def __init__(self):
        self.usuarios = []

    def proximo_id(self):
        return len(self.usuarios) + 1

    def salvar(self, usuario):
        self.usuarios.append(usuario)

    def listar_todos(self):
        return self.usuarios


@pytest.fixture
def service():
    return UsuarioService(FakeUsuarioRepository())


def test_cadastrar_usuario():
    service = UsuarioService(FakeUsuarioRepository())

    usuario = service.cadastrar_usuario(
        "João",
        "joao@email.com",
        "professor"
    )

    assert usuario.id == 1
    assert usuario.nome == "João"
    assert usuario.email == "joao@email.com"
    assert usuario.tipo == "professor"


def test_email_duplicado():
    service = UsuarioService(FakeUsuarioRepository())

    service.cadastrar_usuario(
        "João",
        "joao@email.com",
        "professor"
    )

    with pytest.raises(ValueError):
        service.cadastrar_usuario(
            "Maria",
            "joao@email.com",
            "professor"
        )


def test_email_invalido():
    service = UsuarioService(FakeUsuarioRepository())

    with pytest.raises(ValueError):
        service.cadastrar_usuario(
            "João",
            "email",
            "professor"
        )