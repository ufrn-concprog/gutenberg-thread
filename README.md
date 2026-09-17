# Trabalho Prático: Contagem de Frequência de Palavras

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

**Importante:** nenhuma *thread* deve escrever em uma estrutura de dados compartilhada durante sua execução; cada *thread* deve operar apenas sobre seu próprio bloco de entrada e sobre seu próprio resultado parcial. A combinação dos resultados deve ocorrer **somente após todas as *threads* terem terminado** sua execução. Isso significa que nenhum mecanismo de sincronização deve ser necessário; se a solução a ser implementada parecer exigir um, isso indica que a divisão do trabalho entre as threads não está correta.

A definição de "palavra" fica a critério. Decisões como a diferenciação entre maiúsculas e minúsculas, tratamento de pontuação, acentuação, números ou eventual normalização adicional devem ser definidas a critério e **explicitamente documentadas no relatório**. Não há uma única forma correta exigida, mas a escolha feita deve ser justificada e suficientemente clara para que os resultados sejam interpretáveis.

### Obtenção do corpus

O *corpus de texto* será obtido a partir do [*Project Gutenberg*](https://www.gutenberg.org), um acervo de livros de domínio público. Para isso, deve ser utilizado o *script* [`download_corpus.py`](corpus/download_corpus.py) presente neste repositório, que consulta a API pública [*Gutendex*](https://gutendex.com) para localizar e baixar o texto puro de um livro a partir do seu ID no *Project Gutenberg*.

Esse *script* é independente da linguagem de programação escolhida para o desenvolvimento do restante do trabalho, pois apenas prepara os arquivos de texto que serão usados como entrada. Basta executá-lo uma vez em Python para cada um dos três livros antes de iniciar a implementação, mesmo que esta seja feita em uma linguagem de programação diferente (como Java ou C++):

```bash
python corpus/download_corpus.py <book_id> <output_path>
```

em que `book_id` é o ID do livro no *Project Gutenberg* e `output_path` é o caminho do arquivo no qual o texto será salvo. Preferencialmente, utilize um arquivo de texto simples (`.txt`) como saída, **um para cada livro**.

Os três *corpora* a serem utilizados são fixos para garantir comparabilidade entre os resultados:

| Papel no experimento | Título                             | ID no Project Gutenberg | Tamanho aproximado  |
| :------------------- | :--------------------------------- | ----------------------- | ------------------- |
| Entrada pequena      | *Alice's Adventures in Wonderland* | `11`                    | ~27 mil palavras    |
| Entrada média        | *Pride and Prejudice*              | `1342`                  | ~122 mil palavras   |
| Entrada grande       | *War and Peace*                    | `2600`                  | ~560 mil palavras   |

Os três tamanhos de livros foram escolhidos propositalmente de modo que cada um seja aproximadamente 4–5 vezes maior que o anterior (crescimento aproximadamente exponencial, não linear), o que permite observar tendências com mais clareza do que se os tamanhos fossem muito próximos entre si. **Não é permitido substituir nenhum desses três livros por outros textos.**

## Implementação

O programa a ser implementado deve contemplar:

1. uma **versão sequencial**, sendo esta a implementação de referência, sem uso de *threads*, para servir de *baseline* nas comparações.
2. uma **versão com threads**, com o número de *threads* configurável via parâmetro de linha de comando ou por uma constante facilmente ajustável no código; esse valor não deve ser fixado no código de forma que exija recompilação para testar valores diferentes.

### Experimentação

A tarefa de experimentação consiste em realizar sucessivas execuções do programa implementado, considerando os três textos como entrada e exatamente as seguintes quantidades de *threads*: **1, 2, 4, 8 e 16**. O valor 1 corresponde à execução sequencial, mantendo a mesma divisão em blocos, mas com uma única thread processando todo o texto. Essa variação possibilitará explorar o que acontece quando um grande número de *threads* é criado e a capacidade do sistema operacional para lidar com elas de forma eficiente. 

Caso o valor 16 para o número de *threads* exceda o número de núcleos lógicos disponíveis na máquina utilizada na experimentação, é provável que o desempenho não continue melhorando (podendo até piorar) a partir de algum ponto entre os valores testados. Portanto, deve ser informado no relato o número de núcleos lógicos da máquina utilizada na experimentação, para contextualizar em qual dos valores testados (1, 2, 4, 8 ou 16) esse comportamento começou a ocorrer. Além disso, caso se observe alguma dificuldade na execução decorrente do número de *threads* ou do volume do *corpus* analisado, em razão dos limites impostos pelo sistema operacional, isso deverá ser devidamente registrado no relato, uma vez que se trata dos limites práticos da programação concorrente.

A versão sequencial do programa também deverá ser submetida à mesma carga de trabalho (incluindo a mensuração do tempo de execução) para possibilitar uma análise comparativa em relação à versão sequencial. Do ponto de vista quantitativo, essa análise pode ser feita determinando o ganho de desempenho (*speed-up*) eventualmente obtido com a versão concorrente. Esse cálculo pode ser realizado através da seguinte equação:

$$ S = \frac{T_s}{T_c} $$

sendo $S$ o *speed-up*, $T_s$ o tempo médio despendido pela versão sequencial e $T_c$ o tempo médio despendido pela versão concorrente. Caso o valor do *speed-up* seja superior a 1, tem-se que a versão concorrente é de fato melhor em termos de desempenho do que a sequencial.

**Observação:** É bem sabido que o início da execução de um programa implementado na linguagem de programação Java é afetado de forma relativamente prejudicial pelo carregamento de classes na memória realizado pela máquina virtual Java (JVM) antes da execução propriamente dita do programa, o que se chama *warm-up*. Com isso, apenas após esse processo de carregamento ter sido concluído é que se pode mensurar de forma confiável o desempenho do programa. Caso os programas objeto deste trabalho tenham sido implementados nessa linguagem de programação, a estratégia mais simples para uma medição confiável (uma vez que os programas em questão não possuem requisitos estritos de latência) é realizar algumas execuções do programa e as desconsiderar, justamente pelo fato de os tempos de execução observados serem certamente influenciados pelo tempo de *warm-up* da JVM.

- **10 execuções repetidas por configuração**, reportando média e desvio padrão do tempo de execução — seguindo a mesma metodologia utilizada nos benchmarks apresentados em aula.

Isso totaliza 5 valores de threads × 3 tamanhos de corpus × 10 execuções = 150 execuções cronometradas, além da linha de base sequencial verdadeira.



**Sobre aquecimento (warm-up):** para duplas que optarem por **Java**, é necessário considerar os efeitos de compilação JIT (Just-In-Time) sobre o tempo medido — recomenda-se descartar algumas execuções iniciais antes de começar a coleta, documentando quantas execuções foram descartadas e por quê. Para **C++** e **Python**, esse cuidado não é necessário.

## Entregáveis

1. **Repositório da dupla no Classroom 50**, contendo:
   - Código-fonte da versão sequencial e da versão com threads.
   - Um `README.md` explicando como compilar/executar o código e como reproduzir os experimentos (incluindo como obter o corpus).
2. **Relatório curto, em português**, com a seguinte estrutura:

   1. **Introdução** — o problema escolhido (contagem de frequência de palavras) e por que ele é adequado à paralelização sem sincronização.
   2. **Projeto da solução** — como o texto foi dividido entre as threads, decisões de implementação, **definição de "palavra" adotada e sua justificativa**, e por que nenhum mecanismo de sincronização foi necessário.
   3. **Metodologia experimental** — hardware utilizado (processador, número de núcleos), linguagem escolhida, tamanho exato (em número de palavras e/ou caracteres) de cada um dos três corpora especificados após a normalização adotada, valores de N testados (1, 2, 4, 8 e 16), número de execuções por configuração (10), e, no caso de implementações em Java, quantas execuções iniciais foram descartadas para aquecimento e a justificativa para esse número.
   4. **Resultados** — tabela(s) e/ou gráfico(s) de tempo médio e desvio padrão por configuração.
   5. **Análise e discussão** — o speedup obtido corresponde ao esperado? A partir de que ponto o ganho de desempenho deixa de compensar (ou até piora) ao aumentar o número de threads? Esse ponto de saturação muda conforme o tamanho da entrada aumenta (pequena → média → grande)? Existe uma tendência clara, ou o comportamento é irregular entre os três tamanhos?
   6. **Conclusão** — principais aprendizados sobre concorrência com threads a partir do experimento.

## Avaliação (nota máxima: 4,0)

| Critério | Pontos |
|---|---|
| Implementação correta (divisão adequada do trabalho, ausência de escrita concorrente em estrutura compartilhada, versão sequencial presente) | 1,5 |
| Rigor experimental (uso dos 5 valores de threads especificados, três tamanhos de corpus especificados, 10 execuções repetidas por configuração, média e desvio padrão reportados, tratamento adequado de aquecimento no caso de Java) | 1,0 |
| Qualidade do relatório (metodologia clara, interpretação correta dos resultados, análise genuína e não apenas repetição dos números, definição de "palavra" documentada e justificada) | 1,0 |
| Qualidade do código e práticas no repositório (README, histórico de commits razoável, organização do código) | 0,5 |
