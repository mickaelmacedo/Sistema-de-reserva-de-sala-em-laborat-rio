# Diagrama de Classes
- **Programa** utilizado: Draw.io
- **Classes:** 6
- **Herança:** 1
- **Composições:** 2

## Perguntas 

### Por que vocês escolheram essas classes? *Como derivaram das User Stories?*

Escolhemos essas classes pois elas representam as funcionalidades básicas do sistema. Optamos por estabelecer uma base firme somente com o que é imprescindível, garantindo maior controle ao adicionarmos funções mais específicas futuramente; assim, conseguimos avaliar se os novos recursos alteram drasticamente a estrutura já consolidada.

As user stories nos ajudaram a detectar as maiores necessidades apontadas pelo atual responsável pelos agendamentos dos laboratórios. São elas: ter maior controle sobre o status das salas (agendado ou disponível) e a possibilidade de realizar, de forma centralizada, o check-in com base nas solicitações de reserva feitas por professores e alunos. Nosso diagrama dá poder ao Administrador para atender a todas essas demandas, por isso usamos as user stories para dar mais ênfase a essa entidade.

### Qual relacionamento foi mais difícil de decidir? *(agregação vs composição vs associação simples) E por que escolheram o que escolheram?*

Todos os relacionamentos que compõem a classe Reserva. Inicialmente, apenas o administrador podia acessá-la, mas, dessa forma, não haveria interface entre os usuários comuns e seus agendamentos, tornando impossível a gestão de algo que sequer existiria. Pensamos em criar uma classe de "Solicitações", mas notamos que ela seria quase idêntica à de Reservas. Por fim, concluímos que tanto o Administrador quanto os usuários regulares poderiam interagir diretamente com a Reserva, funcionando como um elo entre eles.

### Se o sistema crescer, que novas classes precisariam ser adicionadas? *O design atual permite isso facilmente?*

Construímos o diagrama justamente para permitir essa escalabilidade. Pretendemos criar uma classe dedicada apenas ao gerenciamento das chaves dos laboratórios, além de outra para gerir informações específicas da infraestrutura, como a quantidade de computadores e a capacidade de cada sala. O design atual permite essas adições facilmente, pois a estrutura principal está isolada e pronta para ser estendida.