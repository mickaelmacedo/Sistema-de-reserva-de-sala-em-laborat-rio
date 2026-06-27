from datetime import datetime


class Reserva:

    def __init__(self, data_hora: datetime, motivo: str, status: str):
        self.__data_hora = data_hora
        self.__motivo = motivo
        self.__status = status
        self.__laboratorio = None

    # Getters
    def get_data_hora(self):
        return self.__data_hora

    def get_motivo(self):
        return self.__motivo

    def get_status(self):
        return self.__status

    def get_laboratorio(self):
        return self.__laboratorio

    # Setters
    def set_data_hora(self, data_hora):
        self.__data_hora = data_hora

    def set_motivo(self, motivo):
        self.__motivo = motivo

    def set_status(self, status):
        self.__status = status

    def set_laboratorio(self, laboratorio):
        self.__laboratorio = laboratorio

    # Método de negócio
    def fazer_checkin(self):
        if self.__laboratorio is None or not self.__laboratorio.get_is_ativo():
            print("Não foi possível fazer check-in. O laboratório está desativado.")
            return False

        if self.__status == "APROVADA":
            self.__status = "EM_USO"
            print("Check-in realizado com sucesso!")
            return True

        elif self.__status == "PENDENTE":
            print("Não foi possível fazer check-in. A reserva ainda está pendente de aprovação.")

        elif self.__status == "REJEITADA":
            print("Não foi possível fazer check-in. A reserva foi rejeitada.")

        elif self.__status == "CANCELADA":
            print("Não foi possível fazer check-in. A reserva foi cancelada.")

        elif self.__status == "EM USO":
            print("Não foi possível fazer check-in. O laboratório já foi reservado.")

        else:
            print("Status da reserva inválido.")

        return False