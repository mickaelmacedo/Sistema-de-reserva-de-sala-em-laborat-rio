# 4. Evidência de TDD

## Funcionalidade: Visualizar todas as solicitações de reserva

Para demonstrar a utilização da metodologia **Test-Driven Development (TDD)**, foi escolhida a funcionalidade **Visualizar todas as solicitações de reserva**.

O desenvolvimento seguiu as três etapas do TDD:

### 1. Red (Teste criado antes da implementação)

Primeiramente foi criado um teste para validar que o sistema deveria retornar todas as reservas cadastradas no repositório.

Arquivo:

```
tests/test_reserva_service.py
```

```python
def test_listar_todas_as_reservas(service, professor, laboratorio):

    from datetime import datetime, timedelta

    inicio = datetime.now() + timedelta(days=1)
    fim = inicio + timedelta(hours=2)

    service.solicitar_agendamento(
        professor,
        laboratorio,
        inicio,
        fim
    )

    reservas = service.listar_todas()

    assert len(reservas) == 1
```

Neste momento o teste **falhou**, pois o método `listar_todas()` ainda não existia na classe `ReservaService`.
