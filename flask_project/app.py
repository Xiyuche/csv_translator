import os
from openai import OpenAI
import csv
import re
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key='sk-aff8187171d643828da2280bf1846bc0',  # 替换为你的 API 密钥
    base_url="https://api.deepseek.com/v1"  # 替换为你的 base_url
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])


def translate_to_chinese(english_text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Translate the following English text to Chinese: '{english_text}'",
            }
        ],
        model="deepseek-chat",
    )
    return chat_completion.choices[0].message.content.strip()


def is_english_text(text, threshold=0.6):
    english_chars = len(re.findall(r'[A-Za-z]', text))
    return english_chars / len(text) > threshold if text else False


def process_csv(input_csv_path, output_csv_path, translate_columns, threshold=0.6):
    with open(input_csv_path, 'r', encoding='utf-8') as infile,             open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(headers)

        translate_indices = [headers.index(col) for col in translate_columns if col in headers]

        for row in reader:
            translated_row = [
                translate_to_chinese(cell) if index in translate_indices and is_english_text(cell, threshold) else cell
                for index, cell in enumerate(row)
            ]
            writer.writerow(translated_row)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
            
            return render_template('select_columns.html', headers=headers, filename=filename)

    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    filename = request.form['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    translate_columns = request.form.getlist('columns')
    threshold = float(request.form['threshold'])

    output_filename = f'translated_{filename}'
    output_filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)

    process_csv(filepath, output_filepath, translate_columns, threshold)

    return send_file(output_filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
