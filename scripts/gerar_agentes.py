#!/usr/bin/env python3
"""Gera os prompts e os scripts de execução dos agentes tradutores (Claude CLI)."""
import pathlib
import re

ROOT = pathlib.Path("/home/marc/Documentos/Projetos/tutorials-early-pt")
AG = ROOT / "_work" / "agents"
AG.mkdir(parents=True, exist_ok=True)

AGENTES = [
    ("01", "episodios/01-ler-dados.qmd",
     "_work/en/episodios/01-ler-dados.qmd",
     "Episódio 1 — Ler dados de casos (read-case-data): fontes de dados de surto, "
     "importação de CSV/Excel/ZIP/SPSS, conexão com bancos de dados relacionais (DBI/RSQLite), "
     "API de sistemas de informação em saúde (readepi), organização do projeto do R."),
    ("02", "episodios/02-limpar-dados.qmd",
     "_work/en/episodios/02-limpar-dados.qmd",
     "Episódio 2 — Limpar dados de casos (clean-data): diagnóstico de características dos dados, "
     "padronização de nomes de colunas, remoção de irregularidades, conversão de datas, "
     "operações específicas de epidemiologia com {cleanepi}."),
    ("03", "episodios/03-validar-dados.qmd",
     "_work/en/episodios/03-validar-dados.qmd",
     "Episódio 3 — Validar dados e marcação (tag-validate): conversão para linelist, "
     "marcação de casos, validação com {cleanepi} e {linelist}, dicionário de dados."),
    ("04", "episodios/04-agregar-visualizar.qmd",
     "_work/en/episodios/04-agregar-visualizar.qmd",
     "Episódio 4 — Agregar e visualizar (aggreagate-visualize): simulação com {simulist}, "
     "conversão de linelist em incidência com {incidence2}, curvas epidêmicas com {ggplot2}, "
     "interpretação de padrões de curva epidêmica."),
    ("05", "setup.qmd e glossario.qmd",
     "_work/en/setup.qmd + _work/en/glossario.qmd",
     "Página de Setup (instalação de R, ferramentas de compilação, pacotes do Epiverse, "
     "projeto do R, conta no GitHub) e o Glossário de termos. São DOIS arquivos de saída."),
]

PROMPT = """Você é um tradutor técnico-científico de epidemiologia. Trabalhe no diretório
{root}

## Passo 1 — Leia as regras
Leia o arquivo `scripts/BRIEF-traducao.md` (caminho absoluto: {root}/scripts/BRIEF-traducao.md)
e siga TODAS as regras invioláveis e o termbase. Ele é a fonte de verdade.

## Passo 2 — Tarefa
{descricao}

ENTRADA (leia o arquivo inteiro antes de começar):
{entradas}

SAÍDA (crie/sobrescreva):
{saidas}

O texto de entrada é uma lição de análise de surtos em R, já convertida do formato
Carpentries/The Carpentries Workbench para o formato Quarto (callouts `::: {{.callout-...}}`).
Os títulos dos callouts já estão em português: não os altere.

## Regras extras para este trabalho
- No cabeçalho YAML (entre `---`), mantenha APENAS a linha `title:` traduzida. Remova
  `teaching:`, `exercises:`, `editor_options:` e qualquer linha `# jarl-ignore ...`.
- O arquivo de saída deve conter SOMENTE o conteúdo da lição traduzido. Não acrescente
  comentários seus, nem relatórios, nem blocos de código novos.
- Preserve exatamente a quantidade e a ordem dos blocos `::: {{.callout-...}}` do original.

## Como escrever o arquivo
Use a ferramenta Write para criar o arquivo de saída completo. Se o arquivo ficar grande e a
ferramenta reclamar, escreva em partes (primeira parte com Write, restante com `cat >> arquivo << 'EOF'`
no Bash ou com a ferramenta Edit), sempre com caminho absoluto.

## Checklist antes de terminar
1. Nenhum token de código R alterado (exceto comentários `#`).
2. Todos os blocos `::: {{.callout-...}}` preservados, com os mesmos títulos.
3. Saídas de console/erros do R preservados em inglês.
4. Nenhum número, link, referência ou dado inventado.
5. `wc -l` do arquivo de saída conferido.
6. Marcações `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` deixadas onde couber.

## Relatório final (texto curto)
- Caminhos absolutos dos arquivos escritos + número de linhas de cada um
- Lista das marcações `[verificar]` (com a linha e o motivo)
- Lista das sugestões `CONTEXTO-BR` (com a linha e a sugestão)
"""

for num, saida_rel, entrada_rel, desc in AGENTES:
    entradas = "\n".join(f"  - {ROOT}/{e.strip()}" for e in re.split(r"\s*\+\s*", entrada_rel))
    saidas = "\n".join(f"  - {ROOT}/{s.strip()}" for s in re.split(r"\s+e\s+|\s+", saida_rel) if s.strip())
    txt = PROMPT.format(root=ROOT, descricao=desc, entradas=entradas, saidas=saidas)
    (AG / f"prompt-{num}.md").write_text(txt, encoding="utf-8")

    sh = f"""#!/usr/bin/env bash
# Agente tradutor {num}
cd "{ROOT}" || exit 1
LOG="{AG}/log-{num}.txt"
agy --dangerously-skip-permissions --print-timeout 40m --print="$(cat '{AG}/prompt-{num}.md')" > "$LOG" 2>&1
echo "EXIT_AGENTE{num}=$?" >> "$LOG"
"""
    p = AG / f"run-{num}.sh"
    p.write_text(sh, encoding="utf-8")
    p.chmod(0o755)

print("Prompts e scripts gerados em", AG)
for f in sorted(AG.iterdir()):
    print(" ", f.name, f.stat().st_size, "bytes")
