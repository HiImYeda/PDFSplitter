# 🚀 Instalação e Configuração - PDF Splitter API

Guia completo para instalar e configurar a aplicação FastAPI.

## 📋 Pré-requisitos

- **Python 3.11+** 
- **Git**
- **Poppler** (para conversão PDF → imagem)

## 🔧 Instalação

### 1. **Clone o repositório**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd PDFSplitter
```

### 2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. **Instale as dependências**

#### Opção A: Usando pip (tradicional)
```bash
pip install -r requirements.txt
```

#### Opção B: Usando uv (moderno e mais rápido)
```bash
# Instale o uv primeiro
pip install uv

# Instale as dependências
uv sync
```

### 4. **Instale o Poppler** (necessário para pdf2image)

#### **Windows:**
```bash
# Usando Chocolatey (recomendado)
choco install poppler

# OU baixe manualmente
# Baixe de: https://github.com/oschwartz10612/poppler-windows/releases
# Extraia e adicione ao PATH
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils
```

#### **macOS:**
```bash
# Usando Homebrew
brew install poppler
```

## 🏃‍♂️ Executando a Aplicação

### **Desenvolvimento:**
```bash
# Método 1: Usando uvicorn diretamente
uvicorn app:app --host 0.0.0.0 --port 5000 --reload

# Método 2: Usando o script principal
python main.py

# Método 3: Usando o script de desenvolvimento
python dev.py
```

### **Produção:**
```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```

## 🌐 Acessando a Aplicação

Após iniciar o servidor, acesse:

- **Interface Web:** http://localhost:5000
- **Documentação API (Swagger):** http://localhost:5000/docs
- **Documentação API (ReDoc):** http://localhost:5000/redoc
- **Health Check:** http://localhost:5000/health

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Verificar status da API |
| GET | `/` | Interface web principal |
| POST | `/api/split-pdf` | Dividir PDF em páginas |
| POST | `/api/html-to-pdf` | Converter HTML para PDF |
| GET | `/docs` | Documentação Swagger |
| GET | `/redoc` | Documentação ReDoc |

## 🧪 Testando a API

### **1. Health Check**
```bash
curl http://localhost:5000/health
```

### **2. HTML para PDF**
```bash
curl -X POST http://localhost:5000/api/html-to-pdf \
  -H "Content-Type: application/json" \
  -d '{"html_content": "<html><body><h1>Teste!</h1></body></html>"}'
```

### **3. Usando Postman**
Importe a collection: `PDF_Splitter_API.postman_collection.json`

## 🐛 Troubleshooting

### **Erro: "Unable to get page count"**
- **Problema:** Poppler não instalado ou não no PATH
- **Solução:** Instale o Poppler conforme instruções acima

### **Erro: "ModuleNotFoundError"**
- **Problema:** Dependências não instaladas
- **Solução:** Execute `pip install -r requirements.txt`

### **Erro: "Port already in use"**
- **Problema:** Porta 5000 já está em uso
- **Solução:** Use uma porta diferente: `uvicorn app:app --port 8000`

### **Erro: "xhtml2pdf encoding"**
- **Problema:** Caracteres especiais no HTML
- **Solução:** Use encoding UTF-8 no HTML: `<meta charset="UTF-8">`

## 🔒 Segurança

### **Produção:**
- Configure CORS adequadamente
- Use HTTPS
- Limite tamanho de uploads
- Implemente rate limiting
- Use variáveis de ambiente para configurações

### **Variáveis de Ambiente:**
```bash
# .env (crie este arquivo)
DEBUG=False
MAX_FILE_SIZE=10485760  # 10MB
CORS_ORIGINS=["https://seudominio.com"]
```

## 📦 Deploy

### **Docker (recomendado):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y poppler-utils

COPY . .
EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

### **Heroku:**
```bash
# Procfile
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**💡 Dica:** Para desenvolvimento, use o comando `python dev.py` que já configura o Poppler automaticamente no Windows! 