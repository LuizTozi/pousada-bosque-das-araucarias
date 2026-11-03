"""Atualiza no index.html a nota e o total de avaliações da pousada no Google.

Fonte: Places API (New) do Google, pesquisa por texto (places:searchText).
A chave vem da variável de ambiente GOOGLE_PLACES_KEY; nunca fica no código.
Só altera o site se a nota ou o total tiverem mudado.

Uso:  GOOGLE_PLACES_KEY=... python scripts/atualizar_nota_google.py
"""

import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

URL_BUSCA = "https://places.googleapis.com/v1/places:searchText"
TEXTO_BUSCA = "Pousada Bosque das Araucárias, Campos do Jordão"
NOME_ESPERADO = "Pousada Bosque das Araucárias"
CIDADE_ESPERADA = "Campos do Jordão"
ARQUIVO_SITE = Path(__file__).resolve().parent.parent / "index.html"

# Trechos do index.html que o script troca (cada um precisa existir uma única vez)
PADRAO_NOTA = re.compile(r'(<span class="nota-google">)[^<]*(</span>)')
PADRAO_DATA = re.compile(r"(<!-- Google: nota e total alterados em )[0-9-]+( -->)")


def buscar_lugar(chave: str) -> dict:
    """Pergunta ao Google pela pousada e devolve os dados do primeiro resultado."""
    corpo = json.dumps({"textQuery": TEXTO_BUSCA, "languageCode": "pt-BR"}).encode()
    pedido = urllib.request.Request(URL_BUSCA, data=corpo, method="POST", headers={
        "Content-Type": "application/json",
        "X-Goog-Api-Key": chave,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,"
                            "places.rating,places.userRatingCount",
    })
    try:
        with urllib.request.urlopen(pedido, timeout=30) as resposta:
            dados = json.load(resposta)
    except urllib.error.HTTPError as erro:
        sys.exit(f"Erro {erro.code} da Places API: {erro.read().decode(errors='replace')}")

    lugares = dados.get("places", [])
    if not lugares:
        sys.exit(f"A busca por '{TEXTO_BUSCA}' não retornou nenhum lugar.")
    return lugares[0]


def conferir_lugar(lugar: dict) -> None:
    """Para tudo se o resultado não for a pousada (evita gravar a nota de outro lugar)."""
    nome = lugar.get("displayName", {}).get("text", "")
    endereco = lugar.get("formattedAddress", "")
    if nome != NOME_ESPERADO or CIDADE_ESPERADA not in endereco:
        sys.exit(f"Resultado inesperado: '{nome}' em '{endereco}'. Nada foi alterado.")
    if "rating" not in lugar or "userRatingCount" not in lugar:
        sys.exit(f"O Google não devolveu nota/total para '{nome}'. Nada foi alterado.")


def formatar(nota: float, total: int) -> str:
    """4.7 e 1216 viram '4,7 no Google · 1.216 avaliações'."""
    nota_br = f"{nota:.1f}".replace(".", ",")
    total_br = f"{total:,}".replace(",", ".")
    return f"{nota_br} no Google · {total_br} avaliações"


def trocar_uma_vez(padrao: re.Pattern, novo_miolo: str, html: str) -> str:
    novo_html, quantidade = padrao.subn(rf"\g<1>{novo_miolo}\g<2>", html)
    if quantidade != 1:
        sys.exit(f"Esperava 1 trecho '{padrao.pattern}' no index.html, achei {quantidade}.")
    return novo_html


def main() -> None:
    chave = os.environ.get("GOOGLE_PLACES_KEY", "").strip()
    if not chave:
        sys.exit("Falta a variável de ambiente GOOGLE_PLACES_KEY.")

    lugar = buscar_lugar(chave)
    conferir_lugar(lugar)
    texto_novo = formatar(lugar["rating"], lugar["userRatingCount"])

    html = ARQUIVO_SITE.read_text(encoding="utf-8")
    texto_atual = PADRAO_NOTA.search(html)
    if texto_atual and f">{texto_novo}<" in texto_atual.group(0):
        print(f"Sem mudança: {texto_novo}")
        return

    html = trocar_uma_vez(PADRAO_NOTA, texto_novo, html)
    html = trocar_uma_vez(PADRAO_DATA, datetime.date.today().isoformat(), html)
    ARQUIVO_SITE.write_text(html, encoding="utf-8")
    print(f"Atualizado: {texto_novo} (lugar {lugar['id']})")


if __name__ == "__main__":
    main()
