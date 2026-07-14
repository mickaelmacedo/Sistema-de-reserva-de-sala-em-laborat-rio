# src/main.py
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.laboratorio_repository import LaboratorioRepository
from src.repositories.reserva_repository import ReservaRepository
from src.services.usuario_service import UsuarioService
from src.services.laboratorio_service import LaboratorioService
from src.services.reserva_service import ReservaService
from src.views.menu import Menu


def main() -> None:
    usuario_repository = UsuarioRepository()
    laboratorio_repository = LaboratorioRepository()
    reserva_repository = ReservaRepository(
        usuario_repository=usuario_repository,
        laboratorio_repository=laboratorio_repository
    )

    usuario_service = UsuarioService(usuario_repository)
    laboratorio_service = LaboratorioService(laboratorio_repository)
    reserva_service = ReservaService(reserva_repository)

    menu = Menu(usuario_repository, usuario_service, laboratorio_service, reserva_service)
    menu.iniciar()


if __name__ == "__main__":
    main()