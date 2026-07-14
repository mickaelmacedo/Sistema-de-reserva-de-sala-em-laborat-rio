# Sistema de Reserva de Laboratório — Arquitetura e Design

## 1. Padrão arquitetural escolhido

**Arquitetura em camadas (3 camadas), em uma aplicação de console (CLI), com persistência em arquivos JSON.**

**Justificativa:**
- Cada camada tem uma responsabilidade única e só conhece a camada imediatamente abaixo dela: `Menu` (view) chama os `Services`; os `Services` chamam os `Repositories`; os `Repositories` leem/escrevem os arquivos JSON. Isso fica evidente em `main.py`, onde os repositórios são criados primeiro, depois injetados nos serviços, e por fim os serviços são injetados no `Menu`.
- Separar a validação de regra de negócio (nos `Services`) da persistência (nos `Repositories`) permite testar as regras (ex.: impedir conflito de horário, impedir que um aluno solicite agendamento) sem depender de arquivo em disco — o projeto já inclui `pytest` e `pytest-cov` no `requirements.txt` para isso.
- Como a interface hoje é um menu de terminal, essa separação também é o que vai permitir trocar a `view` no futuro (por exemplo, para uma interface web) sem precisar reescrever as regras de negócio ou a persistência — só a camada de apresentação muda.
- É a opção de menor custo de implementação para o prazo do projeto: usa apenas a biblioteca padrão do Python (`json`, `os`, `datetime`, `abc`), sem exigir banco de dados externo nem framework web.

---

## 2. Diagrama de arquitetura

```
┌─────────────────────────────────┐
│   Usuário (terminal)            │
└────────────────┬────────────────┘
                 │ entrada/saída via input()/print()
                 ▼
┌────────────────────────────────────────────┐
│  Camada de apresentação — views/menu.py    │
│  Menu interativo (usuários, laboratórios,  │
│  reservas)                                 │
└────────────────┬───────────────────────────┘
                 │ chama métodos dos services
                 ▼
┌────────────────────────────────────────────────┐
│  Camada de negócio — services/                 │
│  UsuarioService · LaboratorioService ·         │
│  ReservaService                                │
│  (validações, permissões, conflito de horário) │
└────────────────┬───────────────────────────────┘
                 │ chama métodos dos repositories
                 ▼
┌───────────────────────────────────────────────┐
│  Camada de dados — repositories/              │
│  UsuarioRepository · LaboratorioRepository ·  │
│  ReservaRepository (herdam de BaseRepository) │
└────────────────┬──────────────────────────────┘
                 │ leitura/escrita
                 ▼
┌───────────────────────────────────────────────┐
│  Persistência — arquivos JSON                 │
│  data/usuarios.json · data/laboratorios.json ·│
│  data/reservas.json                           │
└───────────────────────────────────────────────┘
```

O usuário interage pelo terminal com a classe `Menu`. O `Menu` não acessa dados diretamente — ele delega tudo para os `Services` (por exemplo, `ReservaService.solicitar_agendamento`), que aplicam as regras de negócio e, só então, chamam o `Repository` correspondente para persistir ou consultar os dados em JSON.

---

## 3. Princípios SOLID aplicados (com código real do projeto)

### S — Single Responsibility Principle (SRP)

`UsuarioService` cuida apenas das regras de cadastro de usuário (validar nome, e-mail e tipo, checar duplicidade); ele não sabe como os dados são armazenados — isso é responsabilidade exclusiva do `UsuarioRepository`.

```python
# src/services/usuario_service.py
class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def cadastrar_usuario(self, nome: str, email: str, tipo: str) -> Usuario:
        self._validar_nome(nome)
        self._validar_email(email)
        self._validar_tipo(tipo)
        ...
        self.repository.salvar(novo_usuario)
        return novo_usuario
```

Da mesma forma, a classe `Reserva` (em `models/reserva.py`) só guarda os dados de uma reserva e sabe detectar conflito de horário (`conflita_com`) — ela não decide se uma reserva pode ser aprovada; isso é papel do `ReservaService`. Se a regra de aprovação mudar, só o `ReservaService` é alterado.

### O — Open/Closed Principle (OCP)

`BaseRepository` define o comportamento comum de todos os repositórios (carregar/salvar JSON, gerar próximo ID) e declara dois métodos abstratos (`_para_dict` e `_para_objeto`) que cada subclasse implementa à sua maneira:

```python
# src/repositories/base_repository.py
class BaseRepository(ABC):
    def _carregar_dados(self) -> list[dict]: ...
    def _salvar_dados(self, dados: list[dict]) -> None: ...
    def proximo_id(self) -> int: ...

    @abstractmethod
    def _para_dict(self, objeto) -> dict: ...

    @abstractmethod
    def _para_objeto(self, dado: dict): ...
```

`UsuarioRepository`, `LaboratorioRepository` e `ReservaRepository` estendem `BaseRepository` e só implementam a conversão específica de cada entidade. Se o time precisar adicionar um novo tipo de dado persistido (por exemplo, um `RecursoRepository`), basta criar uma nova subclasse — **nenhuma linha de `BaseRepository` precisa ser alterada**. Isso é exatamente o que o OCP pede: aberto para extensão, fechado para modificação.

---

## 4. Design Pattern utilizado

**Factory Method**, aplicado no método `_para_objeto()` de cada repositório.

**Onde está no código:** cada repositório tem um método dedicado só para transformar um dicionário (linha do JSON) em um objeto de domínio completo — inclusive resolvendo referências entre entidades:

```python
# src/repositories/reserva_repository.py
def _para_objeto(self, dado: dict) -> Reserva:
    usuario = self.usuario_repository.buscar_por_id(dado["usuario_id"])
    laboratorio = self.laboratorio_repository.buscar_por_id(dado["laboratorio_id"])
    ...
    return Reserva(
        id=dado["id"],
        usuario=usuario,
        laboratorio=laboratorio,
        data_inicio=datetime.strptime(dado["data_inicio"], FORMATO_DATA),
        ...
    )
```

**Justificativa:** a construção de um `Reserva` a partir do JSON não é trivial — envolve buscar o `Usuario` e o `Laboratorio` relacionados e converter datas de string para `datetime`. Encapsular essa lógica em um método de fábrica (`_para_objeto`) evita espalhar esse código de reconstrução em todo lugar que precisa ler uma reserva (`buscar_por_id`, `listar_todos`, `listar_por_laboratorio`, `listar_por_status` — todos reaproveitam o mesmo método). Isso centraliza a criação do objeto em um único ponto, facilitando manutenção caso o formato do JSON mude.

---

## 5. Tecnologias utilizadas

| Categoria | Escolha | Justificativa (com base no que o repositório usa) |
|---|---|---|
| **Linguagem** | Python 3 (com type hints) | Já era a linguagem definida no README do projeto; o código usa recursos modernos como `list[str]`, `Usuario \| None`, o que ajuda a documentar os tipos sem custo extra. |
| **Persistência** | Arquivos JSON (`data/*.json`), via biblioteca padrão `json` | Não exige instalar nem configurar um banco de dados — suficiente para o volume de dados do projeto (poucos usuários, laboratórios e reservas) e para rodar em qualquer máquina sem setup adicional. |
| **Interface** | CLI (terminal), via `input()`/`print()` | Reduz o escopo de implementação para caber no prazo, sem abrir mão de uma camada de apresentação separada — a lógica de negócio já está pronta para, futuramente, ser reaproveitada por uma interface web ou desktop. |
| **Testes** | `pytest` + `pytest-cov` (em `requirements.txt`) | Permite testar as regras de negócio (validações, conflito de horário, permissões) isoladamente da interface e da persistência, medindo cobertura de código. |
| **Gestão de tarefas** | Trello | Já definido no README para o Kanban do time. |
| **Diagramação** | Excalidraw | Já definido no README para os diagramas de casos de uso/classes/sequência/atividades (presentes em `uml_models/`). |