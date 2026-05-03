# NutEV Master Pipeline v3

Esta versão corrige o problema observado nos logs anteriores: o pipeline antigo coletava metadados, mas não descia para uma camada forte de **busca web + download + OCR + análise local**. Agora o fluxo padrão é:

1. criar pastas
2. gerar query pack
3. buscar em bases e na web
4. rastrear páginas e links públicos
5. baixar documentos
6. salvar HTMLs de páginas relevantes
7. fazer OCR/extração
8. montar tabelas finais

## Arquivos do pacote

- `nutev_master_pipeline_v3.py` -> script principal
- `nutev_keyword_taxonomy_v3.json` -> taxonomia editável
- `nutev_official_sources_manifest_v3.json` -> fontes oficiais/seeds
- `NUTEV_KEYWORDS_EDITABLE_v3.md` -> visão humana das palavras-chave
- `run_nutev_v3_windows.bat` -> exemplo de execução no Windows

## Instalação

```bash
pip install pandas openpyxl requests beautifulsoup4 pdfplumber pillow pytesseract python-docx scikit-learn
```

Instale também o **Tesseract OCR** no Windows.

## Execução padrão

```bash
python nutev_master_pipeline_v3.py --project-root NUTEV_MASTER_PROJECT --email seu_email@exemplo.com
```

Esse comando já faz:
- bases bibliográficas
- busca web ampla
- crawler oficial
- downloads públicos
- OCR/extracão
- tabelas finais

## Se você já tiver credenciais do Google Programmable Search / Custom Search JSON API

No Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="SUA_CHAVE"
$env:GOOGLE_CSE_ID="SEU_CX"
python .\nutev_master_pipeline_v3.py --project-root NUTEV_MASTER_PROJECT --email seu_email@exemplo.com
```

## Parâmetros úteis

Mais volume:
```bash
python nutev_master_pipeline_v3.py --project-root NUTEV_MASTER_PROJECT --email seu_email@exemplo.com --retmax 40 --web-retmax 15 --download-max 200 --crawl-pages 120 --crawl-links-per-page 30
```

Forçar OCR:
```bash
python nutev_master_pipeline_v3.py --project-root NUTEV_MASTER_PROJECT --email seu_email@exemplo.com --ocr-force
```

Desligar Google, mantendo busca web alternativa:
```bash
python nutev_master_pipeline_v3.py --project-root NUTEV_MASTER_PROJECT --email seu_email@exemplo.com --no-google
```

## Cobertura internacional da web (novo)

Sem depender de credenciais pagas, o pipeline agora amplia a busca para:
- DuckDuckGo HTML padrão;
- DuckDuckGo HTML em múltiplas localidades/idiomas (ex.: US, UK, BR, ES, FR, DE, JP, IN);
- Bing RSS em múltiplos países (ex.: US, BR, GB, ES, FR);
- Internet Archive (acervo global público).

Isso aumenta a chance de encontrar documentos em outros países e idiomas.

## Otimização de palavras-chave e combinações (novo)

O gerador de queries agora:
- ranqueia termos para priorizar expressões mais informativas (multi-palavra e menos ambíguas);
- combina blocos por rodízio para manter diversidade (clínico + padrão alimentar + implementação + tipo documental);
- inclui novas variantes focadas em evidência (`systematic_evidence`) e políticas/framework globais (`policy_global`).
- inclui auto-refino opcional de buscas web com `--self-refine-rounds` (usa termos minerados dos melhores resultados para nova rodada).
- inclui reranqueamento semântico opcional (`--semantic-rerank`) para priorizar resultados mais alinhados com a pergunta de pesquisa.

## Robustez de execução (novo)

- Retries exponenciais com jitter em chamadas HTTP (`safe_get`/`safe_post`);
- Eventos estruturados em JSON para observabilidade (`log_event`);
- Camada de configuração tipada (`PipelineConfig`) para centralizar defaults e validação inicial.
- Downloads com paralelismo controlado (`--download-workers`, 1 a 8) para acelerar coleta sem explosão de concorrência.
- Validação central de dependências por modo (`validate_runtime_dependencies`) com fail-fast para requisitos críticos.
- Classificação de erros (`classify_exception`) para diferenciar timeout/conexão/HTTP/parse nos logs.
- Política de retry por origem (`SOURCE_RETRY_POLICY`) com tratamento explícito para 429/5xx e respeito a `Retry-After`.

## Modularização inicial (novo)

Começamos a quebrar o monólito em módulos reutilizáveis sem mudar a CLI:
- `query_builder.py` (ranking/combinação e geração de queries web);
- `search_adapters.py` (classificação de exceções de busca);
- `download_pipeline.py` (executor paralelo de jobs de download).
- `crawler_pipeline.py` (extração de links candidatos a partir de páginas HTML).

Fase 2 em andamento:
- parsing/extração dos adapters DDG/Bing/Internet Archive foi deslocado para `search_adapters.py`, reduzindo a carga de parsing no arquivo principal.
- extração de candidatos de crawler web foi deslocada para `crawler_pipeline.py`.

## Testes automatizados (novo)

- Foram adicionados testes unitários iniciais para:
  - ranking/combinação de queries (`tests/test_query_builder.py`);
  - classificação de exceções (`tests/test_search_adapters.py`).
  - extração de links de crawler (`tests/test_crawler_pipeline.py`).

## Engenharia de software (v2)

- `pyproject.toml` com configuração de qualidade (pytest + ruff).
- `Makefile` com alvos `test`, `lint` e `check`.
- `CONTRIBUTING.md` com padrão de contribuição e validação mínima.
- CI em GitHub Actions (`.github/workflows/ci.yml`) com lint + testes automatizados em push/PR.

## Saídas principais

- `02_search_hits/normalized/NUTEV_SEARCH_MASTER.xlsx`
- `02_search_hits/rayyan_ready/NUTEV_RAYYAN_READY.csv`
- `02_search_hits/raw/NUTEV_DOWNLOAD_MANIFEST.csv`
- `05_extraction/NUTEV_LOCAL_ANALYSIS_v3.xlsx`
- `06_tables/NUTEV_MASTER_TABLES_v3.xlsx`

## Pastas do corpus

- `03A_bibliographic_oa`
- `03B_web_direct_docs`
- `03C_web_landing_pages`
- `03D_official_seed_docs`
- `03E_manual_drop`

## Observação

O script baixa **documentos públicos** e não tenta acessar material por login/paywall. Para OCR:
- PDFs escaneados -> OCR
- imagens -> OCR
- DOCX/XLSX/CSV/HTML/JSON/PPTX -> extração textual nativa
