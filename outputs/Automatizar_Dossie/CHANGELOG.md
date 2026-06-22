# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

---

## [1.1.0] — 2024-06-19

### Added

- ✨ Refatoração completa em arquitetura modular
- ✨ Classe `DossieAutomation` para orquestração centralizada
- ✨ Classe `FileProcessor` para processamento de PDFs e DOCXs
- ✨ Módulo `utils/helpers.py` com funções de formatação e validação
- ✨ Logging centralizado com `loguru`
- ✨ Suite completa de testes com pytest
- ✨ Arquivo `.devcontainer/devcontainer.json` para desenvolvimento com Visual Studio Code
- ✨ Documentação extensiva (README, CONTRIBUTING, pyproject.toml)
- ✨ Support para type hints em todo o código base

### Changed

- 🔄 Refator de `app_gerador.py` → `app/main.py`
- 🔄 Separação clara: core (negócio), utils (helpers), config
- 🔄 Melhor estrutura de configuração (environment variables + constants)
- 🔄 Validação de CNPJ e CPF com algoritmos oficiais
- 🔄 Mensagens de erro mais descritivas

### Fixed

- 🐛 Tratamento de erros de arquivo não encontrado
- 🐛 Cleanup de arquivos temporários mais robusto
- 🐛 Logging de operações críticas

---

## [1.0.0] — 2024-01-15

### Added

- 🎉 Versão inicial do Gerador de Dossiês Contábeis
- 🎉 Interface Streamlit com 3 abas (Empresa, Sócios, Uploads)
- 🎉 Processamento automático de PDFs (Balanço + DRE)
- 🎉 Inserção dinâmica de conteúdo DOCX (Notas + Carta)
- 🎉 Template DOCX com Jinja2
- 🎉 Integração com webhooks n8n
- 🎉 Formatação automática de CNPJ e CPF
- 🎉 Deploy no Streamlit Cloud

---

## [0.1.0] — 2023-12-01

### Added

- 📝 Estrutura inicial do projeto
- 📝 Prototipagem da interface
- 📝 Testes manuais

---

## Como usar este changelog

### Adicionando uma entrada

Ao fazer um PR ou release, adicione uma entrada na seção **[Unreleased]**:

```markdown
### Added
- ✨ Novo suporte para XLS (balanço em Excel)
- ✨ Validação de assinatura digital

### Fixed
- 🐛 Corrige erro de encoding em nomes com acentos
```

Após fazer o release, mova a seção [Unreleased] para a versão (ex: [1.2.0]).

### Categorias

- **Added:** Novas features
- **Changed:** Mudanças em features existentes
- **Deprecated:** Features que serão removidas em breve
- **Removed:** Features removidas
- **Fixed:** Bug fixes
- **Security:** Fixes de segurança

---

## Versionamento

Seguimos [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Mudanças incompatíveis (breaking)
- **MINOR** (1.0.0 → 1.1.0): Novas features (backward-compatible)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes (backward-compatible)

Exemplo:
- `1.1.0`: Refatoração + novas features
- `1.1.1`: Bug fix leve
- `2.0.0`: Rewrite total ou mudança de arquitetura

---

## Links de Versão

- **v1.1.0:** [GitHub Release](https://github.com/camposs04/Automatizar_Dossie/releases/tag/v1.1.0)
- **v1.0.0:** [GitHub Release](https://github.com/camposs04/Automatizar_Dossie/releases/tag/v1.0.0)