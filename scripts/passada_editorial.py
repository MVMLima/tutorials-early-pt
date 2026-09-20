#!/usr/bin/env python3
"""
Passada editorial final sobre os arquivos traduzidos:

1. remove os comentários de trabalho deixados pelos agentes (`[verificar]` / `CONTEXTO-BR`)
2. insere as caixas "No Brasil" (conteúdo verificado pelo revisor humano)
3. corrige link relativo do glossário, comentários em inglês e o chunk que erra de propósito
"""
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent.parent

CAIXA_EP01 = """::: {.callout-note title="No Brasil: onde ficam os dados de casos"}

No Brasil, os dados de casos dos agravos de notificação compulsória são consolidados no **SINAN**
e publicados de forma aberta e anonimizada pelo DATASUS, na plataforma de dados abertos e na área
de *Transferência/Download de Arquivos*. Os arquivos são distribuídos por agravo, ano e unidade
federativa, no formato **DBC** (DBF compactado).

Para ler esses arquivos direto no R existe o pacote
[`{microdatasus}`](https://cran.r-project.org/package=microdatasus), que baixa, lê e pré-processa
os microdados do DATASUS, com funções específicas para SINAN, SIM, SINASC, SIH, SIA e CNES.
Fonte: [Ministério da Saúde — dados sobre agravos de notificação](https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/agravos-de-notificacoes/agravos-de-notificacoes).

Ao ler arquivos exportados de sistemas de vigilância, confira sempre o **separador** e a
**codificação** antes de importar: eles variam entre sistemas e entre versões.

:::

"""

CAIXA_EP02 = """::: {.callout-note title="No Brasil: formato de data"}

A convenção de escrita de datas no Brasil é **DD/MM/AAAA**, então, ao padronizar datas vindas de
sistemas de vigilância, o argumento `orders` costuma ser `c("dmy")`. Como este episódio mostra, o
caminho seguro é declarar explicitamente a ordem esperada em vez de deixar o R adivinhar.

:::

"""

CAIXA_EP03 = """::: {.callout-note title="No Brasil: o dicionário de dados do SINAN"}

Cada agravo do SINAN tem um **dicionário de dados** oficial publicado pela Secretaria de
Vigilância em Saúde, descrevendo o nome de cada campo da ficha, o tipo do campo e as categorias
possíveis. Ele fica na pasta *Documentação* da área de transferência de arquivos do DATASUS e é a
referência para decidir qual coluna marcar como identificador, como data de evento e como
desfecho no seu linelist. Fonte:
[Ministério da Saúde — agravos de notificação](https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/agravos-de-notificacoes/agravos-de-notificacoes).

:::

"""

CAIXA_EP04_SE = """::: {.callout-note title="No Brasil: semana epidemiológica"}

A vigilância brasileira agrega os dados por **Semana Epidemiológica (SE)**, que corresponde ao
`epiweek` do `{incidence2}`. Por convenção internacional, as semanas epidemiológicas são contadas
de **domingo a sábado**: a primeira semana do ano é a que contém o maior número de dias de
janeiro, e a última é a que contém o maior número de dias de dezembro. Fonte: *Caderno de Análise
— Roteiro para uso do SINAN Net* (SVS/MS, 2019), seção "Calendário Epidemiológico":
<https://portalsinan.saude.gov.br/images/documentos/Agravos/Violencia/CADERNO_ANALISE_SINAN_Marco_2019_V1.pdf>.

:::

"""

CAIXA_EP04_ATRASO = """::: {.callout-note title="No Brasil: dados preliminares e dados finais"}

Para o SINAN, o DATASUS publica duas bases: os **dados preliminares**, passíveis de atualização e
revisão pelas áreas técnicas responsáveis pela vigilância dos agravos, e os **dados finais**, que
não são mais atualizados para os anos já disponibilizados. É essa diferença de tempo entre o
registro e a consolidação que produz o atraso de notificação e a censura à direita nas últimas
semanas de uma curva epidêmica. Fonte:
[SINAN — instrucional para download de microdados](http://portalsinan.saude.gov.br/images/documentos/Agravos/microdados/INSTRUCIONAL_PARA_DOWNLOAD_DE_MICRODADOS_DO_SINAN.pdf).

:::

"""

# (arquivo, âncora, texto a inserir ANTES da âncora | None = substituir a âncora)
EDICOES = [
    ("episodios/01-ler-dados.qmd",
     "Este episódio demonstra como ler dados de casos de cada uma dessas fontes.",
     ("antes", CAIXA_EP01)),
    ("episodios/02-limpar-dados.qmd",
     "Participe da discussão sobre [este exemplo reproduzível](https://github.com/epiverse-trace/cleanepi/discussions/262).",
     ("depois", "\n\n" + CAIXA_EP02.rstrip())),
    ("episodios/03-validar-dados.qmd",
     "<!-- CONTEXTO-BR: No contexto das fichas do SINAN ou SIVEP-Gripe, as tags do {linelist} servem para mapear campos padronizados com siglas do sistema: id = \"NU_NOTIFIC\", date_onset = \"DT_SIN_PRI\", date_reporting = \"DT_NOTIFIC\", gender = \"CS_SEXO\", age = \"NU_IDADE_N\". -->",
     ("troca", CAIXA_EP03.rstrip())),
    ("episodios/04-agregar-visualizar.qmd",
     "<!-- CONTEXTO-BR: No Brasil, a vigilância epidemiológica organiza os dados por Semanas Epidemiológicas (SE), correspondentes ao intervalo 'epiweek' do {incidence2}, padrão",
     ("troca-prefixo", CAIXA_EP04_SE.rstrip())),
    ("episodios/04-agregar-visualizar.qmd",
     "<!-- CONTEXTO-BR: O atraso de notificação e digitação é uma realidade frequente no SINAN e no SIVEP-Gripe. Em surtos ativos, as últimas semanas epidemiológicas sofrem c",
     ("troca-prefixo", CAIXA_EP04_ATRASO.rstrip())),
]

# comentários/lixo que sai
SUBSTITUICOES = [
    ("episodios/02-limpar-dados.qmd", "](glossario.qmd#reportingdelay)", "](../glossario.qmd#reportingdelay)"),
    ("episodios/03-validar-dados.qmd",
     "```{r}\ncleaned_data %>%\n  # simular uma alteração no tipo de dados em uma variável",
     "```{r, error=TRUE}\ncleaned_data %>%\n  # simular uma alteração no tipo de dados em uma variável"),
    ("setup.qmd", "<!--\nDuring the tutorial, we will need a number of R packages. Packages contain useful R code written by other people. We will use packages from the [Epiverse-TRACE](https://epiverse-trace.github.io/).\n-->\n\n", ""),
    ("setup.qmd", "<!-- 4. Configure the Multi-factor Authentication (see below).-->\n", ""),
]

# remove comentários de trabalho dos agentes
MARCADOR = re.compile(r"[ \t]*<!--\s*(?:\[verificar|CONTEXTO-BR)[^\n]*?-->\n?")


def main() -> None:
    # 1. caixas
    for rel, ancora, (modo, texto) in EDICOES:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        if modo == "troca-prefixo":
            linhas = txt.split("\n")
            achou = False
            for i, linha in enumerate(linhas):
                if linha.startswith(ancora):
                    linhas[i] = texto
                    achou = True
                    break
            if not achou:
                print(f"FALHA âncora em {rel}: {ancora[:60]}")
                continue
            p.write_text("\n".join(linhas), encoding="utf-8")
        else:
            if ancora not in txt:
                print(f"FALHA âncora em {rel}: {ancora[:60]}")
                continue
            novo = (texto.rstrip() + "\n\n" + ancora) if modo == "antes" else \
                   (ancora + texto.rstrip() + "\n") if modo == "depois" else texto
            p.write_text(txt.replace(ancora, novo, 1), encoding="utf-8")
        print(f"caixa inserida em {rel}")

    # 2. substituições pontuais
    for rel, de, para in SUBSTITUICOES:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        if de not in txt:
            print(f"FALHA substituição em {rel}: {de[:60]}")
            continue
        p.write_text(txt.replace(de, para, 1), encoding="utf-8")
        print(f"substituição aplicada em {rel}")

    # 3. limpeza dos marcadores restantes
    for p in sorted(list(P.glob("*.qmd")) + list(P.glob("episodios/*.qmd"))):
        txt = p.read_text(encoding="utf-8")
        novo = MARCADOR.sub("", txt)
        if novo != txt:
            p.write_text(novo, encoding="utf-8")
            print(f"marcadores removidos de {p.relative_to(P)}")


if __name__ == "__main__":
    main()
