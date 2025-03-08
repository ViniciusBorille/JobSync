from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfkit
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do caminho do wkhtmltopdf (se necessário)
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")  # Altere para seu caminho correto

@app.route('/salvar_curriculo', methods=['POST'])
def salvar_curriculo():
    try:
        dados = request.json
        print("✅ Dados recebidos no backend:", dados)

        return jsonify({
            "mensagem": f"Currículo de {dados['nome']} salvo com sucesso!",
            "dados": dados
        })
    except Exception as e:
        print("❌ Erro no backend:", str(e))
        return jsonify({"erro": str(e)}), 500

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    try:
        dados = request.json
        pdf_filename = f"curriculo_{dados['nome'].replace(' ', '_')}.pdf"
        pdf_path = os.path.join("curriculos", pdf_filename)

        if not os.path.exists("curriculos"):
            os.makedirs("curriculos")

        # Criando o HTML para o PDF
        html_content = f"""
        <html>
        <head><style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #0F4C5C; }}
            p {{ font-size: 14px; }}
            .section {{ margin-bottom: 15px; }}
        </style></head>
        <body>
            <h1>Currículo de {dados['nome']}</h1>
            <div class="section"><strong>Email:</strong> {dados['email']}</div>
            <div class="section"><strong>Telefone:</strong> {dados['telefone']}</div>
            <div class="section"><strong>Cargo:</strong> {dados['cargo']}</div>
            <div class="section"><strong>Descrição:</strong> {dados['descricao']}</div>
            <div class="section"><strong>Habilidades:</strong> {dados['habilidades']}</div>
            <div class="section"><strong>Formação Acadêmica:</strong> {dados['formacao']}</div>
        </body>
        </html>
        """

        # Gerando o PDF
        pdfkit.from_string(html_content, pdf_path, configuration=config)

        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        print("❌ Erro ao gerar PDF:", str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
