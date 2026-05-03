# Análise técnica do projeto NutEV Master Pipeline v3

## Visão geral
Este repositório implementa um pipeline **end-to-end** para revisão de literatura e coleta documental em Nutrição/Estilo de Vida, com foco em:
- geração de consultas (query pack) por taxonomia;
- busca bibliográfica e busca web;
- crawling de fontes oficiais;
- download de documentos públicos;
- OCR/extração local;
- consolidação em planilhas para triagem (incluindo formato Rayyan).

## Estrutura observada
- **Script principal monolítico:** `nutev_master_pipeline_v3.py` (2.222 linhas; 84 funções).
- **Configuração de domínio:**
  - `nutev_keyword_taxonomy_v3.json` (taxonomia);
  - `nutev_official_sources_manifest_v3.json` (fontes oficiais).
- **Documentação de uso:** `README_v3.md`.
- **Saída operacional já presente:** árvore `NUTEV_MASTER_PROJECT` com querypacks, corpus e resultados.

## Arquitetura funcional (pipeline)
1. **Scaffold e paths padrão** (`scaffold_project`, `build_default_paths`).
2. **Carga de insumos** (taxonomia + manifesto de fontes).
3. **Geração de queries** (`build_query_pack`, `build_query_variants`, `build_web_queries`).
4. **Camadas de busca** (`run_search_layers`):
   - PubMed, EuropePMC, OpenAlex, Crossref, DOAJ;
   - Google CSE opcional;
   - fallback web por DDG HTML.
5. **Enriquecimento OA** (`enrich_with_unpaywall`).
6. **Crawler oficial** (`crawl_official_sources`).
7. **Downloads** (OA, web candidates, official seeds).
8. **Análise local e OCR** (`analyze_local_documents`, `extract_text_*`).
9. **Export final** (`write_outputs`) para CSV/XLSX e logs JSON.

## Pontos fortes
- Cobertura ampla de fontes com fallback resiliente.
- Design pragmático para ambientes sem credenciais Google.
- Múltiplos formatos locais suportados (PDF, DOCX, planilhas, HTML, imagens etc.).
- Deduplicação e escore de relevância orientados à triagem PRISMA.
- Organização consistente de outputs para auditoria e reprodutibilidade.

## Riscos e gargalos
- **Acoplamento alto:** toda a lógica em um único arquivo dificulta manutenção e testes unitários.
- **Tratamento de exceções genérico:** muitos `except Exception` com log simples reduzem observabilidade de causa-raiz.
- **Dependências opcionais dispersas:** sem validação central por modo (ex.: OCR, DOCX, ML) antes da execução.
- **Escalabilidade:** loops sequenciais com `sleep` e chamadas HTTP síncronas podem alongar execuções grandes.
- **Política de retry limitada:** faltam estratégias robustas para timeout/rate-limit por provedor.

## Oportunidades de melhoria (priorizadas)
1. **Modularização por domínio** (queries, search adapters, crawling, download, extraction, export).
2. **Camada de configuração tipada** (ex.: dataclass/pydantic para validação de parâmetros e defaults).
3. **Observabilidade estruturada** (logs JSON por etapa, métricas por fonte, erro classificado).
4. **Retries exponenciais com jitter** e orçamento por origem.
5. **Testes automatizados**:
   - unitários para parsers e normalização;
   - integração com fixtures HTTP/mock.
6. **Paralelismo controlado** para download e crawling (thread pool/async com rate-limit por domínio).

## Veredito
O projeto está funcionalmente robusto para uso aplicado em revisão de evidências e mineração documental pública. O principal próximo salto é de **engenharia de software** (modularidade, testes e observabilidade), mais do que de escopo funcional.
