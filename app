from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfkit
import os

app = Flask(__name__)

# 🔹 Permitir CORS corretamente
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# 🔹 Adicionar suporte ao método OPTIONS para evitar erro de preflight
@app.route('/gerar_pdf', methods=['OPTIONS'])
def options_preflight():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE, PUT")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    try:
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "Nenhum JSON válido recebido"}), 400

        print("✅ Dados recebidos:", dados)

        pdf_filename = f"curriculo_{dados['nome'].replace(' ', '_')}.pdf"
        pdf_path = os.path.join("curriculos", pdf_filename)

        if not os.path.exists("curriculos"):
            os.makedirs("curriculos")

        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #0F4C5C; }}
                p {{ font-size: 14px; line-height: 1.5; }}
                .section {{ margin-bottom: 15px; }}
                strong {{ color: #0F4C5C; }}
            </style>
        </head>
        <body>
            <h1>Currículo de {dados['nome']}</h1>
            <p><strong>Email:</strong> {dados['email']}</p>
            <p><strong>Telefone:</strong> {dados['telefone']}</p>
            <p><strong>Cargo:</strong> {dados['cargo']}</p>
            <p><strong>Descrição:</strong> {dados['descricao']}</p>
            <p><strong>Habilidades:</strong> {dados['habilidades']}</p>
            <p><strong>Formação Acadêmica:</strong> {dados['formacao']}</p>
        </body>
        </html>
        """

        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        pdfkit.from_string(html_content, pdf_path, configuration=config, options={"encoding": "UTF-8"})

        return send_file(pdf_path, as_attachment=True)
    
    except Exception as e:
        print("❌ Erro ao gerar PDF:", str(e))
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
