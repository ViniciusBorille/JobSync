import pdfkit

def gerar_pdf(nome, descricao):
    html_content = f"""
    <h1>{nome}</h1>
    <p>{descricao}</p>
    """
    pdfkit.from_string(html_content, 'curriculo.pdf')
