# Pousada Bosque das Araucárias: site

Site da Pousada Bosque das Araucárias (Campos do Jordão, SP).

**Status:** protótipo em aprovação. Pré-visualização: https://luiztozi.github.io/pousada-bosque-das-araucarias/

## Estrutura

```
index.html       página única (HTML + CSS + um pouco de JavaScript)
fotos/           fotos otimizadas (máx. 1600 px, sem metadados)
logo.jpg         logo original enviado pela família
logo-claro.png   logo em creme, fundo transparente (topo e rodapé verdes)
favicon.png      ícone da aba do navegador
```

Não há framework, build nem dependências. O GitHub Pages publica o `index.html` como está.

## Ver no computador

Abrir o `index.html` no navegador, ou, dentro desta pasta:

```bash
python3 -m http.server 8765    # depois abrir http://127.0.0.1:8765
```

## Atualizar conteúdo

- **Nota e avaliações do Booking:** seção `AVALIACOES` no HTML e a lista `NOTAS` no JavaScript.
- **Galeria (carrossel):** lista `FOTOS` no JavaScript (arquivo + legenda), na ordem em que aparecem.
- **Comentários (carrossel):** copiar um `<blockquote class="depoimento">` inteiro na seção de avaliações e trocar texto e nome.
- **O que fazer:** lista `PASSEIOS` no JavaScript (nome, distância, descrição, busca no mapa).
- **Reserva direta:** o formulário só monta uma mensagem de WhatsApp para a gestora de reservas
  (Walkira Tozi, constante `WHATSAPP_RESERVAS`). Nada é confirmado pelo site. **Regra para evitar overbooking:**
  só confirmar ao hóspede depois de bloquear a data no painel do Booking.
- **Publicar:** `git add . && git commit -m "..." && git push`. O site atualiza em ~1 minuto.

## Fontes dos dados

- Nota, avaliações, tipos de quarto, regras e distâncias: [página da pousada no Booking.com](https://www.booking.com/hotel/br/pousada-bosque-das-araucarias.pt-br.html), consultada em 31/10/2026.
- WhatsApp e Instagram: informados pela família.
- E-mail e endereço: site antigo (e-mail a confirmar).
- "O que fazer", consultado em 31/10/2026:
  - Distâncias: lista "Proximidades da acomodação" do Booking.com (Vila Capivari: texto de descrição do Booking).
    O Booking dá 10,9 km para o Horto Florestal na descrição e 16 km na lista de proximidades; usamos a lista.
  - Parque Estadual / Horto: [SEMIL-SP](https://semil.sp.gov.br/12/parque-estadual-de-campos-do-jordao/).
  - Museu Felícia Leirner e Auditório Claudio Santoro: [site oficial](https://museufelicialeirner.org.br/exposicao-museu-visto-de-cima).
  - Palácio Boa Vista, Amantikir, teleférico, Capivari, Pico do Imbiri e Parque das Cerejeiras: guias e notícias de turismo
    (Guia da Semana, Melhores Destinos, Diário do Turismo, Gazeta SP, Wikivoyage).
  - Fora da lista: trem da EFCJ (operação incerta em 2026) e Cachoeira Véu da Noiva (fontes fracas).

## Antes do lançamento

- [ ] Remover a etiqueta `<meta name="robots" content="noindex, nofollow">`.
- [ ] Configurar o domínio `pousadabosquedasaraucarias.com.br` (Settings → Pages → Custom domain).

## Nota do Google atualizada todo mês

- **O quê:** `scripts/atualizar_nota_google.py` consulta a Places API (New) do Google e troca, no `index.html`, o texto "4,7 no Google · 216 avaliações". Se o resultado da busca não for a pousada, ele para sem alterar nada.
- **Quando:** `.github/workflows/atualizar-nota-google.yml` roda no dia 1 de cada mês (9h de Brasília). Para rodar na hora: aba **Actions** → "Atualizar nota do Google" → **Run workflow**.
- **Chave:** fica no segredo `GOOGLE_PLACES_KEY` do repositório (Settings → Secrets and variables → Actions). Nunca no código.
- **Rodar no computador:** `GOOGLE_PLACES_KEY=<chave> python scripts/atualizar_nota_google.py`
- **Booking:** não tem API pública; a nota, as categorias e os comentários do Booking são atualizados à mão.
