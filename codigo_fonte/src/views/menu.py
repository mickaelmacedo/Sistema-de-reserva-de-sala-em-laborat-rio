# src/views/menu.py
from datetime import datetime
from src.repositories.usuario_repository import UsuarioRepository
from src.services.usuario_service import UsuarioService
from src.services.laboratorio_service import LaboratorioService
from src.services.reserva_service import ReservaService

FORMATO_DATA_HORA = "%d/%m/%Y %H:%M"


class Menu:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        usuario_service: UsuarioService,
        laboratorio_service: LaboratorioService,
        reserva_service: ReservaService
    ):
        self.usuario_repository = usuario_repository
        self.usuario_service = usuario_service
        self.laboratorio_service = laboratorio_service
        self.reserva_service = reserva_service

    def _buscar_usuario(self, usuario_id: int):
        usuario = self.usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário com id {usuario_id} não encontrado.")
        return usuario

    def iniciar(self) -> None:
        while True:
            self._exibir_menu_principal()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self._menu_usuarios()
            elif opcao == "2":
                self._menu_laboratorios()
            elif opcao == "3":
                self._menu_reservas()
            elif opcao == "0":
                print("\nEncerrando o sistema. Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")

    def _exibir_menu_principal(self) -> None:
        print("\n" + "=" * 40)
        print("SISTEMA DE RESERVA DE LABORATÓRIOS")
        print("=" * 40)
        print("1. Usuários")
        print("2. Laboratórios")
        print("3. Reservas")
        print("0. Sair")

    # ---------- USUÁRIOS ----------

    def _menu_usuarios(self) -> None:
        while True:
            print("\n--- USUÁRIOS ---")
            print("1. Cadastrar usuário")
            print("2. Listar usuários")
            print("0. Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self._cadastrar_usuario()
            elif opcao == "2":
                self._listar_usuarios()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida.")

    def _cadastrar_usuario(self) -> None:
        try:
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            tipo = input("Tipo (aluno/professor/admin): ").strip()

            usuario = self.usuario_service.cadastrar_usuario(nome, email, tipo)
            print(f"\nUsuário cadastrado com sucesso! ID: {usuario.id}")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _listar_usuarios(self) -> None:
        usuarios = self.usuario_service.listar_todos()
        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return

        print("\n--- LISTA DE USUÁRIOS ---")
        for usuario in usuarios:
            print(f"[{usuario.id}] {usuario.nome} - {usuario.email} ({usuario.tipo})")

    # ---------- LABORATÓRIOS ----------

    def _menu_laboratorios(self) -> None:
        while True:
            print("\n--- LABORATÓRIOS ---")
            print("1. Cadastrar laboratório")
            print("2. Listar laboratórios")
            print("3. Remover laboratório")
            print("0. Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self._cadastrar_laboratorio()
            elif opcao == "2":
                self._listar_laboratorios()
            elif opcao == "3":
                self._remover_laboratorio()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida.")

    def _cadastrar_laboratorio(self) -> None:
        try:
            nome = input("Nome do laboratório: ").strip()
            capacidade = int(input("Capacidade: ").strip())
            recursos_texto = input("Recursos (separados por vírgula, opcional): ").strip()
            recursos = [r.strip() for r in recursos_texto.split(",")] if recursos_texto else []

            laboratorio = self.laboratorio_service.cadastrar_laboratorio(nome, capacidade, recursos)
            print(f"\nLaboratório cadastrado com sucesso! ID: {laboratorio.id}")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _listar_laboratorios(self) -> None:
        laboratorios = self.laboratorio_service.listar_todos()
        if not laboratorios:
            print("\nNenhum laboratório cadastrado.")
            return

        print("\n--- LISTA DE LABORATÓRIOS ---")
        for laboratorio in laboratorios:
            recursos = ", ".join(laboratorio.recursos) if laboratorio.recursos else "nenhum"
            print(f"[{laboratorio.id}] {laboratorio.nome} - capacidade: {laboratorio.capacidade} - recursos: {recursos}")

    def _remover_laboratorio(self) -> None:
        try:
            laboratorio_id = int(input("ID do laboratório a remover: ").strip())
            self.laboratorio_service.remover_laboratorio(laboratorio_id)
            print("\nLaboratório removido com sucesso!")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    # ---------- RESERVAS ----------

    def _menu_reservas(self) -> None:
        while True:
            print("\n--- RESERVAS ---")
            print("1. Solicitar agendamento (professor)")
            print("2. Listar solicitações pendentes")
            print("3. Aprovar solicitação (admin)")
            print("4. Rejeitar solicitação (admin)")
            print("5. Cancelar reserva (admin)")
            print("0. Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self._solicitar_agendamento()
            elif opcao == "2":
                self._listar_pendentes()
            elif opcao == "3":
                self._aprovar_solicitacao()
            elif opcao == "4":
                self._rejeitar_solicitacao()
            elif opcao == "5":
                self._cancelar_reserva()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida.")

    def _solicitar_agendamento(self) -> None:
        try:
            professor_id = int(input("ID do professor solicitante: ").strip())
            laboratorio_id = int(input("ID do laboratório: ").strip())
            inicio_texto = input("Data/hora de início (dd/mm/aaaa hh:mm): ").strip()
            fim_texto = input("Data/hora de término (dd/mm/aaaa hh:mm): ").strip()

            professor = self._buscar_usuario(professor_id)
            laboratorio = self.laboratorio_service.buscar_por_id(laboratorio_id)
            inicio = datetime.strptime(inicio_texto, FORMATO_DATA_HORA)
            fim = datetime.strptime(fim_texto, FORMATO_DATA_HORA)

            reserva = self.reserva_service.solicitar_agendamento(professor, laboratorio, inicio, fim)
            print(f"\nSolicitação registrada com sucesso! ID: {reserva.id} (status: {reserva.status})")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _listar_pendentes(self) -> None:
        pendentes = self.reserva_service.listar_solicitacoes_pendentes()
        if not pendentes:
            print("\nNenhuma solicitação pendente.")
            return

        print("\n--- SOLICITAÇÕES PENDENTES ---")
        for reserva in pendentes:
            self._exibir_reserva(reserva)

    def _aprovar_solicitacao(self) -> None:
        try:
            admin_id = int(input("ID do administrador: ").strip())
            reserva_id = int(input("ID da solicitação a aprovar: ").strip())

            admin = self._buscar_usuario(admin_id)
            reserva = self.reserva_service.aprovar_solicitacao(admin, reserva_id)
            print(f"\nSolicitação {reserva.id} aprovada com sucesso!")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _rejeitar_solicitacao(self) -> None:
        try:
            admin_id = int(input("ID do administrador: ").strip())
            reserva_id = int(input("ID da solicitação a rejeitar: ").strip())
            motivo = input("Motivo da rejeição: ").strip()

            admin = self._buscar_usuario(admin_id)
            reserva = self.reserva_service.rejeitar_solicitacao(admin, reserva_id, motivo)
            print(f"\nSolicitação {reserva.id} rejeitada. Motivo: {reserva.motivo_rejeicao}")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _cancelar_reserva(self) -> None:
        try:
            admin_id = int(input("ID do administrador: ").strip())
            reserva_id = int(input("ID da reserva a cancelar: ").strip())

            admin = self._buscar_usuario(admin_id)
            self.reserva_service.cancelar_reserva(admin, reserva_id)
            print("\nReserva cancelada com sucesso!")
        except ValueError as erro:
            print(f"\nErro: {erro}")

    def _exibir_reserva(self, reserva) -> None:
        inicio = reserva.data_inicio.strftime(FORMATO_DATA_HORA)
        fim = reserva.data_fim.strftime(FORMATO_DATA_HORA)
        print(
            f"[{reserva.id}] {reserva.laboratorio.nome} | prof. {reserva.usuario.nome} | "
            f"{inicio} - {fim} | status: {reserva.status}"
        )