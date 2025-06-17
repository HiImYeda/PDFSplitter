# 🚀 PDF Splitter API - FastAPI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Uma API moderna e rápida para dividir PDFs e converter HTML para PDF, construída com **FastAPI**.

## ✨ Funcionalidades

- 📄 **Divisão de PDF**: Divide PDFs em páginas individuais
- 🌐 **HTML para PDF**: Converte conteúdo HTML em PDF de alta qualidade
- 🖼️ **PDF para Imagem**: Gera imagens PNG de páginas PDF
- 🚀 **API RESTful**: Endpoints padronizados com validação automática
- 📚 **Documentação Automática**: Swagger UI e ReDoc incluídos
- 🖥️ **Interface Web**: Interface amigável para upload de arquivos
- ⚡ **Alta Performance**: Construído com FastAPI e Uvicorn

## 🛠️ Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI de alta performance  
- **[Pydantic](https://pydantic.dev/)** - Validação de dados com Type Hints
- **[pdf2image](https://github.com/Belval/pdf2image)** - Conversão PDF → Imagem
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - Manipulação de PDFs
- **[xhtml2pdf](https://xhtml2pdf.readthedocs.io/)** - HTML → PDF
- **[Pillow](https://pillow.readthedocs.io/)** - Processamento de imagens

## 🚀 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/PDFSplitter.git
cd PDFSplitter

# 2. Crie ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python main.py
```

> 📋 **Requisitos**: Python 3.11+, Poppler (ver [INSTALL.md](INSTALL.md) para detalhes)

## 🌐 Acesso Rápido

Após executar a aplicação:

- 🏠 **Interface Web**: http://localhost:5000
- 📖 **Documentação API**: http://localhost:5000/docs  
- 🔍 **ReDoc**: http://localhost:5000/redoc
- ❤️ **Health Check**: http://localhost:5000/health

## 📡 API Endpoints

| Método | Endpoint | Descrição | Exemplo |
|--------|----------|-----------|---------|
| `GET` | `/health` | Status da API | ✅ `200 OK` |
| `POST` | `/api/split-pdf` | Dividir PDF | PDF → Páginas |
| `POST` | `/api/html-to-pdf` | HTML → PDF | HTML → PDF + Imagens |
| `GET` | `/docs` | Swagger UI | 📖 Documentação |

## 💻 Exemplo de Uso

### 🌐 Converter HTML para PDF

```bash
curl -X POST http://localhost:5000/api/html-to-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<html><body><h1>Meu Documento</h1><p>Conteúdo em HTML</p></body></html>"
  }'
```

### 📄 Resposta

```json
{
  "success": true,
  "pdf_base64": "JVBERi0xLjQK...",
  "pages": [
    {
      "page_number": 1,
      "image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "total_pages": 1
}
```

## 🧪 Testando

### 📮 Postman
Importe `PDF_Splitter_API.postman_collection.json` para testar todos os endpoints.

### 🔄 Teste Automático
```bash
python test_api.py
```

## 📁 Estrutura do Projeto

```
PDFSplitter/
├── app.py                 # Aplicação FastAPI principal
├── main.py               # Script de execução
├── requirements.txt      # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Este arquivo
├── INSTALL.md           # Guia completo de instalação
├── templates/           # Templates HTML
├── static/              # Arquivos estáticos
└── postman_examples.md  # Exemplos para Postman
```

## 🚀 Deploy

### 🐳 Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y poppler-utils
COPY . .
EXPOSE 5000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

### ☁️ Heroku
```bash
# Procfile
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

## 🐛 Problemas Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| "Unable to get page count" | Poppler não instalado | `choco install poppler` |
| "ModuleNotFoundError" | Dependências faltando | `pip install -r requirements.txt` |
| "Port in use" | Porta ocupada | Use `--port 8000` |

> 📚 Veja [INSTALL.md](INSTALL.md) para troubleshooting completo

## 🤝 Contribuindo

1. 🍴 Fork o projeto
2. 🌿 Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. 💾 Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. 📤 Push para branch (`git push origin feature/nova-funcionalidade`)
5. 🔄 Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

[🐛 Reportar Bug](../../issues) • [💡 Solicitar Feature](../../issues) • [💬 Discussões](../../discussions)

</div> 