# Diversidados
# Desafio Aula 5: Aplicação de modelos na prática


- [Introdução](#introduçao)
  - [O Processo de aprovação](#o-processo-de-aprovacao)
- [Tarefas](#tarefas)
  - [Análise Exploratória](#analise-exploratoria)
    - [Risco de Crédito](#risco-de-credito)
	  - [Propensão a gasto](#propensa-a-gasto)
  - [Resolvendo um problema de negócio](#resolvedo-um-problema-de-negocio)
- [Arquivos](#arquivos)
- [O que esperamos das equipes?](#o-que-esperamos-das-equipes)
- [Para casa](#para-casa)
  - [Modelagem](#modelagem)
- [Os dados](#os-dados)

## Introdução

### O processo de aprovação

Para receber o seu cartão tudo o que o cliente precisa fazer é solicitá-lo através de um convite de um amigo ou se inscrevendo no nosso site. Após isso, nosso objetivo é responder em alguns segundos ou aprovando o cartão de crédito ou enviando o cliente para uma lista de espera. Todo esse processo faz uso pesado de Machine Learning para a tomada de decisões.
Resumidamente, o processo funciona mais ou menos assim:
 - Cliente recebe um convite ou faz sua solicitação direto pelo site do Nubank
- Nós fazemos requisições de dados nos nossos parceiros e rodamos diversos modelos
- Com os resultados em mãos tomamos uma decisão de crédito.
	- Aprovar ou não o cliente
	- Para os aprovados, atribuir um limite de crédito inicial

## Tarefas

### Análise Exploratória

1. A inadimplência é o aspecto mais sensível quando se fala em crédito (target_default). Faça algumas visualizações que explorem a inadimplência na base fornecida.

2. Analisando a distribuição do volume de compras em 3 meses dos clientes (variável "spends"), você diria que ela segue uma distribuição normal? Há algo de estranho nela? Se sim, qual seria a justificativa ou hipótese para tal?


### Resolvendo um problema de negócio

O desafio a ser resolvido é a decisão de dar um cartão de crédito a um cliente, e como funciona o produto de cartão de crédito?

A receita de um cartão de crédito vem de duas fontes principais: Intercâmbio e Juros.
1. Intercâmbio: Representa uma porcentagem de todos os gastos do cliente no cartão de crédito. Para o problema iremos assumir que a taxa de intercâmbio é fixa em 2% e portanto de todos os gastos do cliente, 2% se torna receita para o Nubank.
2. Juros: Se um cliente não paga o valor completo da fatura em dia, ele será cobrado um juros, que para esse problema será de 10% ao mês e portanto na próxima fatura ele será cobrado o valor não pago da fatura anterior com juros de 10%.

Os custos por sua vez vem de três fontes principais: Custos operacionais, custos de emissão do cartão e perdas por inadiplêmcia.
1. Custos operacionais: Representam custos de atendimento e infrastrutura gastos com cada novo cliente, para o problema podemos assumir que cada cliente custa R$ 10,00 ao Nubank em custos operacionais.
2. Custos de cartão: Custo de emissão do cartão para o cliente, para o problema vamos assumir um custo de R$ 5,00
3. Perdas por inadimplência, referem-se ao valor perdido caso o cliente não pague a sua fatura, para esse desafio vamos assumir que se o cliente se torna inadimplemente perdemos o valor total de sua fatura

Resumindo as informações descritas anteriormente (elas não precisam ser obrigatoriametne usadas em sua solução):


|           Métrica                            |Valor |
|:--------------------------------------------:|:----:|
|          Taxa de juros do rotativo           |  10% |
|          Taxa de intercâmbio                 |  2%  |
|          Custo unitário do cartão            |  5.0 |
|          Custo operacional                   |  10.0|
|          Inflação mensal                     |  1%  |

Um negócio é feito de decisões e é preciso definir como os dados serão usados para ajudar na tomada de decisão. Para isso serão fornecidos dados simulados de clientes usando o cartão de crédito, bem como dois modelos de previsão, um de risco e outro de gastos. **O desafio consiste em usar os dois modelos para construir uma política para decidir:**
1. Se o cliente deve ser aprovado ou não.
2. Qual o limite inicial que esse cliente deve receber.

Você pode encontrar mais sobre o funcionamento do nubank em [nosso site](https://nubank.com.br/perguntas/) na seção "Sobre o Nubank". É importante salientar que não há uma resposta única e correta para este problema e que ele pode ser abordado de diferentes formas. Sinta-se livre para propor qualquer solução que você acredite ser a melhor. 

Sabemos que é um problema complexo e adoraríamos ver abordagens simples, racionais e criativas.

Criem um notebook e discutam em grupo algumas possiveis solucões, trabalhem com os dados para validar se aquelas soluções fazem sentido e então implementem as ideias mais promissoras!

## Arquivos

- `questions.md`: este arquivo, contém a descrição do desafio e a explicação do problema;
- `Solution-template.ipynb`: Python notebook para ser usado como base para criação das analises
- /data
  - `policy_dataset.csv`, é a base que vamos trabalhar em cima durante o exercicio em questão, ela contém: 
    - dados de aquisição: Informações que sabemos das pessoas no momento que elas aplicam
    - dados de comportamento: Dados de como o cliente utilizou o cartão após ser aprovado para o cartão
    - previsões dos modelos: Previsões de gastos e risco de dois modelos treinados (spend_prediction e risk_prediction)

## O que esperamos das equipes?

Trabalho em equipe para definir uma regra de decisão para aprovação e decisão dos melhores limites começando com regras simples e tentando chegar a uma regra mais otimizada com o passar do tempo.

Para guiar os times, damos algumas dicas de como montar a política:
1. Comece definindo o valor de um cliente: A partir dos dados reais tente entender quanto de receitas e perdas cada cliente deu para o Nubank, quais clientes são mais ou menos lucrativos?
2. Comece a relacionar a lucratividade com as previsões dos modelos, como elas podem ser usadas para criar regras de aprovação?
3. Criem um forma de avaliar as diferentes regras de decisão para tentar encontrar a melhor regra.
4. Iterem sobre o problema

## Para casa

Para casa, fica o desafio de construir os modelos de risco e gastos que foram dados prontos para o desafio.

### Modelagem


Durante a aula, os dois modelos serão fornecidos para que os alunos foquem no desafio de negócio, fica como lição de casa tentar treinar os modelos e chegar em uma performance boa considerando as métricas relevantes. 

Para a análise em questão serão necessários dois modelos, um modelo para previsão de inadimplencia e um segundo modelo para previsão de gastos dos clientes. 

#### Risco de Crédito

Faça um modelo para prever o risco de inadimplência de um cliente utilizando apenas dados de acquisição, ou seja, apenas dados que são conhecidos na fase de aplicação deste. Lembre-se que o limite inicial é definido após o cliente ser aceito.


#### Propensão a Gasto

Faça um modelo que seja capaz de distinguir clientes de acordo com a sua propensão de gasto. Você é livre para transformar esse problema em regressào, classificação, não supervisionado e etc, contanto que ao final consiga distinguir qual cliente tende a gastar mais.

Para a construção do modelo, algumas questões relevantes a serem tratadas:
- O que se está tentando prever?
- Qual foi o target (variável alvo) escolhido? Se optou-se por um modelo não supervisionado, qual o motivo?
- Quais variáveis foram selecionadas e qual foi o critério de seleção?
- Quais as variáveis mais importantes do seu modelo?
- Quais métricas foram selecionadas para a validação do modelo? O que cada uma delas significa de acordo com o contexto do que se está tentando prever? Quais evidências te fariam crer ou não de que a performance de validação será a mesma de quando este modelo estiver rodando de fato com novos dados?

## Os dados

**ATENÇãO**: Todos os dados utilizados no desafio são fictícios!

### Dados de acquisição

Coluna|Tipo|Descrição
---|---|---
ids|String|identificador único de um aplicante
pii_cpf|String|CPF do aplicante
email|String|E-mail do solicitante
tags|String|Tags descritivas dadas pelo provedor de dados
score_1|String|Score de crédito 1, categorias
score_2|String|Score de crédito 2, categorias
score_3|Float|Score de crédito 3
score_4|Float|Score de crédito 4
score_5|Float|Score de crédito 5
score_6|Float|Score de crédito 6
risk_rate|Float|Risco associado ao aplicante
last_amount_borrowed|Float|Valor do último empréstimo que o aplicante tomou
last_borrowed_in_months|Int\Duração do último empréstimo que o aplicante tomou
reason|String|Razão pela qual foi feita uma consulta naquele cpf
income|Float|Renda estimada pelo provedor dos dados para o aplicante
facebook_profile|Bool|Se o aplicante possui perfil no Facebook
state|String|Estado de residência do aplicante
zip|String|Código postal do aplicante
shipping_zip_code|Int|Código do endereço de entrega
shipping_state|String|Estado do endereço de entrega
channel|String|Canal pelo qual o aplicante aplicou
job_name|String|Profissão do aplicante
real_state|String|Informação sobre habitação do aplicante
ok_since|Float|Quantidade de dias que
n_bankruptcies|Float|Quantidade de bancarrotas que o cliente já experimentou
n_defaulted_loads|Float|Quantidade de empréstimos não pagos no passado
n_accounts|Float|
n_issues|Float|
user_agent|String|Informação sobre dispositivo usado para a aplicação
reported_income|Int|Renda informada pelo próprio aplicante
profile_phone_number|String|Número de telefone, ex: `210-2813414`
marketing_channel|Object| Canal de marketing pelo qual o aplicante chegou na página de pedido de crédito
lat_lon|Object|Latitude e longitude da localização
external_data_provider_fraud_score|Int|Score de fraude
external_data_provider_first_name|String|Primeiro nome do aplicante
external_data_provider_email_seen_before|String|Se o e-mail já foi consultado junto ao provedor de dados
external_data_provider_credit_checks_last_year|Int|Quantidade de consultas de crédito na janela de um ano
external_data_provider_credit_checks_last_month|Int|Quantidade de consultas de crédito na janela de um mês
external_data_provider_credit_checks_last_2_year|Int|Quantidade de consultas de crédito na janela de dois anos
application_time_in_funnel|Int|Tempo gasto pelo aplicante durante o processo de aplicação
application_time_applied|Date|Horário de aplicação

### Dados de comportamento

Coluna|Tipo|Descrição
---|---|---
ids|String|identificador único de um aplicante
credit_line|Int|Limite do cartão
month|Int|Ordenação dos meses que a pessoa é cliente, sendo 0 o primeiro mês dela como cliente
spend|Float|Valor gasto naquele mês
revolving_balance|Float|Valor que o cliente não pagou da fatura atual e que irá rolar para a próxima
target_default|Boolean|Indicativo de inadiplêmcia sobre a pessoa ter ou não pago a fatura do cartão

### Previsões do modelo
Coluna|Tipo|Descrição
---|---|---
risk_prediction|Float|Previsão de risco dada pelo modelo
spend_prediction|Float|Previsão de gastos dada pelo modelo

