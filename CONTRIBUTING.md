# Contribuindo

## Padrão de engenharia adotado
- Testes antes de merge (`python -m pytest tests`).
- Lint estático com Ruff (`ruff check .`).
- Logs estruturados JSON para erros e eventos.
- Alterações de módulos devem incluir testes unitários.

## Fluxo recomendado
1. Crie branch de feature.
2. Implemente com funções pequenas e tipadas.
3. Rode `make check`.
4. Abra PR com motivação, impacto e validação.
