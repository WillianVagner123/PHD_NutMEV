# Roadmap de refatoracao segura

Este documento registra uma proposta pratica para continuar a evolucao do projeto sem quebrar a CLI atual.

## Objetivo

Reduzir o acoplamento do `nutev_master_pipeline_v3.py`, aumentar previsibilidade de execucao e facilitar testes incrementais.

## Prioridade 1 - Estado e checkpoints

Adicionar uma camada simples de estado por etapa:

- `07_logs/pipeline_state.json`
- status por stage: `pending`, `running`, `done`, `failed`, `skipped`
- timestamps de inicio/fim
- contadores principais: registros, downloads, erros

Beneficios:

- reexecutar sem perder progresso;
- diagnosticar quebra no meio do pipeline;
- permitir modo `--resume` no futuro.

## Prioridade 2 - Registro central de documentos

Criar um registro unico para URLs/documentos candidatos antes do download:

- URL canonica;
- URL origem/pai;
- tipo inferido;
- bucket de destino;
- status de download;
- hash quando disponivel.

Beneficios:

- evita downloads duplicados;
- separa descoberta de aquisicao;
- permite filtros por fonte, extensao e prioridade.

## Prioridade 3 - Extrair etapas do orquestrador

Migrar gradualmente funcoes do arquivo principal para modulos menores:

- `pipeline_state.py` - checkpoints, eventos e resumo;
- `document_registry.py` - deduplicacao/canonicalizacao de documentos;
- `local_extraction.py` - extracao textual e OCR;
- `outputs.py` - Excel, CSV, Rayyan e tabelas finais;
- `pipeline_cli.py` - parsing/validacao de argumentos.

Regra: manter `nutev_master_pipeline_v3.py` como entrypoint compativel.

## Prioridade 4 - Testes de regressao

Adicionar testes pequenos antes de cada migracao:

- canonicalizacao de URL;
- deteccao de extensao;
- deduplicacao de documentos;
- montagem de caminhos de saida;
- classificacao de documentos locais.

## Prioridade 5 - Qualidade operacional

Melhorias recomendadas:

- `--dry-run` para listar queries, seeds e destinos sem baixar;
- `--resume` para reaproveitar checkpoints;
- `--max-by-source` para limitar fontes barulhentas;
- `--fail-fast` opcional para CI;
- relatorio final em Markdown com resumo da execucao.

## Plano de execucao sugerido

1. Criar `pipeline_state.py` com testes.
2. Integrar estado sem mudar outputs existentes.
3. Criar `document_registry.py` com testes.
4. Conectar registro central ao crawler/download.
5. Separar extracao local e outputs.
6. Atualizar README e exemplos.

## Criterio de seguranca

Cada etapa deve preservar:

- nomes de arquivos de saida atuais;
- argumentos CLI existentes;
- formato das planilhas principais;
- comportamento padrao do comando documentado no README.
