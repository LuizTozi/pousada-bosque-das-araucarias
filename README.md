# Pousada Bosque das Araucárias: site

Site da Pousada Bosque das Araucárias (Campos do Jordão, SP).

**Status:** protótipo em aprovação. Pré-visualização: https://luiztozi.github.io/pousada-bosque-das-araucarias/

## Estrutura

```
index.html   página única (HTML + CSS + um pouco de JavaScript)
fotos/       fotos otimizadas (máx. 1600 px, sem metadados)
```

Não há framework, build nem dependências. O GitHub Pages publica o `index.html` como está.

## Ver no computador

Abrir o `index.html` no navegador, ou, dentro desta pasta:

```bash
python3 -m http.server 8765    # depois abrir http://127.0.0.1:8765
```

## Atualizar conteúdo

- **Nota e avaliações do Booking:** seção `AVALIACOES` no HTML e a lista `NOTAS` no JavaScript.
- **Galeria:** lista `FOTOS` no JavaScript (arquivo + legenda).
- **Publicar:** `git add . && git commit -m "..." && git push`. O site atualiza em ~1 minuto.

## Fontes dos dados

- Nota, avaliações, tipos de quarto, regras e distâncias: [página da pousada no Booking.com](https://www.booking.com/hotel/br/pousada-bosque-das-araucarias.pt-br.html), consultada em 31/10/2026.
- WhatsApp e Instagram: informados pela família.
- E-mail e endereço: site antigo (e-mail a confirmar).

## Antes do lançamento

- [ ] Remover a etiqueta `<meta name="robots" content="noindex, nofollow">`.
- [ ] Configurar o domínio `pousadabosquedasaraucarias.com.br` (Settings → Pages → Custom domain).
