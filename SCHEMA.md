# SCHEMA — Formato de Lição (`licao-XX.json`)

Cada lição é um arquivo JSON em `licoes/`. Após editar, rode `python build-mobile.py` para atualizar `manifest.js`.

---

## Estrutura raiz

```jsonc
{
  "id":     "licao-01-verbos-movimento",   // slug único; nunca mude depois de criado
  "titulo": "Verbos de Movimento",          // exibido na tela inicial
  "modulo": 2,                              // número do módulo da aula
  "fonte":  "Fundo de Bolsas 1-6-26",      // referência ao material-fonte
  "vocab":      [ /* VocabItem */  ],
  "exercicios": [ /* Exercicio */ ]
}
```

---

## VocabItem

```jsonc
{
  "id":      "v-holekh",       // slug estável = "v-" + transliteração sem espaços/acentos
  "heb":     "הוֹלֵךְ",        // texto hebraico (com ou sem nikud — seja consistente)
  "translit":"holekh",         // pronúncia em ABNTph / padrão do livro
  "pt":      "ir (masc. sing.)",
  "cat":     "verbos"          // verbos | substantivos | preposicoes | adverbios | acronimos | ...
}
```

**Regra de ID:** o motor persiste o progresso por `vocab.id`. Nunca renomeie um id após ter estudado a lição.

---

## Exercicios

Todos os tipos compartilham:

```jsonc
{
  "id":   "ex-01-parear",    // slug único dentro da lição
  "tipo": "...",             // ver tipos abaixo
  ...campos específicos do tipo...
}
```

### `multipla_escolha` (exercício manual explícito)

> Os exercícios de vocabulário (`VocabItem`) geram **automaticamente** dois exercícios de múltipla escolha (heb→pt e pt→heb). Use este tipo apenas para perguntas contextuais especiais que não são deriváveis do vocabulário.

```jsonc
{
  "tipo": "multipla_escolha",
  "instrucao": "Qual forma usar para 'elas vêm'?",
  "pergunta_heb": "elas vêm",           // ou pergunta_pt / pergunta_heb
  "opcoes": [
    { "id": "a", "texto": "בָּאוֹת", "correta": true  },
    { "id": "b", "texto": "בָּאִים", "correta": false },
    { "id": "c", "texto": "בָּא",    "correta": false },
    { "id": "d", "texto": "בָּאָה",  "correta": false }
  ]
}
```

### `montar_frase`

O usuário toca nas peças do banco para montar a frase na ordem certa.

```jsonc
{
  "tipo": "montar_frase",
  "instrucao": "Monte a frase em hebraico:",
  "frase_pt":  "Ela vem da sala de aula",
  "frase_heb": "הִיא בָּאָה מֵהַכִּיתָה",   // resposta exata (tokenizada por espaços)
  "banco": [                                 // tiles disponíveis — inclua distratores
    "הִיא", "בָּאָה", "מֵהַכִּיתָה",
    "הוּא", "הוֹלֶכֶת", "לַכִּיתָה"
  ]
}
```

**Importante:** a comparação é `tiles_escolhidos.join(' ') === frase_heb`. Garanta que as palavras no banco, quando concatenadas com espaço, formem exatamente `frase_heb`.

### `lacuna`

O usuário escolhe a palavra que preenche o espaço em branco.

```jsonc
{
  "tipo": "lacuna",
  "instrucao": "Complete com o verbo correto:",
  "template":  "אֲנִי ___ לַבַּנְק",   // use ___ (três underscores) para a lacuna
  "traducao":  "Eu vou para o banco",   // dica em português (opcional)
  "opcoes":    ["הוֹלֵךְ", "הוֹלֶכֶת", "בָּאָה", "בָּא"],
  "resposta":  "הוֹלֵךְ"
}
```

### `parear`

O usuário conecta cada item da coluna esquerda ao seu par na coluna direita.

```jsonc
{
  "tipo": "parear",
  "instrucao": "Conecte cada forma verbal à sua tradução:",
  "pares": [
    ["בָּא",    "vir (masc.)"],
    ["בָּאָה",  "vir (fem.)"],
    ["הוֹלֵךְ", "ir (masc.)"],
    ["הוֹלֶכֶת","ir (fem.)"]
  ]
}
```

Máximo recomendado: **5 pares** (UX mobile).

---

## Convenções de ID

| Prefixo | Uso |
|---------|-----|
| `v-`    | vocab item (`v-holekh`) |
| `ex-`   | exercício manual (`ex-01-parear`) |

Slug de vocab: `v-` + transliteração minúscula sem acentos, apóstrofos ou espaços.
- "ba'a" → `v-baa`
- "holekh" → `v-holekh`
- "sha'ah" → `v-shaah`

---

## localStorage

| Chave | Escopo | Formato |
|-------|--------|---------|
| `heb_trainer_vocab_v1` | global | `{ "v-ba": { correct, wrong, streak, mastered } }` |
| `heb_trainer_licoes_v1` | por lição | `{ "licao-01": { "ex-01": { correct, wrong } } }` |

Domínio de vocabulário: `streak >= 5` → `mastered: true` → sai do pool de exercícios automáticos.
