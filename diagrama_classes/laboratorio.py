from datetime import datetime

class Laboratorio:

    def __init__(self, id: int, nome: str, is_ativo: bool, capacidade: int):
        self.__id = id
        self.__nome = nome
        self.__is_ativo = is_ativo
        self.__capacidade = capacidade

        # Relacionamento com Reserva (1 Laboratório pode possuir várias Reservas)
        self.__reservas = []

    # Getters
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_is_ativo(self):
        return self.__is_ativo

    def get_capacidade(self):
        return self.__capacidade

    # Setters
    def set_nome(self, nome):
        self.__nome = nome

    def set_is_ativo(self, ativo):
        self.__is_ativo = ativo

    def set_capacidade(self, capacidade):
        self.__capacidade = capacidade

    # Método de negócio
    def reservar(self, reserva):
        """
        Adiciona uma reserva ao laboratório somente
        se ele estiver ativo e o status for válido.
        """
        if not self.__is_ativo:
            print("Não foi possível realizar a reserva. O laboratório está desativado.")
            return False

        status = reserva.get_status()

        if status == "APROVADA":
            self.__reservas.append(reserva)
            print("Reserva aprovada e adicionada ao laboratório.")
            return True

        elif status == "PENDENTE":
            self.__reservas.append(reserva)
            print("Reserva pendente adicionada ao laboratório. Aguardando aprovação.")
            return True

        elif status == "CANCELADA":
            print("A reserva foi cancelada!.")
            return False

        elif status == "REJEITADA":
            print("Não foi possível realizar a reserva. A reserva foi rejeitada.")
            return False

        elif status == "EM USO":
            print("Não foi possível realizar a reserva. O laboratório já está em uso.")
            return False

        else:
            print("Status da reserva inválido.")
            return False

    def liberar(self):
        """
        Libera todas as reservas do laboratório.
        """
        self.__reservas.clear()
        print("Laboratório liberado com sucesso.")
