# 📮 Guia da Collection Postman - PDF Splitter API

Este arquivo contém exemplos e instruções para usar a collection do Postman com a API FastAPI.

## 🚀 Como Importar a Collection

1. **Abra o Postman**
2. **Click em "Import"** (canto superior esquerdo)
3. **Selecione "Upload Files"**
4. **Escolha o arquivo** `PDF_Splitter_API.postman_collection.json`
5. **Click "Import"**

## 🔧 Configuração

A collection usa uma variável de ambiente `{{base_url}}` que está configurada para `http://localhost:5000`.

### Para alterar a URL:
1. Click no nome da collection
2. Vá na aba "Variables"
3. Altere o valor de `base_url` se necessário

## 📋 Endpoints Incluídos

### 1. **Health Check** 
- **Método:** GET
- **URL:** `/health`
- **Descrição:** Verifica se a API está funcionando
- **Testes incluídos:** Status 200, campos obrigatórios

### 2. **Split PDF**
- **Método:** POST  
- **URL:** `/api/split-pdf`
- **Body:** JSON com `pdf_base64`
- **Descrição:** Divide PDF em páginas individuais
- **Testes incluídos:** Validação de resposta, estrutura de dados

### 3. **HTML to PDF**
- **Método:** POST
- **URL:** `/api/html-to-pdf` 
- **Body:** JSON com `html_content`
- **Descrição:** Converte HTML em PDF
- **Testes incluídos:** PDF gerado, páginas criadas

### 4. **Main Page**
- **Método:** GET
- **URL:** `/`
- **Descrição:** Interface web da aplicação

### 5. **API Documentation**
- **Swagger UI:** GET `/docs`
- **ReDoc:** GET `/redoc`
- **OpenAPI Schema:** GET `/openapi.json`

## 📄 Exemplos de Dados

### PDF Base64 Simples (para Split PDF)

```json
{
    "pdf_base64": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovT3V0bGluZXMgMiAwIFIKL1BhZ2VzIDMgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9UeXBlIC9PdXRsaW5lcwovQ291bnQgMAo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWzQgMCBSXQo+PgplbmRvYmoKNCAwIG9iago8PAovVHlwZSAvUGFnZQovUGFyZW50IDMgMCBSCi9SZXNvdXJjZXMgPDwKL0ZvbnQgPDwKL0YxIDUgMCBSCj4+Cj4+Ci9NZWRpYUJveCBbMCAwIDYxMiA3OTJdCi9Db250ZW50cyA2IDAgUgo+PgplbmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKPj4KZW5kb2JqCjYgMCBvYmoKPDwKL0xlbmd0aCA0NAo+PgpzdHJlYW0KQlQKL0YxIDEyIFRmCjEwMCA3MDAgVGQKKFRlc3RlIGRvIFBERikgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNwowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA3NCAwMDAwMCBuIAowMDAwMDAwMTIwIDAwMDAwIG4gCjAwMDAwMDAxNzcgMDAwMDAgbiAKMDAwMDAwMDM2NCAwMDAwMCBuIAowMDAwMDAwNDU2IDAwMDAwIG4gCnRyYWlsZXIKPDwKL1NpemUgNwovUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNTQ5CiUlRU9G"
}
```

### HTML Simples (para HTML to PDF)

```json
{
    "html_content": "<html><head><title>Teste</title></head><body><h1>Hello World!</h1><p>Este é um teste da API.</p></body></html>"
}
```

### HTML Complexo com CSS

```json
{
    "html_content": "<html><head><title>Documento Teste</title><style>body{font-family:Arial,sans-serif;margin:40px;background:#f9f9f9}.container{background:white;padding:30px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}h1{color:#2E86AB;border-bottom:2px solid #2E86AB;padding-bottom:10px}.info{background:#e3f2fd;padding:15px;border-left:4px solid #2196f3;margin:20px 0}table{width:100%;border-collapse:collapse;margin:20px 0}th,td{border:1px solid #ddd;padding:12px;text-align:left}th{background:#f5f5f5}</style></head><body><div class='container'><h1>🚀 Relatório de Teste API</h1><div class='info'><strong>Info:</strong> Este documento foi gerado via API FastAPI</div><h2>Dados do Teste</h2><table><tr><th>Campo</th><th>Valor</th></tr><tr><td>Framework</td><td>FastAPI</td></tr><tr><td>Validação</td><td>Pydantic</td></tr><tr><td>Status</td><td>✅ Funcionando</td></tr></table><h2>Funcionalidades</h2><ul><li>Conversão HTML → PDF</li><li>Divisão de PDFs</li><li>Geração de imagens</li><li>Documentação automática</li></ul></div></body></html>"
}
```

## 🧪 Testes Automáticos

Cada request tem testes automáticos incluídos que verificam:

- ✅ Status code correto
- ✅ Estrutura de resposta
- ✅ Campos obrigatórios
- ✅ Tipos de dados
- ✅ Content-Type headers

### Para ver os resultados dos testes:
1. Execute qualquer request
2. Vá na aba "Test Results"
3. Veja quais testes passaram/falharam

## 📝 Como Obter um PDF em Base64

### Método 1: Python
```python
import base64

with open('seu_arquivo.pdf', 'rb') as file:
    pdf_data = file.read()
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    print(pdf_base64)
```

### Método 2: Online
1. Acesse: https://base64.guru/converter/encode/pdf
2. Faça upload do seu PDF
3. Copie o resultado (sem prefixo `data:application/pdf;base64,`)

### Método 3: PowerShell (Windows)
```powershell
$pdfBytes = [System.IO.File]::ReadAllBytes("C:\caminho\para\arquivo.pdf")
$pdfBase64 = [System.Convert]::ToBase64String($pdfBytes)
Write-Output $pdfBase64
```

## 🔍 Dicas de Teste

### Para Split PDF:
- Use PDFs pequenos para testes rápidos
- Verifique se `total_pages` corresponde ao PDF original
- Cada página retorna `pdf_base64` e `image_base64`

### Para HTML to PDF:
- Teste CSS inline primeiro
- Imagens devem estar em base64 ou URLs públicas
- Fontes web podem não funcionar (use fontes padrão)

### Troubleshooting:
- **413 Error:** PDF muito grande
- **400 Error:** Base64 inválido ou HTML malformado
- **500 Error:** Erro interno (verifique logs da API)

## 📊 Monitoramento

A collection inclui logs automáticos que mostram:
- URL da request
- Status da response  
- Tempo de resposta
- Resultados dos testes

## 🔗 Links Úteis

- **Swagger UI:** http://localhost:5000/docs
- **ReDoc:** http://localhost:5000/redoc
- **Health Check:** http://localhost:5000/health
- **Interface Web:** http://localhost:5000

## 🎯 Fluxo de Teste Recomendado

1. **Health Check** - Verificar se API está online
2. **HTML to PDF** - Testar conversão simples
3. **Split PDF** - Testar divisão com PDF gerado
4. **Documentação** - Explorar endpoints no Swagger
5. **Interface Web** - Testar interface gráfica

---

**💡 Dica:** Execute os requests em sequência usando o "Collection Runner" para um teste completo automatizado! 