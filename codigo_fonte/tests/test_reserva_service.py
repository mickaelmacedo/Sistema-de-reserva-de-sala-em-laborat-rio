# tests/test_reserva_service.py
import pytest
from datetime import datetime, timedelta
from src.models.usuario import Usuario
from src.models.laboratorio import Laboratorio
from src.models.reserva import Reserva
from src.services.reserva_service import ReservaService


class ReservaRepositoryFake:
    def __init__(self):
        self._reservas = []
        self._proximo_id = 1

    def proximo_id(self) -> int:
        return self._proximo_id

    def salvar(self, reserva: Reserva) -> None:
        self._reservas.append(reserva)
        self._proximo_id += 1

    def atualizar(self, reserva: Reserva) -> None:
        for i, r in enumerate(self._reservas):
            if r.id == reserva.id:
                self._reservas[i] = reserva
                return

    def buscar_por_id(self, reserva_id: int):
        for r in self._reservas:
            if r.id == reserva_id:
                return r
        return None

    def listar_por_laboratorio(self, laboratorio_id: int) -> list[Reserva]:
        return [r for r in self._reservas if r.laboratorio.id == laboratorio_id]

    def listar_por_status(self, status: str) -> list[Reserva]:
        return [r for r in self._reservas if r.status == status]

    def listar_todos(self) -> list[Reserva]:
        return self._reservas


@pytest.fixture
def repository():
    return ReservaRepositoryFake()


@pytest.fixture
def service(repository):
    return ReservaService(repository)


@pytest.fixture
def professor():
    return Usuario(id=1, nome="Ana Silva", email="ana@exemplo.com", tipo="professor")


@pytest.fixture
def outro_professor():
    return Usuario(id=2, nome="Bruno Costa", email="bruno@exemplo.com", tipo="professor")


@pytest.fixture
def admin():
    return Usuario(id=3, nome="Carla Souza", email="carla@exemplo.com", tipo="admin")


@pytest.fixture
def aluno():
    return Usuario(id=4, nome="Davi Lima", email="davi@exemplo.com", tipo="aluno")


@pytest.fixture
def laboratorio():
    return Laboratorio(id=1, nome="Lab de Redes", capacidade=20, recursos=["projetor"])


@pytest.fixture
def amanha_14h():
    amanha = datetime.now() + timedelta(days=1)
    return amanha.replace(hour=14, minute=0, second=0, microsecond=0)


class TestSolicitarAgendamento:
    def test_professor_solicita_com_sucesso(self, service, professor, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=2)

        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        assert reserva.id == 1
        assert reserva.status == "pendente"
        assert reserva.professor == professor

    def test_aluno_nao_pode_solicitar(self, service, aluno, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)

        with pytest.raises(ValueError, match="Apenas professores"):
            service.solicitar_agendamento(aluno, laboratorio, amanha_14h, fim)

    def test_nao_permite_data_inicio_maior_que_fim(self, service, professor, laboratorio, amanha_14h):
        fim = amanha_14h - timedelta(hours=1)

        with pytest.raises(ValueError, match="anterior à data de término"):
            service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

    def test_nao_permite_solicitacao_no_passado(self, service, professor, laboratorio):
        ontem = datetime.now() - timedelta(days=1)
        fim = ontem + timedelta(hours=1)

        with pytest.raises(ValueError, match="horários passados"):
            service.solicitar_agendamento(professor, laboratorio, ontem, fim)

    def test_permite_duas_solicitacoes_pendentes_no_mesmo_horario(
        self, service, professor, outro_professor, laboratorio, amanha_14h
    ):
        fim = amanha_14h + timedelta(hours=2)

        reserva1 = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)
        reserva2 = service.solicitar_agendamento(outro_professor, laboratorio, amanha_14h, fim)

        assert reserva1.status == "pendente"
        assert reserva2.status == "pendente"


class TestAprovarSolicitacao:
    def test_admin_aprova_com_sucesso(self, service, professor, admin, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        aprovada = service.aprovar_solicitacao(admin, reserva.id)

        assert aprovada.status == "aprovada"
        assert aprovada.aprovado_por == admin

    def test_professor_nao_pode_aprovar(self, service, professor, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        with pytest.raises(ValueError, match="Apenas administradores"):
            service.aprovar_solicitacao(professor, reserva.id)

    def test_nao_permite_aprovar_duas_solicitacoes_conflitantes(
        self, service, professor, outro_professor, admin, laboratorio, amanha_14h
    ):
        fim = amanha_14h + timedelta(hours=2)
        reserva1 = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)
        reserva2 = service.solicitar_agendamento(outro_professor, laboratorio, amanha_14h, fim)

        service.aprovar_solicitacao(admin, reserva1.id)

        with pytest.raises(ValueError, match="Conflito de horário"):
            service.aprovar_solicitacao(admin, reserva2.id)

    def test_nao_permite_aprovar_solicitacao_ja_processada(self, service, professor, admin, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)
        service.aprovar_solicitacao(admin, reserva.id)

        with pytest.raises(ValueError, match="já foi processada"):
            service.aprovar_solicitacao(admin, reserva.id)


class TestRejeitarSolicitacao:
    def test_admin_rejeita_com_sucesso(self, service, professor, admin, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        rejeitada = service.rejeitar_solicitacao(admin, reserva.id, "Laboratório em manutenção")

        assert rejeitada.status == "rejeitada"
        assert rejeitada.motivo_rejeicao == "Laboratório em manutenção"

    def test_exige_motivo_para_rejeitar(self, service, professor, admin, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        with pytest.raises(ValueError, match="motivo da rejeição"):
            service.rejeitar_solicitacao(admin, reserva.id, "")


class TestCancelarReserva:
    def test_admin_cancela_reserva_aprovada(self, service, professor, admin, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)
        service.aprovar_solicitacao(admin, reserva.id)

        cancelada = service.cancelar_reserva(admin, reserva.id)

        assert cancelada.status == "cancelada"

    def test_professor_nao_pode_cancelar(self, service, professor, laboratorio, amanha_14h):
        fim = amanha_14h + timedelta(hours=1)
        reserva = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim)

        with pytest.raises(ValueError, match="Apenas administradores"):
            service.cancelar_reserva(professor, reserva.id)


class TestListarPendentes:
    def test_lista_apenas_pendentes(self, service, professor, admin, laboratorio, amanha_14h):
        fim1 = amanha_14h + timedelta(hours=1)
        reserva1 = service.solicitar_agendamento(professor, laboratorio, amanha_14h, fim1)

        inicio2 = fim1
        fim2 = inicio2 + timedelta(hours=1)
        service.solicitar_agendamento(professor, laboratorio, inicio2, fim2)

        service.aprovar_solicitacao(admin, reserva1.id)
        pendentes = service.listar_solicitacoes_pendentes()

        assert len(pendentes) == 1
        assert pendentes[0].status == "pendente"
