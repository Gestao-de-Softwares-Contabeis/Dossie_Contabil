# ⚡ Guia Rápido — Começar em 5 Minutos

Instruções mínimas para rodar a aplicação localmente.

---

## 1️⃣ Pré-requisitos

```bash
# Verificar Python 3.10+
python --version

# Verificar pip
pip --version

# Instalar Pandoc (necessário!)
# Linux:
sudo apt-get install pandoc

# macOS:
brew install pandoc

# Windows: Baixe em https://pandoc.org/installing.html
```

---

## 2️⃣ Clonar & Instalar

```bash
# Clone o repositório
git clone https://github.com/camposs04/Automatizar_Dossie.git
cd Automatizar_Dossie

# Crie virtual environment
python -m venv venv

# Ative (escolha seu SO)
source venv/bin/activate           # Linux/macOS
# ou
venv\Scripts\activate              # Windows

# Instale dependências
pip install -r requirements.txt
```

---

## 3️⃣ Configure (Opcional)

Se quiser usar n8n ou outras integrações:

```bash
# Copie o template de variáveis
cp .env.example .env

# Edite .env com seus valores
nano .env  # ou seu editor favorito
```

---

## 4️⃣ Execute

```bash
# Rodar aplicação
streamlit run main.py

# Abrirá em http://localhost:8501
```

---

## 5️⃣ Teste (Opcional)

```bash
# Executar testes
pytest tests/ -v

# Com cobertura
pytest --cov=app tests/
```

---

## 🎯 Próximos Passos

- [ ] Leia `README.md` para visão geral completa
- [ ] Leia `DEVELOPMENT.md` se vai modificar código
- [ ] Consulte `STRUCTURE.md` para entender a organização
- [ ] Veja `CONTRIBUTING.md` se vai contribuir

---

## 🐛 Problemas?

### "Pandoc not found"
→ Instale Pandoc (veja pré-requisitos acima)

### "ModuleNotFoundError: No module named 'streamlit'"
→ Rodou `pip install -r requirements.txt`? Tente novamente

### "template_base_ofc.docx not found"
→ O arquivo template precisa estar no repositório (envie manualmente ao GitHub)

### Mais ajuda?
→ Veja seção "Troubleshooting" em `README.md`

---

## 📞 Ambiente Pronto?

Perfeito! Agora:

1. Preencha os formulários
2. Faça upload dos 4 arquivos (Balanço, DRE, Notas, Carta)
3. Clique em "✅ GERAR DOSSIÊ"
4. Baixe o resultado! 🎉

---

**Happy generating!** 🚀