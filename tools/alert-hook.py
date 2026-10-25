"""MkDocs-hook: zet GitHub-meldingen om naar admonitions van Material.

De Markdown gebruikt de schrijfwijze van GitHub voor meldingen:

    > [!NOTE]
    > **Bron.** Deze pagina is geverifieerd tegen ...

GitHub toont dat als een gekleurd kader. MkDocs kent die schrijfwijze niet en
toonde het als een grijs citaat met de tekst "[!NOTE]" erin, slecht leesbaar
op een telefoon. Deze hook zet zo'n blok tijdens de build om naar een
admonition:

    !!! note "Opmerking"

        **Bron.** Deze pagina is geverifieerd tegen ...

De Markdown zelf blijft ongewijzigd, zodat de bestanden op GitHub goed blijven
werken. Blokken binnen een codeblok (``` of ~~~) worden niet geraakt.

De kop komt in de taal van de pagina (docs/nl/ of docs/en/).

Ingeschakeld via `hooks:` in mkdocs.yml.
"""

import re

KOP = re.compile(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
HEK = re.compile(r"^\s*(`{3,}|~{3,})")

# GitHub-soort -> (soort in Material, kop NL, kop EN)
SOORT = {
    "NOTE": ("note", "Opmerking", "Note"),
    "TIP": ("tip", "Tip", "Tip"),
    "IMPORTANT": ("info", "Belangrijk", "Important"),
    "WARNING": ("warning", "Waarschuwing", "Warning"),
    "CAUTION": ("danger", "Let op", "Caution"),
}


def omzetten(markdown: str, engels: bool) -> str:
    """Geef de markdown terug met elk GitHub-meldingsblok als admonition."""
    regels = markdown.split("\n")
    uit = []
    hek = None  # het openende hek van het codeblok waarin we staan
    i = 0
    while i < len(regels):
        regel = regels[i]

        m = HEK.match(regel)
        if m:
            teken = m[1]
            if hek is None:
                hek = teken
            elif teken[0] == hek[0] and len(teken) >= len(hek):
                hek = None
            uit.append(regel)
            i += 1
            continue

        k = KOP.match(regel) if hek is None else None
        if not k:
            uit.append(regel)
            i += 1
            continue

        soort, nl, en = SOORT[k[1]]
        if uit and uit[-1].strip():
            uit.append("")
        uit.append(f'!!! {soort} "{en if engels else nl}"')
        uit.append("")
        i += 1
        while i < len(regels) and regels[i].startswith(">"):
            tekst = regels[i][1:]
            if tekst.startswith(" "):
                tekst = tekst[1:]
            uit.append("    " + tekst if tekst.strip() else "")
            i += 1
        uit.append("")
    return "\n".join(uit)


def on_page_markdown(markdown, page, **kwargs):
    engels = page.file.src_uri.startswith("en/")
    return omzetten(markdown, engels)
