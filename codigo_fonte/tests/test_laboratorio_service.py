import pytest

from src.services.laboratorio_service import LaboratorioService


class FakeLaboratorioRepository:

    def __init__(self):
        self.laboratorios = []

    def proximo_id(self):
        return len(self.laboratorios) + 1

    def salvar(self, laboratorio):
        self.laboratorios.append(laboratorio)

    def listar_todos(self):
        return self.laboratorios

    def buscar_por_id(self, id):
        for lab in self.laboratorios:
            if lab.id == id:
                return lab
        return None

    def remover(self, id):
        self.laboratorios = [
            l for l in self.laboratorios
            if l.id != id
        ]


@pytest.fixture
def service():
    return LaboratorioService(FakeLaboratorioRepository())


def test_cadastrar_laboratorio(service):
    lab = service.cadastrar_laboratorio(
        "Lab Redes",
        30
    )

    assert lab.nome == "Lab Redes"
    assert lab.capacidade == 30


def test_capacidade_invalida(service):
    with pytest.raises(ValueError):
        service.cadastrar_laboratorio(
            "Lab",
            0
        )


def test_buscar_laboratorio(service):
    lab = service.cadastrar_laboratorio(
        "Lab IA",
        20
    )

    encontrado = service.buscar_por_id(lab.id)

    assert encontrado.id == lab.id


def test_remover_laboratorio(service):
    lab = service.cadastrar_laboratorio(
        "Lab BD",
        25
    )

    service.remover_laboratorio(lab.id)

    assert len(service.listar_todos()) == 0