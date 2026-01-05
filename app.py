from flask import Flask, render_template, request, send_file
from models import db, Resume
from pdf_generator import create_pdf
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resumes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
