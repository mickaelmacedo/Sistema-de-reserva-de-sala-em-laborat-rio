# 🔗 Testes de Integração

Os testes de integração verificam a comunicação entre as camadas do sistema (Services, Repositories e Models), garantindo que o fluxo completo das funcionalidades funcione corretamente.

| ID | Integração | Cenário | Resultado Esperado | Resultado |
|----|------------|----------|--------------------|-----------|
| IT01 | `UsuarioService` + `UsuarioRepository` | Cadastrar um usuário e recuperar pela listagem | O usuário deve ser salvo no repositório e aparecer na listagem | ✅ Passou |
| IT02 | `LaboratorioService` + `LaboratorioRepository` | Cadastrar um laboratório e buscá-lo pelo ID | O laboratório deve ser persistido e recuperado corretamente | ✅ Passou |
| IT03 | `ReservaService` + `ReservaRepository` | Solicitar uma reserva e aprová-la | A reserva deve ser salva, atualizada para **Aprovada** e permanecer armazenada no repositório | ✅ Passou |

---

## IT01 – Cadastro de Usuário

**Objetivo**

Verificar a integração entre `UsuarioService` e `UsuarioRepository`.

**Fluxo**

1. Criar um usuário.
2. Salvar no repositório.
3. Listar todos os usuários.

**Resultado esperado**

- O usuário é persistido corretamente.
- A listagem retorna exatamente um usuário cadastrado.

---

## IT02 – Cadastro de Laboratório

**Objetivo**

Verificar a integração entre `LaboratorioService` e `LaboratorioRepository`.

**Fluxo**

1. Cadastrar um laboratório.
2. Buscar pelo identificador.

**Resultado esperado**

- O laboratório é salvo corretamente.
- A busca retorna o mesmo objeto cadastrado.

---

## IT03 – Solicitação e Aprovação de Reserva

**Objetivo**

Verificar o fluxo completo de uma reserva.

**Fluxo**

1. Um professor solicita um agendamento.
2. A solicitação é salva no repositório.
3. Um administrador aprova a solicitação.
4. O status da reserva é atualizado.

**Resultado esperado**

- A reserva é criada com status **Pendente**.
- Após a aprovação, o status passa para **Aprovada**.
- O administrador responsável fica registrado na reserva.

---

## Resumo

- **Framework utilizado:** pytest
- **Testes de integração:** 3
- **Status:** Todos aprovados
- **Taxa de sucesso:** **100%**
