from flask import Flask, request, render_template, redirect, url_for, flash, send_file
import os
from input import save_file
from process import process_file

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages
UPLOAD_FOLDER = './output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = save_file(file, file.filename)  # Save the uploaded file
        processed_file_path = process_file(file_path)  # Process the saved file
        if processed_file_path:
            return render_template('complete.html', file_url=url_for('download_file', filename=os.path.basename(processed_file_path)))
        else:
            flash('File processing failed')
            return redirect(url_for('upload_form'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)