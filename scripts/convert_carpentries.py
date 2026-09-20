#!/usr/bin/env python3
"""
Converte episódios do formato Carpentries Workbench (sandpaper) para Quarto.

- Divs cercados (: :: ::: questions / challenge / solution / ... ) -> callouts Quarto
- Ajusta caminhos de dados, imagens e links internos para o layout do site PT-BR
- Preserva 100% dos blocos de código (nada é alterado dentro de ``` ... ```)

Uso: python3 scripts/convert_carpentries.py <arquivo_entrada> <arquivo_saida>
"""
import re
import sys

# classe carpentries -> (tipo de callout quarto, titulo PT-BR, colapsado)
BLOCKS = {
    "questions":  ("note",      "Perguntas",             False),
    "objectives": ("tip",       "Objetivos",             False),
    "prereq":     ("important", "Pré-requisitos",        False),
    "spoiler":    ("note",      "Detalhes",              True),
    "callout":    ("note",      None,                    False),
    "challenge":  ("tip",       "Desafio",               False),
    "hint":       ("note",      "Dica",                  True),
    "solution":   ("note",      "Solução",               True),
    "checklist":  ("note",      "Checklist",             False),
    "caution":    ("warning",   "Atenção",               False),
    "discussion": ("note",      "Discussão",             False),
    "keypoints":  ("note",      "Pontos-chave",          False),
    "instructor": ("important", "Para o instrutor",      True),
    "checkpoint": ("note",      "Checagem",              False),
}

OPEN = re.compile(r"^(:{3,})\s*([A-Za-z][\w-]*)\s*$")
CLOSE = re.compile(r"^:{3,}\s*$")

# reescritas de links/caminhos (aplicadas fora dos blocos de código)
REWRITES = [
    (r"\(\.\./learners/setup\.md", "\(../setup.qmd"),
    (r"\(\.\./learners/reference\.md", "\(../glossario.qmd"),
    (r"\(reference\.md", "\(glossario.qmd"),
    (r"\(\.\./episodes/read-cases\.Rmd\)", "(01-ler-dados.qmd)"),
    (r"\(\.\./episodes/describe-cases\.Rmd\)", "(04-agregar-visualizar.qmd)"),
    (r"\(\.\./episodes/clean-data\.Rmd\)", "(02-limpar-dados.qmd)"),
    (r"\(\.\./episodes/tag-validate\.Rmd\)", "(03-validar-dados.qmd)"),
    (r"\(\.\./episodes/aggreagate-visualize\.Rmd\)", "(04-agregar-visualizar.qmd)"),
    (r'here::here\("episodes", *"data"', 'here::here("data"'),
    (r"hiperlink", "hiperlink"),
]

# links de download do site original -> arquivo local do repositório
DL = re.compile(r"https://epiverse-trace\.github\.io/tutorials-early/data/")
# imagens: fig/ -> ../img/ (episódios ficam em episodios/)
IMG = re.compile(r'(src="|\]\()(?P<p>(\.\./)?(episodes/)?fig/)(?P<f>[\w.\-]+\.(?:png|jpg|jpeg|svg))')


def convert(text: str, in_episodes_dir: bool) -> str:
    out, stack, in_code, in_tab = [], [], False, 0

    for line in text.split("\n"):
        # nunca tocar em blocos de código
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        m = OPEN.match(line)
        if m:
            cls = m.group(2).lower()
            if cls in BLOCKS:
                kind, title, collapse = BLOCKS[cls]
                if cls == "checklist" and m.group(1) == ":":  # não é div carpentries
                    pass
                attrs = f".callout-{kind}"
                if cls == "challenge":
                    attrs += " .desafio"
                if cls == "solution":
                    attrs += " .solucao"
                opts = ""
                if title:
                    opts += f' title="{title}"'
                if collapse:
                    opts += ' collapse="true"'
                out.append(f"::: {{{attrs}{opts}}}")
                stack.append(cls)
                in_tab += 1 if cls == "tab" else 0
                continue
            elif cls == "tab":
                out.append("::: {.panel-tabset}")
                stack.append("tab")
                in_tab += 1
                continue
            else:  # div genérica desconhecida -> mantém como div Quarto
                out.append(f"::: {{.{cls}}}")
                stack.append(cls)
                continue

        if CLOSE.match(line):
            if stack:
                stack.pop()
                if stack.count("tab") == 0:
                    in_tab = 0
                out.append(":::")
            # senão: linha decorativa de separação do carpentries -> remover
            continue

        # conteúdo normal
        if stack and stack[-1] == "tab" and re.match(r"^#{3,4} ", line):
            line = line[1:]  # ### Título -> ## Título (tabs do panel-tabset)
        for pat, rep in REWRITES:
            line = re.sub(pat, rep, line)
        line = DL.sub("../data/" if in_episodes_dir else "data/", line)
        line = IMG.sub(lambda mm: f"{mm.group(1)}{'../' if in_episodes_dir else ''}img/{mm.group('f')}", line)
        out.append(line)

    return "\n".join(out)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    in_episodes_dir = "/episodios/" in dst or sys.argv[3:] == ["episodes"]
    text = open(src, encoding="utf-8").read()
    res = convert(text, in_episodes_dir)
    open(dst, "w", encoding="utf-8").write(res)
    # relatório
    print(f"{src} -> {dst}: {len(text.splitlines())} -> {len(res.splitlines())} linhas")
    for name, (kind, title, _) in BLOCKS.items():
        a = len(re.findall(rf"^:{{3,}}\s*{name}\s*$", text, re.M))
        needle = f'title="{title}"' if title else f"{{{'.callout-' + kind}"
        b = res.count(needle)
        if a and b < a:
            print(f"  ATENCAO: {a} blocos '{name}' declarados, {b} convertidos")


if __name__ == "__main__":
    main()
