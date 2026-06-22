.PHONY: help install dev test format lint clean run

help:
	@echo "📚 Automatizar Dossiê — Tarefas Disponíveis"
	@echo ""
	@echo "Instalação & Setup:"
	@echo "  make install        Instala dependências"
	@echo "  make dev            Instala dependências de desenvolvimento"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make run            Executa a aplicação (streamlit run main.py)"
	@echo "  make format         Formata código com Black"
	@echo "  make lint           Verifica qualidade de código com Ruff"
	@echo "  make test           Executa testes com pytest"
	@echo "  make coverage       Gera relatório de cobertura"
	@echo ""
	@echo "Manutenção:"
	@echo "  make clean          Remove arquivos temporários"
	@echo "  make freeze         Gera requirements.txt atualizado"
	@echo ""

install:
	pip install --upgrade pip
	pip install -r requirements.txt

dev:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"

run:
	streamlit run main.py

format:
	black app/ config/ tests/
	ruff check --fix app/ config/ tests/

lint:
	ruff check app/ config/ tests/
	black --check app/ config/ tests/

test:
	pytest -v

coverage:
	pytest --cov=app --cov-report=html
	@echo "✅ Relatório gerado em: htmlcov/index.html"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf .coverage htmlcov/
	rm -rf build/ dist/ *.egg-info/

freeze:
	pip freeze > requirements.txt
	@echo "✅ requirements.txt atualizado"

# Atalhos compostos
all: format lint test

setup: install dev
	@echo "✅ Environment pronto para desenvolvimento!"
	@echo "Execute: make run"