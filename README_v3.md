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