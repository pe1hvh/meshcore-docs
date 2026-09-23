"""MkDocs-hook: laat lijnregels in de tekst meeschalen met de schermbreedte.

Een aantal hoofdstukken gebruikt losse regels van `═` of `─` tekens als
scheidingslijn. De browser ziet zo'n reeks als één woord zonder breekpunt,
waardoor die op een smal scherm uit de tekstkolom steekt en de hele pagina
breder maakt.

Deze hook zet tijdens de build om elke regel binnen een alinea die 10 of meer
van die tekens bevat een <span class="domca-lijn">. De opmaak staat in
docs/stylesheets/extra.css. Codeblokken worden niet geraakt: daar staan geen
<p>-elementen. De markdown zelf blijft ongewijzigd.

Ingeschakeld via `hooks:` in mkdocs.yml.
"""

import re

ALINEA = re.compile(r"(<p\b[^>]*>)(.*?)(</p>)", re.S)
LIJN = re.compile(r"(?:─|═){10,}")


def _regel(regel: str) -> str:
    if LIJN.search(regel) and "<" not in regel:
        return f'<span class="domca-lijn">{regel}</span>'
    return regel


def on_page_content(html, **kwargs):
    return ALINEA.sub(
        lambda m: m[1] + "\n".join(map(_regel, m[2].split("\n"))) + m[3], html
    )
