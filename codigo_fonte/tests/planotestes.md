# 🧪 Plano de Testes

Esta seção apresenta os testes planejados para validar as principais funcionalidades do Sistema de Reserva de Laboratórios. Cada teste verifica se o sistema atende aos requisitos funcionais especificados.

| ID | Descrição | Entrada | Saída Esperada | Resultado |
|----|-----------|---------|----------------|-----------|
| T01 | Cadastro de usuário | Nome, e-mail | Usuário cadastrado com sucesso | Passou |
| T02 | Cadastro de laboratório | Nome e capacidade válidos | Sala registrada com sucesso  | Passou |
| T03 | Cadastro com e-mail incorreto |Nome, E-mail invalido | Mensagem de erro informando credenciais inválidas | Passou |
| T04 | Solicitação de reserva | Laboratório disponível, data e horário válidos | Reserva criada com status **Pendente** | Passou |
| T05 | Solicitação em horário ocupado | Laboratório já reservado para o mesmo horário | Reserva rejeitada por conflito de horário | Passou |
| T06 | Solicitação em horário final menor que inicial | Data final com horario uma hora antes da inicial | Mensagem informando indisponibilidade | Passou |
| T07 | Aprovação de reserva | Reserva com status **Pendente** | Status alterado para **Aprovada** | Passou |
| T08 | Cancelamento de reserva pelo admin | Reserva aprovada pertencente ao professor | Reserva cancelada e horário liberado | Passou |
| T09 | Rejeição de reserva | Reserva com status **Pendente** | Status alterado para **Rejeitada** | Passou |
| T10 | Consulta de reservas pendentes | Multiplas Reservas com status **Pendente**, **Aprovada** e **Rejeitada** | Lista de reservas ainda sem resposta | Passou |

## Resumo

- **Total de testes planejados:** 10
- **Testes aprovados:** 10
- **Testes reprovados:** 0
- **Taxa de sucesso:** **100%**
