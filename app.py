from flask import Flask, render_template, request, send_file
from pdf_generator import create_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/builder')
def builder():
    return render_template('builder.html')

@app.route('/api/generate_pdf', methods=['POST'])
def generate_pdf_route():
    data = request.json
    pdf_buffer = create_pdf(data)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name='resume.pdf',
        mimetype='application/pdf'
    )

# IMPORTANT: do NOT use app.run() in production
