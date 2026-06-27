from laboratorio import Laboratorio
from reserva import Reserva
from datetime import datetime

# Criando um laboratório
lab = Laboratorio(
    id=1,
    nome="Laboratório de Informática 1",
    is_ativo=True,
    capacidade=30
)

# Criando uma reserva
r = Reserva(
    data_hora=datetime.now(),
    motivo="Aula de Programação",
    status="APROVADA"
)

# Associando a reserva ao laboratório
r.set_laboratorio(lab)

# Verificando o status antes de reservar
if r.get_status() == "CANCELADA":
    print("A reserva foi cancelada.")
else:
    # Tentando reservar o laboratório
    if lab.reservar(r):
        print("Reserva realizada com sucesso!")
    else:
        print("Não foi possível realizar a reserva.")

    # Fazendo check-in
    if r.fazer_checkin():
        print("Check-in realizado!")

    # Só imprime o status se não for "EM USO"
    if r.get_status() != "EM USO":
        print("Status da reserva:", r.get_status())
