# BRIEF — Tradução e adaptação PT-BR do tutorial Epiverse-TRACE "Early tasks"

## Fonte
- Original (EN): https://epiverse-trace.github.io/tutorials-early/ (Epiverse-TRACE, CC-BY 4.0)
- DOI: 10.5281/zenodo.21512018
- Arquivos de trabalho (já convertidos de Carpentries → Quarto): `_work/en/`

## Objetivo
Produzir a versão em português brasileiro, para uso em oficinas presenciais de análise de
dados de surto (análise de dados de casos, limpeza, validação, incidência e curvas epidêmicas).

## Regras invioláveis

1. **Não alterar código.** Nenhum token de código R pode mudar: funções, argumentos, nomes de
   objetos, strings, números, caminhos de arquivo, nomes de colunas (`case_id`, `date_onset`…).
   Só é permitido traduzir **comentários R** (linhas cujo conteúdo, ignorando espaços, começa com `#`).
2. **Não alterar saídas pré-impressas.** Blocos de saída de console, mensagens de erro e avisos
   do R permanecem em inglês, exatamente como o R os emite.
3. **Não alterar estrutura Quarto.** Mantenha todas as linhas `::: {.callout-...}` / `:::` como
   estão (os títulos já estão em português). Não crie, funda ou remova callouts.
4. **Não inventar.** Não acrescente números, datas, referências, DOIs, links, nomes de portarias
   ou dados que não estejam no original. Se algo do original estiver ambíguo, traduza literalmente
   e marque com `<!-- [verificar] -->` logo depois.
5. **Manter em inglês** (é o nome técnico, não se traduz): nomes de pacotes (`{cleanepi}`,
   `{linelist}`, `{incidence2}`, `{readepi}`, `{simulist}`, `{tibble}`, `{dplyr}`…), nomes de
   funções (`cleanepi::clean_data()`), nomes de colunas e valores de colunas, URLs, caminhos de
   arquivo, e o termo **linelist** (na primeira ocorrência escreva "linelist (lista de casos)" e
   depois use só "linelist").
6. **Tom.** Português brasileiro técnico, direto, como um epidemiologista explicando para outro.
   Sem floreio, sem "vamos mergulhar", sem "poderoso". Trate o leitor por "você".
7. **Links internos**: mantenha os destinos como estão (já apontam para os arquivos do site PT).

## Termbase (use consistentemente)

| Inglês | Português |
|---|---|
| outbreak | surto |
| outbreak analytics | análise de surtos |
| case data | dados de casos |
| linelist | linelist |
| cleaning / to clean | limpeza / limpar |
| validation / validate | validação / validar |
| incidence | incidência |
| epidemic curve | curva epidêmica |
| aggregated data | dados agregados |
| reporting delay | atraso de notificação |
| right-censoring | censura à direita |
| case definition | definição de caso |
| date of onset | data de início dos sintomas |
| to import / to read data | importar / ler dados |
| data frame | data frame |
| dataset | conjunto de dados |
| column names | nomes das colunas |
| missing values | valores ausentes |
| duplicated rows | linhas duplicadas |
| key / primary key | chave / chave primária |
| R package | pacote do R |
| code chunk | bloco de código |
| tidy data | dados tidy (organizados) |
| dictionary | dicionário (de dados) |
| Challenge | Desafio |
| Solution | Solução |
| Hint | Dica |
| Key points | Pontos-chave |
| checklist | checklist |
| to handle | tratar / lidar com |
| you can | você pode |

## Ferramentas e ambiente (adaptação ao contexto brasileiro)
- Onde o original diz **RStudio**, escreva **Positron (ou RStudio, se preferir)** na primeira
  menção de cada arquivo e apenas **Positron** nas seguintes. Não reescreva capturas de tela nem
  menus que só existem no RStudio — nesses casos mantenha RStudio e não invente equivalente.
- Onde o original ensina a instalar pacotes, você pode acrescentar a menção ao espelho brasileiro
  do CRAN — use **exatamente** esta linha, sem alterar o resto:
  `options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))`.
- **Não** crie blocos de contexto brasileiro por conta própria. Quando perceber um ponto onde
  caberia uma ligação com a prática brasileira (SINAN, DATASUS, e-SUS, rotina de vigilância),
  deixe um comentário no arquivo, na linha exata, neste formato:
  `<!-- CONTEXTO-BR: sugestão curta do que caberia aqui -->`
  O revisor (agente pai) decide e escreve o texto final desses boxes.

## Entrega
- Arquivo de saída no caminho indicado no prompt do seu agente, em UTF-8.
- Ao terminar, informe: caminho absoluto do arquivo, número de linhas (`wc -l`) e lista de
  marcações `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` que você deixou.
