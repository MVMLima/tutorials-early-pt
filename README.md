# Análise de dados de surto com R — adaptação PT-BR

Site do curso **Análise de dados de surto com R: ler, limpar, validar e visualizar dados de casos
(linelist)**, adaptação para o português brasileiro do tutorial *Epiverse-TRACE Tutorials Early*.

**Site publicado:** https://mvmlima.github.io/tutorials-early-pt/

## O que tem aqui

| Arquivo | Conteúdo |
|---|---|
| `index.qmd` | Página inicial: sobre o curso, público, pré-requisitos |
| `setup.qmd` | Preparação do ambiente (R, ferramentas de compilação, pacotes, projeto do R) |
| `episodios/01-ler-dados.qmd` | Ler dados de casos (arquivos, bancos de dados, APIs) |
| `episodios/02-limpar-dados.qmd` | Limpar dados de casos |
| `episodios/03-validar-dados.qmd` | Validar dados e marcar casos (linelist) |
| `episodios/04-agregar-visualizar.qmd` | Agregar em incidência e fazer curvas epidêmicas |
| `glossario.qmd` | Glossário de termos |
| `instrutor.qmd` | Notas e plano de aula para quem conduz a oficina |
| `licenca.qmd` | Licença e créditos |
| `data/` | Os 17 arquivos de dados usados no curso (também baixáveis pelo site) |
| `img/` | Figuras do material original |
| `_source/` | Arquivos originais em inglês (formato Carpentries), mantidos para conferência |

## Como renderizar localmente

Requisitos: [Quarto](https://quarto.org/) 1.8+ e R 4.2+.

```bash
# 1. pacotes do curso numa biblioteca local do projeto (não mexe na biblioteca global do R)
Rscript -e '.libPaths(c(".Rlib", .libPaths()));
  options(repos = c(epiverse = "https://epiverse-trace.r-universe.dev",
                    CRAN = "https://cran-r.c3sl.ufpr.br/"));
  pak::pkg_install(c("readepi","cleanepi","reactable","rio","here","DBI","RSQLite",
                     "dbplyr","linelist","simulist","incidence2",
                     "epiverse-trace/tracetheme","tidyverse"), lib = ".Rlib")'

# 2. renderizar
quarto render
```

O site sai em `_site/`. Para pré-visualizar com recarregamento automático: `quarto preview`.

O `_quarto.yml` usa `execute: freeze: auto`, então os resultados dos blocos de código ficam
guardados em `_freeze/` e o build no GitHub Actions **não precisa do R nem dos pacotes**. Se
você alterar o **código** de um `.qmd`, renderize localmente de novo e commite o `_freeze/`
atualizado junto com o arquivo.

## Publicação

O workflow `.github/workflows/publish.yml` renderiza o site e publica na branch `gh-pages` a
cada push na `main`. O GitHub Pages serve a partir dessa branch.

## Verificação da tradução

```bash
python3 scripts/verificar_traducao.py
```

Compara cada episódio traduzido com o original convertido (`_source/en-quarto/`) e aponta: blocos de
código que foram alterados, callouts perdidos, links internos quebrados e imagens ausentes.

## Como a versão PT-BR foi produzida

1. `scripts/convert_carpentries.py` converte as lições do formato Carpentries Workbench
   (divs cercados com `::::`) para o formato Quarto (callouts), ajustando caminhos de dados,
   imagens e links internos.
2. Cinco agentes tradutores (CLI `agy`) traduzem e adaptam cada episódio seguindo
   `scripts/BRIEF-traducao.md` (termbase e regras: código intocado, nada inventado).
3. `scripts/verificar_traducao.py` confere a integridade do código.

## Licença

O material original é publicado sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Esta adaptação é publicada sob a **mesma licença**. Créditos completos em `licenca.qmd`.

Citação do original:

> Degoot A, Valle-Campos A, Mané K, Gruson H, Funk S, Eggo R, Kucharski A, Bah B (2026).
> *Epiverse-TRACE Tutorials Early: Read and clean case data, and make linelist for outbreak
> analytics with R.* DOI: [10.5281/zenodo.21512018](https://doi.org/10.5281/zenodo.21512018)
