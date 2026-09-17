# Trabalho Prático: Projeto Gutenberg

<sub>Última atualização: 17/09/2026</sub>

## Sumário

- [Objetivo](#objetivo)
- [Tarefas](#tarefas)
  - [O problema](#o-problema)
  - [Obtenção do corpus](#obtenção-do-corpus)
  - [Implementação](#implementação)
  - [Experimentação](#experimentação)
  - [Relato](#relato)
- [Autoria e política de colaboração](#autoria-e-política-de-colaboração)
- [Entrega](#entrega)
- [Avaliação](#avaliação)
- [Dúvidas e informações](#dúvidas-e-informações)

## Objetivo

Implementar e avaliar experimentalmente uma solução que utilize múltiplas *threads* para o problema de contagem de frequência de palavras em um *corpus* de texto, comparando o desempenho com diferentes números de *threads*.

## Tarefas

### O problema

Este trabalho consiste essencialmente em implementar um programa que, dado um *corpus* de texto, conte a frequência de cada palavra. Essa tarefa deve ser dividida da seguinte forma:

1. O texto é dividido em ***N* blocos independentes** (por exemplo, por linha ou por parágrafo), onde *N* é o número de *threads* utilizadas.
2. Cada *thread* conta as frequências de palavras **apenas no seu próprio bloco**, produzindo um resultado parcial (um dicionário/mapa de palavras--contagem) que pertence exclusivamente àquela *thread*.
3. Após todas as threads finalizarem (*join*), os resultados parciais são **combinados em uma única contagem final**, realizada na *thread* principal.

**Importante:** nenhuma *thread* deve escrever em uma estrutura de dados compartilhada durante sua execução; cada *thread* deve operar apenas sobre seu próprio bloco de entrada e sobre seu próprio resultado parcial. A combinação dos resultados deve ocorrer **somente após todas as *threads* terem concluído sua execução**. Isso significa que nenhum mecanismo de sincronização deve ser necessário; se a solução a ser implementada parecer exigir um, isso indica que a divisão do trabalho entre as threads não está correta.

A definição de "palavra" fica a critério. Decisões como a diferenciação entre maiúsculas e minúsculas, o tratamento de pontuação, a acentuação, os números ou a eventual normalização adicional devem ser definidas a critério e **explicitamente documentadas no relatório**. Não há uma única forma correta exigida, mas a escolha feita deve ser justificada e suficientemente clara para que os resultados sejam interpretáveis.

### Obtenção do corpus

O *corpus de texto* será obtido a partir do [*Project Gutenberg*](https://www.gutenberg.org), um acervo de livros de domínio público. Para isso, deve ser utilizado o *script* [`download_corpus.py`](corpus/download_corpus.py) presente neste repositório, que consulta a API pública [*Gutendex*](https://gutendex.com) para localizar e baixar o texto puro de um livro a partir do seu ID no *Project Gutenberg*.

Esse *script* é independente da linguagem de programação escolhida para o desenvolvimento do restante do trabalho, pois apenas prepara os arquivos de texto que serão usados como entrada. Basta executá-lo uma vez em Python para cada um dos três livros antes de iniciar a implementação, mesmo que esta seja feita em uma linguagem de programação diferente (como Java ou C++):

```bash
python corpus/download_corpus.py <book_id> <output_path>
```

em que `book_id` é o ID do livro no *Project Gutenberg* e `output_path` é o caminho do arquivo no qual o texto será salvo. Preferencialmente, utilize um arquivo de texto simples (`.txt`) como saída, **um para cada livro**.

Os três *corpora* a serem utilizados são fixos para garantir comparabilidade entre os resultados:

| Papel no experimento | Título                             | ID no Project Gutenberg | Tamanho aproximado  |
| :------------------- | :--------------------------------- | :---------------------- | :------------------ |
| Entrada pequena      | *Alice's Adventures in Wonderland* | 11                      | ~27 mil palavras    |
| Entrada média        | *Pride and Prejudice*              | 1342                    | ~122 mil palavras   |
| Entrada grande       | *War and Peace*                    | 2600                    | ~560 mil palavras   |

Os três tamanhos de livros foram escolhidos propositalmente de modo que cada um seja aproximadamente 4–5 vezes maior que o anterior (crescimento aproximadamente exponencial, não linear), o que permite observar tendências com mais clareza do que se os tamanhos fossem muito próximos entre si. **Não é permitido substituir nenhum desses três livros por outros textos.**

## Implementação

O programa a ser implementado deve contemplar:

1. uma **versão sequencial**, sendo esta a implementação de referência, sem uso de *threads*, para servir de *baseline* nas comparações.
2. uma **versão com threads**, com o número de *threads* configurável via parâmetro de linha de comando ou por uma constante facilmente ajustável no código; esse valor não deve ser fixado no código, de modo que exija recompilação para testar valores diferentes.

O programa poderá ser implementado utilizando as facilidades das linguagens de programação C/C++, Java ou Python. Outra linguagem de programação diferente dessas três poderá ser utilizada contanto que a proposta seja previamente validada com o docente. O desenvolvimento da solução deve, de antemão, visar ao desenvolvimento de *software* de qualidade, isto é, que funcione correta e eficientemente, seja exaustivamente testado, bem documentado e com tratamento adequado de eventuais exceções.

### Experimentação

A tarefa de experimentação consiste em realizar sucessivas execuções do programa implementado, considerando os três textos como entrada e exatamente as seguintes quantidades de *threads*: **1, 2, 4, 8 e 16**. O valor 1 corresponde à execução sequencial, mantendo a mesma divisão em blocos, mas com uma única thread processando todo o texto. Essa variação permitirá explorar o que acontece quando um grande número de *threads* é criado e a capacidade do sistema operacional de lidar com elas de forma eficiente. 

Caso o valor 16 para o número de *threads* exceda o número de núcleos lógicos disponíveis na máquina utilizada na experimentação, é provável que o desempenho não continue melhorando (podendo até piorar) a partir de algum ponto entre os valores testados. Portanto, deve ser informado no relato o número de núcleos lógicos da máquina utilizada na experimentação, para contextualizar em qual dos valores testados (1, 2, 4, 8 ou 16) esse comportamento começou a ocorrer. Além disso, caso se observe alguma dificuldade na execução decorrente do número de *threads* ou do volume do *corpus* analisado, em razão dos limites impostos pelo sistema operacional, isso deverá ser devidamente registrado no relato, uma vez que se trata de limitações práticas da programação concorrente.

No intuito de tornar os experimentos estatisticamente representativos, será necessário executar, para cada uma das versões, um total de **10 vezes** para cada cenário, o que totaliza 5 valores de *threads* $\times$ 3 tamanhos de *corpus* $\times$ 10 execuções = 150 execuções. O tempo de cada grupo de 10 execuções deverá ser registrado a fim de calcular os valores máximo, mínimo, médio e desvio padrão. É importante utilizar uma unidade de medida em um nível de granularidade que permita a observação dos valores. Por exemplo, a utilização de segundos (ou mesmo milissegundos, dependendo do caso) como unidade de medida pode resultar em valores significativamente pequenos e expressos praticamente como zero, o que não é desejável para o propósito da análise.

Especificamente em relação à análise comparativa entre as versões sequencial e concorrente, ainda é necessário determinar o ganho de desempenho (*speed-up*) eventualmente obtido com a versão concorrente. Esse cálculo pode ser realizado através da seguinte equação:

$$ S = \frac{T_s}{T_c} $$

sendo $S$ o *speed-up*, $T_s$ o tempo médio despendido pela versão sequencial e $T_c$ o tempo médio despendido pela versão concorrente. Caso o valor do *speed-up* seja superior a 1, a versão concorrente é, em média, melhor do que a versão sequencial em termos de desempenho.

**Observação:** É bem sabido que o início da execução de um programa implementado na linguagem de programação Java é afetado de forma relativamente prejudicial pelo carregamento de classes na memória, realizado pela máquina virtual Java (JVM), antes da execução propriamente dita do programa, o que se chama *warm-up*. Com isso, apenas após esse processo de carregamento ter sido concluído é que se pode mensurar de forma confiável o desempenho do programa. Caso os programas objeto deste trabalho tenham sido implementados nessa linguagem de programação, a estratégia mais simples para uma medição confiável (uma vez que os programas em questão não possuem requisitos estritos de latência) é realizar algumas execuções do programa e desconsiderá-las, justamente porque os tempos de execução observados são certamente influenciados pelo tempo de *warm-up* da JVM. O relato deve informar quantas execuções foram descartadas devido ao *warm-up*.

## Relato

Uma vez realizadas as tarefas de implementação e de experimentação, deverá ser elaborado um relatório contendo, no mínimo, as seguintes seções:

1. **Introdução.** Descrever o problema e explicar por que ele é adequado para ser tratado por meio de programação concorrente.
2.  **Projeto da solução.** Descrever como o texto foi dividido entre as *threads*, as decisões de implementação, a definição de "palavra" adotada e sua justificativa.
3.  **Metodologia experimental.** Apresentar a caracterização técnica da máquina utilizada (processador e quantidade de núcleos, sistema operacional, quantidade de memória RAM), a linguagem de programação e a versão do compilador empregados, tamanho exato (em número de palavras e/ou caracteres) de cada um dos três *corpora* especificados após a normalização adotada, números de *threads* testados e, no caso de implementações em Java, quantas execuções iniciais foram descartadas para aquecimento e a justificativa para esse número.
4.**Resultados.** Apresentar os resultados obtidos relativos aos tempos observados na execução das versões sequencial e concorrente, em forma de gráfico de linha e de tabelas.
5. **Análise e discussão.** Discutir os resultados sob a perspectiva do relacionamento entre o desempenho dos programas e a carga de trabalho, bem como realizar uma análise do ganho de desempenho (*speed-up*). O *speed-up* obtido corresponde ao esperado? A partir de que ponto o ganho de desempenho deixa de compensar (ou até piora) com o aumento do número de *threads*? Esse ponto de saturação muda conforme o tamanho da entrada aumenta? Existe uma tendência clara ou o comportamento é irregular entre os três tamanhos?
9. **Conclusão.** Principais aprendizados sobre concorrência com *threads* a partir do experimento.

## Autoria e política de colaboração

Este trabalho deverá necessariamente ser realizado em equipe composta por **até dois estudantes**, sendo importante, quando possível, dividir as tarefas igualmente entre os integrantes. Após a implementação das soluções para os problemas propostos, o arquivo [`author.md`](https://github.com/ufrn-concprog/gutenberg-thread/tree/master/author.md) presente no repositório deverá ser editado preenchendo as informações de identificação dos integrantes da equipe, na seção [Informações de Autoria](https://github.com/ufrn-concprog/gutenberg-thread/tree/master/author.md#identificação-de-autoria).

O trabalho em cooperação entre os estudantes da turma é estimulado, sendo admissível a discussão de ideias e estratégias. Contudo, tal interação não deve ser entendida como permissão para a utilização de (parte do) código-fonte de colegas, o que pode caracterizar uma situação de plágio. **Trabalhos copiados, no todo ou em parte, de outros colegas ou da Internet, ou ainda gerados por ferramentas de Inteligência Artificial, serão anulados e receberão nota zero.**

## Entrega

O sistema de controle de versões [Git](https://git-scm.com) e o serviço de hospedagem de repositórios [GitHub](https://git-scm.com) serão utilizados para possibilitar a entrega da implementação realizada. Para possibilitar a associação de repositórios Git a cada equipe e reuni-los sob a mesma infraestrutura, foi criada uma atividade (*assignment*) no [Classroom 50](https://classroom50.org/).

A fim de garantir a boa manutenção do repositório, deve-se ainda configurar corretamente o arquivo `.gitignore` para desconsiderar arquivos que não devam ser versionados, como os executáveis gerados pela compilação do código-fonte. Também não é necessário versionar os arquivos de saída gerados pela obtenção do *corpus*.

A entrega deste trabalho deverá ser realizada até as **23:59 do dia 30 de setembro de 2026** no respectivo repositório Git da equipe. O relatório elaborado, preferencialmente em formato *Adobe Portable Document Format* (PDF), deverá ser enviado através da opção *Tarefas* da Turma Virtual do SIGAA, juntamente com o endereço do repositório no campo *Comentários*. **Um único membro da equipe deve realizar esse envio**, e não serão aceitos envios por outros meios ou em repositórios que não os descritos nesta especificação.

## Avaliação

A avaliação do trabalho contabilizará nota de até 4,0 pontos na 1ª Unidade da disciplina e será feita de acordo com os seguintes critérios:

| Critério | Pontos |
| :--------| ------ |
| Implementação correta (divisão adequada do trabalho, ausência de escrita concorrente em estrutura compartilhada, versão sequencial presente) | 1,5 |
| Rigor experimental (uso dos 5 valores de *threads* especificados, três tamanhos de *corpus* especificados, 10 execuções repetidas por configuração, média e desvio padrão reportados, tratamento adequado de *warm-up* no caso de Java) | 1,0 |
| Qualidade do relatório (metodologia clara, interpretação correta dos resultados, análise genuína e não apenas repetição dos números, definição de "palavra" documentada e justificada) | 1,0 |
| Qualidade do código e práticas no repositório (README, histórico de *commits* razoável, organização do código) | 0,5 |

## Dúvidas e informações

Caso haja qualquer dúvida, questionamento ou necessidade de informação adicional, enviar um *e-mail* para <everton.cavalcante@ufrn.br>.
