# CLAUDE.md — Hebraico Trainer Playbook

## Visão geral do projeto

Motor único de lições para estudo de hebraico. Cada lição é um JSON em `licoes/`. O app carrega via `licoes/manifest.js` (gerado por `build-mobile.py`). Progresso em `localStorage`: vocab global (`heb_trainer_vocab_v1`), exercícios por lição (`heb_trainer_licoes_v1`).

```
hebraico-trainer/
├── index.html                  ← SPA completo (motor + UI inline)
├── licoes/
│   ├── manifest.js             ← gerado por build-mobile.py — não edite
│   └── licao-01-verbos-movimento.json
├── SCHEMA.md                   ← formato detalhado de cada campo
├── CLAUDE.md                   ← este arquivo
├── build-mobile.py             ← atualiza manifest.js + gera mobile HTML
└── .gitignore
```

---

## Fluxo: foto do livro → lição JSON

### 1. O usuário manda a foto

Envie a imagem da página (ou trecho digitado) e diga algo como:
> "Gera a lição para esta página. É da aula X, fonte: Fundo de Bolsas DD-MM."

### 2. O que extrair da imagem

| Visto na página | Tipo de exercício a gerar |
|-----------------|--------------------------|
| Tabela de palavras com tradução | `vocab[]` + `multipla_escolha` automático |
| Frase para reordenar / completar | `montar_frase` |
| Frase com lacuna / preposição a preencher | `lacuna` |
| Diálogo ou pares pergunta/resposta | `parear` ou `multipla_escolha` explícito |
| Conjugação verbal (tabela masculino/feminino) | Vários `VocabItem` + exercício `parear` |

### 3. Gerar o JSON

Crie `licoes/licao-NN-slug.json` seguindo o SCHEMA.md. Regras:

- **`vocab.id`** = `v-` + transliteração sem acentos/apóstrofos (`ba'a` → `v-baa`)
- **`exercicio.id`** = `ex-NN-tipo` (ex: `ex-01-parear`, `ex-02-montar`)
- Para conjugações, crie um item de vocab por forma (masc, fem, masc-pl, fem-pl)
- Inclua distratores plausíveis nos bancos de palavras (`montar_frase`) — formas da mesma raiz verbal, preposições trocadas, etc.
- Para `lacuna`, 3-4 opções são suficientes
- Para `parear`, máximo 5 pares (UX mobile)

### 4. Registrar a lição

Após criar o JSON, rode:
```bash
cd hebraico-trainer
python build-mobile.py
```

Isso atualiza `manifest.js` (o app vai listar a nova lição) e gera `hebraico-trainer-mobile.html`.

### 5. Commit e push

```bash
git add licoes/licao-NN-slug.json licoes/manifest.js
git commit -m "feat: lição NN — título da lição"
git push
```

O GitHub Pages publica automaticamente em ~1 minuto.

---

## Publicar / atualizar no GitHub Pages

### Primeira publicação

```bash
cd hebraico-trainer

# 1. Criar o repositório no GitHub (interface web ou gh CLI)
# Via browser: github.com/new → nome: hebraico-trainer → Public → Create

# 2. Conectar e fazer push
git remote add origin https://github.com/SEU_USUARIO/hebraico-trainer.git
git branch -M main
git push -u origin main

# 3. Ativar GitHub Pages
# Acesse: github.com/SEU_USUARIO/hebraico-trainer/settings/pages
# Source: Deploy from branch → Branch: main → / (root) → Save
```

URL do app: `https://SEU_USUARIO.github.io/hebraico-trainer/`

### Atualizar uma lição existente

```bash
# Edite o JSON, depois:
python build-mobile.py          # atualiza manifest.js
git add licoes/ 
git commit -m "update: lição XX — descrição da mudança"
git push
```

### Adicionar uma lição nova

```bash
# 1. Crie licoes/licao-NN-slug.json  (conforme SCHEMA.md)
python build-mobile.py
git add licoes/licao-NN-slug.json licoes/manifest.js
git commit -m "feat: lição NN — título"
git push
```

### Gerar o arquivo mobile (offline)

```bash
python build-mobile.py
# Abre: hebraico-trainer-mobile.html no navegador
# Ou envia o arquivo para o iPhone via AirDrop / e-mail
```

---

## Tipos de exercício — referência rápida

| Tipo | Gerado por | Quando usar |
|------|-----------|-------------|
| `multipla_escolha` heb→pt | Motor (automático) | Todo `vocab[]` gera este |
| `multipla_escolha` pt→heb | Motor (automático) | Todo `vocab[]` não-dominado gera este |
| `montar_frase` | JSON (`exercicios[]`) | Frase do livro para reordenar |
| `lacuna` | JSON (`exercicios[]`) | Preencher preposição/conjugação |
| `parear` | JSON (`exercicios[]`) | Conectar formas a traduções |

---

## Spaced repetition — resumo

- **Prioridade de exercício** = `100 + erros×10 − acertos` (mais erros = aparece primeiro)
- **Domínio de vocab** = streak ≥ 5 acertos consecutivos → `mastered: true` → sai do pool automático
- Progresso de vocab é **global** (dominar "בָּא" em lição 1 vale para lição 3)
- Progresso de exercícios de frase é **local por lição**

---

## Convenções de commit

```
feat: lição NN — título         (nova lição)
update: lição NN — descrição    (edição de lição existente)
fix: bug no renderer de lacuna  (correção no motor)
chore: atualiza manifest.js     (só build)
```
