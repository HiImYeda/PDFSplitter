import base64
import io
from xhtml2pdf import pisa  # Importa a nova biblioteca

# 1. Defina os caminhos dos arquivos de entrada e saída
# Use "raw strings" (r'...') para evitar problemas com barras invertidas no Windows.
caminho_arquivo_html = r'C:\Users\LATITUDE 3420\Desktop\Projetos\python_reparte_pdf\teste_html.txt'
caminho_arquivo_base64 = r'C:\Users\LATITUDE 3420\Desktop\Projetos\python_reparte_pdf\base64_teste.txt'

def converter_html_para_pdf_base64(caminho_html, caminho_base64):
    """
    Lê um arquivo HTML, converte para PDF em memória e salva o resultado
    em formato Base64 em um arquivo de texto.
    """
    try:
        # 2. Leia o conteúdo do arquivo HTML
        print(f"Lendo o arquivo HTML de: {caminho_html}")
        with open(caminho_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. Use xhtml2pdf para converter HTML para PDF em memória
        print("Convertendo HTML para PDF...")
        # O resultado será escrito em um buffer de bytes
        resultado_em_memoria = io.BytesIO()
        
        # Cria o PDF. O 'source' é o HTML, e o 'dest' é o buffer de memória.
        pdf = pisa.CreatePDF(
                io.StringIO(html_content),                
                dest=resultado_em_memoria
        )

        # Se o PDF foi criado com sucesso, pisa.CreatePDF retorna False
        if pdf.err:
            raise Exception(f"Erro ao criar o PDF: {pdf.err}")

        # Pega os bytes do PDF gerado
        pdf_bytes = resultado_em_memoria.getvalue()
        resultado_em_memoria.close()

        # 4. Codifique os bytes do PDF em Base64
        print("Codificando o PDF para Base64...")
        base64_encoded_pdf = base64.b64encode(pdf_bytes)
        base64_string = base64_encoded_pdf.decode('utf-8')

        # 5. Salve a string Base64 no arquivo de saída
        print(f"Salvando a string Base64 em: {caminho_base64}")
        with open(caminho_base64, 'w') as f:
            f.write(base64_string)

        print("\nProcesso concluído com sucesso!")
        print(f"O arquivo '{caminho_base64}' foi criado.")

    except FileNotFoundError:
        print(f"\nERRO: O arquivo de entrada não foi encontrado em '{caminho_html}'. Verifique o caminho e o nome do arquivo.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")


# Executa a função principal
if __name__ == '__main__':
    converter_html_para_pdf_base64(caminho_arquivo_html, caminho_arquivo_base64)
