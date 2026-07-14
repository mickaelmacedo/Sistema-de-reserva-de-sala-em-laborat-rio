# Relatório de Cobertura de Testes

Este relatório apresenta o resultado da execução dos testes automatizados e a cobertura de código obtida utilizando **pytest** e **pytest-cov**.

## Execução dos Testes

```text
tests/test_laboratorio_service.py ....                                         [ 18%]
tests/test_reserva_service.py ...............                                  [ 86%]
tests/test_usuario_service.py ...                                              [100%]

22 passed in 0.08s
```

## Resumo da Execução

| Métrica | Resultado |
|---------|----------:|
| Framework de testes | pytest |
| Ferramenta de cobertura | pytest-cov |
| Total de testes executados | **22** |
| Testes aprovados | **22** |
| Testes reprovados | **0** |
| Tempo de execução | **0,08 s** |

---

## Cobertura por Arquivo

| Arquivo | Cobertura |
|----------|----------:|
| `src/repositories/base_repository.py` | 41% |
| `src/repositories/laboratorio_repository.py` | 31% |
| `src/repositories/reserva_repository.py` | 31% |
| `src/repositories/usuario_repository.py` | 41% |
| `src/services/laboratorio_service.py` | **93%** |
| `src/services/reserva_service.py` | **94%** |
| `src/services/usuario_service.py` | **90%** |

---

## Cobertura Geral

| Categoria | Cobertura |
|-----------|----------:|
| Classes de Serviço | **92%** |
| Repositórios | **34%** |
| Cobertura Total do Projeto | **63%** |

---

## Relatório Gerado

```text
Name                                         Stmts   Miss  Cover
--------------------------------------------------------------------------
src/repositories/base_repository.py             22     13    41%
src/repositories/laboratorio_repository.py      36     25    31%
src/repositories/reserva_repository.py          51     35    31%
src/repositories/usuario_repository.py          22     13    41%
src/services/laboratorio_service.py             27      2    93%
src/services/reserva_service.py                 71      4    94%
src/services/usuario_service.py                 30      3    90%
--------------------------------------------------------------------------
TOTAL                                          259     95    63%
```

---

## Análise dos Resultados

Foram executados **22 testes automatizados**, todos concluídos com sucesso, sem falhas ou erros de execução.

As classes da camada de **Serviços**, responsáveis pelas regras de negócio do sistema, apresentaram excelente cobertura (**90% a 94%**), indicando que as principais funcionalidades implementadas foram devidamente testadas.

A cobertura total do projeto foi de **63%**, superando o requisito mínimo de **40%** estabelecido para o projeto.

> **Resultado:** O sistema atende ao requisito de cobertura mínima das classes de negócio.
