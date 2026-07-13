# Sistema de Reserva de Laboratório — Documentação

## 1. Descrição do problema

Atualmente, o agendamento dos laboratórios do DCET é feito de forma manual: os professores combinam horários por e-mail com o secretário responsável (Rafael), e o controle de ocupação é mantido em uma planilha. Esse processo gera três problemas recorrentes:

1. **Falta de visibilidade** — professores e alunos não têm acesso a uma agenda pública dos laboratórios, então não sabem, sem perguntar diretamente ao administrador, se um horário está livre.
2. **Sobrecarga do administrador** — toda solicitação, alteração ou conflito de horário precisa passar manualmente pelo Rafael, que também precisa verificar pessoalmente a disponibilidade real dos laboratórios.
3. **Conflitos e imprevistos mal geridos** — quando um professor falta ou cancela informalmente, o laboratório fica vago sem que isso seja registrado ou comunicado, e não há critério formal e consistente para resolver disputas por um mesmo horário.

**Problema que o sistema resolve:** centralizar e automatizar o processo de solicitação, avaliação e controle de uso dos laboratórios, substituindo o fluxo baseado em e-mail e planilha por um sistema com agenda pública, fluxo de aprovação e regras claras de prioridade.

**Usuários-alvo:**
- **Administrador/Coordenador de laboratório** (hoje, o Rafael) — avalia, aprova ou rejeita solicitações, bloqueia horários e laboratórios em caso de imprevistos.
- **Professor** — solicita agendamento ou cancelamento de uso de laboratório.
- **Monitor** — solicita agendamento (sem poder cancelar).
- **Aluno / público em geral** — consulta a agenda pública, sem poder solicitar agendamentos diretamente.
- **Colegiados externos** — solicitam uso via memorando, tratados como uma categoria de prioridade diferenciada.

---

## 2. Requisitos Funcionais

| ID | Requisito |
|----|-----------|
| **RF01** | O sistema deve permitir o cadastro de usuário com e-mail e senha. |
| **RF02** | O sistema deve oferecer dois tipos de login distintos: login administrativo (coordenadores/administradores de laboratório) e login de usuário regular (professores, monitores e alunos). |
| **RF03** | O sistema deve permitir que o professor solicite o agendamento de um laboratório em um dia e horário específicos. |
| **RF04** | O sistema deve permitir que o professor solicite o cancelamento de um agendamento já aprovado. |
| **RF05** | O sistema deve permitir que o monitor solicite o agendamento de um laboratório, sem oferecer a opção de cancelamento. |
| **RF06** | O sistema deve impedir que um mesmo professor ou monitor tenha mais de uma solicitação de agendamento ativa simultaneamente (um laboratório e um horário por vez). |
| **RF07** | O sistema deve exigir que toda solicitação informe o colegiado do solicitante e o motivo do agendamento. |
| **RF08** | O sistema deve permitir que o administrador visualize as solicitações pendentes e as aprove ou rejeite. |
| **RF09** | O sistema deve permitir que o administrador bloqueie horários ou laboratórios específicos em caso de imprevisto (manutenção, problema técnico etc.), tornando-os indisponíveis para novas solicitações. |
| **RF10** | O sistema deve exibir uma agenda pública, em formato de calendário, com todos os agendamentos confirmados, acessível sem necessidade de login. |
| **RF11** | O sistema deve aplicar automaticamente uma ordem de prioridade quando duas solicitações concorrerem pelo mesmo laboratório e horário, seguindo a hierarquia: (1) Colegiado, (2) Aula, (3) Extensão, (4) Atividades externas. |
| **RF12** | O sistema deve registrar o check-in do uso efetivo do laboratório no horário agendado. |
| **RF13** | O sistema deve permitir o registro de solicitações de colegiados externos, identificando-as como originadas por memorando. |
| **RF14** | O sistema deve permitir a definição de um período no início do semestre para o agendamento em lote (reserva de dias fixos por disciplina/colegiado ao longo do semestre). |


---

## 3. Requisitos Não Funcionais (categorizados por FURPS+)

| ID | Categoria | Requisito (mensurável) |
|----|-----------|--------------------------|
| **RNF01** | **Usability** | Um usuário sem treinamento prévio deve conseguir concluir uma solicitação de agendamento em no máximo 3 telas/cliques e menos de 2 minutos. |
| **RNF02** | **Reliability** | O sistema não deve permitir, sob nenhuma circunstância, que dois agendamentos aprovados fiquem sobrepostos para o mesmo laboratório e horário (0 conflitos de dados admitidos). |
| **RNF03** | **Performance** | A consulta da agenda pública deve retornar resultados em no máximo 2 segundos, considerando até 50 acessos simultâneos. |
| **RNF04** | **Supportability** (Manutenibilidade) | O código deve ser modularizado por camada (dados, regras de negócio, interface) e possuir cobertura de testes automatizados de no mínimo 70% nas regras de agendamento e prioridade. |
| **RNF05** | **Security** | Senhas devem ser armazenadas com hash (nunca em texto puro) e sessões de usuário devem expirar automaticamente após 30 minutos de inatividade. |
| **RNF06** | **+ (Legal/Compliance)** | O armazenamento de dados pessoais (e-mail, nome, colegiado) deve seguir os princípios da LGPD, permitindo a exclusão de conta e dos dados associados mediante solicitação do usuário. |
| **RNF07** | **+ (Design Constraint)** | O sistema deve ser implementado em Python e ser acessível via navegador web, sem exigir instalação de software adicional pelo usuário final. |

---

## 4. User Stories

**US01 — Solicitação de agendamento (Professor)**
> Como **professor**, quero **solicitar o agendamento de um laboratório em um dia e horário específicos**, para **garantir o uso do espaço para minha disciplina**.
> **Critérios de aceitação:**
> - Dado que estou logado como professor, quando seleciono um laboratório e horário disponíveis e informo colegiado e motivo, então a solicitação é registrada com status "pendente".
> - O sistema não permite selecionar um horário já bloqueado ou ocupado.

**US02 — Cancelamento de agendamento (Professor)**
> Como **professor**, quero **cancelar um agendamento que já fiz**, para **liberar o laboratório caso eu não possa mais utilizá-lo**.
> **Critérios de aceitação:**
> - Dado um agendamento aprovado em meu nome, quando solicito o cancelamento, então o horário volta a ficar disponível na agenda pública.
> - Monitores não veem essa opção em suas solicitações.

**US03 — Solicitação de agendamento (Monitor)**
> Como **monitor**, quero **solicitar o uso de um laboratório**, para **realizar atividades de monitoria no horário necessário**.
> **Critérios de aceitação:**
> - Dado que estou logado como monitor, quando envio uma solicitação, então ela aparece na fila de aprovação do administrador.
> - Não há botão de cancelamento disponível para solicitações de monitor.

**US04 — Aprovação de solicitações (Administrador)**
> Como **administrador (Rafael)**, quero **visualizar e avaliar as solicitações pendentes**, para **decidir quais agendamentos serão confirmados sem precisar checar a disponibilidade pessoalmente**.
> **Critérios de aceitação:**
> - Dado que existem solicitações pendentes, quando acesso o painel administrativo, então vejo lista com solicitante, colegiado, motivo, laboratório e horário.
> - Ao aprovar, o agendamento passa a constar na agenda pública; ao rejeitar, o solicitante é notificado.

**US05 — Bloqueio emergencial de laboratório (Administrador)**
> Como **administrador**, quero **bloquear um laboratório ou horário específico**, para **impedir novas solicitações quando houver um problema inesperado (ex: manutenção)**.
> **Critérios de aceitação:**
> - Dado um horário bloqueado, quando um usuário tenta solicitá-lo, então o sistema informa que está indisponível.
> - Agendamentos já aprovados naquele horário são sinalizados para reavaliação.

**US06 — Consulta pública da agenda (Aluno/Professor/Público)**
> Como **membro da comunidade acadêmica**, quero **consultar a agenda dos laboratórios sem precisar fazer login**, para **saber rapidamente quais horários estão disponíveis**.
> **Critérios de aceitação:**
> - Dado que acesso a página pública, quando seleciono um laboratório, então vejo um calendário com todos os horários ocupados e livres.
> - Nenhuma ação de agendamento é permitida nesta tela sem login.

**US07 — Resolução de conflito por prioridade (Sistema/Administrador)**
> Como **administrador**, quero **que o sistema aplique automaticamente a ordem de prioridade (colegiado > aula > extensão > atividades externas) quando duas solicitações colidirem**, para **evitar decisões arbitrárias e agilizar a resolução de conflitos**.
> **Critérios de aceitação:**
> - Dado duas solicitações para o mesmo horário e laboratório, quando o sistema as processa, então a de maior prioridade é sugerida para aprovação automaticamente, sem impedir a decisão final do administrador.

**US08 — Check-in de uso do laboratório**
> Como **administrador**, quero **registrar o check-in de uso efetivo do laboratório**, para **saber quando um agendamento aprovado não foi utilizado e o horário ficou vago**.
> **Critérios de aceitação:**
> - Dado um agendamento no horário atual, quando o professor/monitor realiza check-in, então o status muda para "em uso".
> - Se não houver check-in até X minutos após o início do horário, o sistema marca o agendamento como "vago".

**US09 — Solicitação de colegiado externo via memorando**
> Como **coordenador de um colegiado externo ao DCET**, quero **registrar minha solicitação de uso de laboratório com base em um memorando**, para **ter meu pedido tratado dentro do fluxo formal e da hierarquia de prioridade correta**.
> **Critérios de aceitação:**
> - Dado que sou um solicitante externo, quando registro minha solicitação, então ela é identificada como "atividade externa" para fins de prioridade.

**US10 — Agendamento em lote no início do semestre**
> Como **professor**, quero **reservar previamente os dias da semana em que terei aula em determinado laboratório durante todo o semestre**, para **não precisar refazer a solicitação a cada semana**.
> **Critérios de aceitação:**
> - Dado o período de agendamento em lote definido pelo administrador, quando informo os dias fixos da semana e o intervalo de datas, então o sistema gera automaticamente as solicitações recorrentes para aprovação.

---

## 5. Priorização dos Requisitos

### 🟢 MVP (essenciais para a primeira entrega)
- RF01 — Cadastro de usuário
- RF02 — Login administrativo x login regular
- RF03 — Solicitação de agendamento (professor)
- RF05 — Solicitação de agendamento (monitor)
- RF06 — Limite de uma solicitação ativa por usuário
- RF07 — Registro de colegiado e motivo na solicitação
- RF08 — Aprovação/rejeição de solicitações pelo administrador
- RF10 — Agenda pública em formato de calendário
- RNF01, RNF02, RNF05 (usabilidade básica, integridade de dados, segurança de senha)

### 🟡 Desejáveis (segunda iteração)
- RF04 — Cancelamento de agendamento (professor)
- RF09 — Bloqueio de horários/laboratórios pelo administrador
- RF11 — Resolução automática de conflitos por prioridade
- RF13 — Registro de solicitações externas via memorando
- RNF03, RNF04 (performance e manutenibilidade)

### 🔵 Futuros (versões posteriores)
- RF12 — Check-in de uso do laboratório
- RF14 — Agendamento em lote no início do semestre
- RNF06 — Conformidade LGPD completa (exclusão de conta/dados)
- Notificações automáticas por e-mail sobre aprovação/rejeição
- Painel de estatísticas de uso dos laboratórios para o administrador

---

## 6. Glossário

| Termo | Definição |
|-------|-----------|
| **Colegiado** | Unidade acadêmica responsável por um curso; usada como critério de prioridade e como informação obrigatória em toda solicitação. |
| **Solicitação** | Pedido de uso de laboratório feito por um professor ou monitor, ainda não confirmado. Diferente de "Reserva". |
| **Reserva/Agendamento** | Solicitação já aprovada pelo administrador, constando oficialmente na agenda pública. |
| **Login administrativo (login adm)** | Tipo de acesso destinado a coordenadores e administradores de laboratório, com permissões de aprovar, rejeitar e bloquear. |
| **Usuário regular** | Professores, monitores e alunos; possuem permissões limitadas a solicitar (professor/monitor) ou apenas consultar (aluno). |
| **Vago** | Situação em que um laboratório foi agendado, mas o horário não foi utilizado (por ausência do responsável), tornando-se disponível novamente. |
| **Check-in** | Confirmação, dentro do sistema, de que o solicitante compareceu e está utilizando o laboratório no horário agendado. |
| **Prioridade de agendamento** | Ordem de critérios (colegiado > aula > extensão > atividades externas) usada para decidir qual solicitação prevalece em caso de conflito de horário. |
| **Memorando** | Documento formal usado por colegiados externos ao DCET para solicitar uso de laboratório junto ao administrador. |
| **Bloqueio de horário/laboratório** | Ação do administrador que torna um horário ou laboratório indisponível para novas solicitações, geralmente por imprevisto técnico ou manutenção. |