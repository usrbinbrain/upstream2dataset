# upstream2dataset

## Descrição

O **upstream2dataset** e uma ferramenta Python que usa a API do GitHub para extrair a arvore de arquivos de um repositorio e branch, e gerar um dataset com o caminho e conteudo de cada arquivo.

Agora o script suporta **dois formatos de saida**:
- `txt` (padrao)
- `json` (opcional)

---

## Funcionalidades

- **Extracao da arvore do repositorio:** consulta recursiva via endpoint de tree do GitHub (`recursive=true`).
- **Coleta de conteudo de arquivos:** para cada item `blob`, busca e decodifica o conteudo em Base64.
- **Geracao de dataset em TXT ou JSON:**
  - `txt`: formato textual legivel
  - `json`: estrutura pronta para pipelines/datasets
- **Metadados por arquivo no JSON:** `path`, `content`, `sha`, `size`.
- **Filtros customizaveis:** possibilidade de adaptar a selecao dos arquivos editando o trecho de filtro no codigo.

---

## Requisitos

- **Python 3.x**
- Biblioteca **requests** (`pip install requests`)
- **GitHub Personal Access Token (gh_pat)** com permissao para leitura do repositorio alvo

---

## Instalacao e Uso

```bash
1. Clone o repositorio
git clone https://github.com/usrbinbrain/upstream2dataset.git

2. Instale dependencias
pip3 install requests

3. Execute o script
python3 upstream2dataset/upstream2dataset.py <repository_name> <branch> <gh_pat> [txt|json]
```

---

## Parametros

- **`<repository_name>`**: repositorio no formato `owner/repository` (ex.: `oracle/oci-python-sdk`)
- **`<branch>`**: branch alvo (ex.: `main`, `master`)
- **`<gh_pat>`**: token pessoal do GitHub
- **`[txt|json]`** (opcional): formato de saida
  - `txt` = padrao
  - `json` = saida estruturada em JSON

---

## Exemplos de Execucao

### Saida TXT (padrao)

```bash
python3 upstream2dataset.py "github-acc/github-repo" "main" "ghp_zzzzzzzzzzzzzzzzzz"
```

Tambem funciona explicitando:
```bash
python3 upstream2dataset.py "github-acc/github-repo" "main" "ghp_zzzzzzzzzzzzzzzzzz" txt
```

Arquivo gerado:
`github-acc@github-repo-main_FullDataset.txt`

### Saida JSON

```bash
python3 upstream2dataset.py "github-acc/github-repo" "main" "ghp_zzzzzzzzzzzzzzzzzz" json
```

Arquivo gerado:
`github-acc@github-repo-main_FullDataset.json`

---

## Formato de Saida TXT

Exemplo simplificado:

```text
Project repo Name: github-acc/github-repo
Project repo Branch: main

File Name: README.md
File README.md Content:
<file content>

File Name: src/app.py
File src/app.py Content:
<file content>
```

---

## Formato de Saida JSON

Exemplo simplificado:

```json
{
  "repo": "github-acc/github-repo",
  "branch": "main",
  "files": [
    {
      "path": "README.md",
      "content": "<file content>",
      "sha": "abc123...",
      "size": 1024
    },
    {
      "path": "src/app.py",
      "content": "<file content>",
      "sha": "def456...",
      "size": 2048
    }
  ]
}
```

---

## Funcionamento Interno

1. **Busca da arvore do repositorio**  
   Monta a URL da API:
   `https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=true`

2. **Iteracao dos itens**  
   Percorre `tree` e processa itens com `type == "blob"`.

3. **Download e decodificacao**  
   Para cada arquivo, consulta a URL do blob, decodifica Base64 e armazena conteudo.

4. **Geracao do arquivo final**  
   Escreve em `.txt` ou `.json`, conforme argumento opcional `[txt|json]`.

---

## Customizacao de Filtros

No trecho de filtro em upstream2dataset.py, voce pode ajustar para:
- apenas arquivos de uma pasta (`src`, `examples`, etc.)
- apenas extensoes especificas (`.py`, `.md`, etc.)

Atualmente, o script processa todos os arquivos encontrados na arvore.

---

## Observacoes

- O script pode gerar arquivos grandes para repositorios extensos.
- Pode haver falha em alguns blobs individuais; nesses casos, o script registra erro e continua.
- O nome do arquivo de saida segue o padrao:
  - `owner@repo-branch_FullDataset.txt`
  - `owner@repo-branch_FullDataset.json`
