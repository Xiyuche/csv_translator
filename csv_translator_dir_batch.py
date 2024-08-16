import os
from openai import OpenAI
import csv
import re
import concurrent.futures

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key='sk-aff8187171d643828da2280bf1846bc0',  # 替换为你的 API 密钥
    base_url="https://api.deepseek.com/v1"  # 替换为你的 base_url
)


def translate_to_chinese(english_text):
    # 调用 OpenAI API 进行翻译
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Translate the following English text to Chinese: '{english_text}'",
            }
        ],
        model="deepseek-chat",
    )
    # 返回翻译结果
    return chat_completion.choices[0].message.content.strip()


def is_english_text(text, threshold=0.6):
    english_chars = len(re.findall(r'[A-Za-z]', text))
    return english_chars / len(text) > threshold if text else False


def translate_csv(input_csv_path, output_csv_path, translate_columns, threshold=0.6):
    with open(input_csv_path, 'r', encoding='utf-8') as infile, \
            open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 读取表头并写入输出文件
        headers = next(reader)
        writer.writerow(headers)

        # 获取需要翻译的列的索引
        translate_indices = [headers.index(col) for col in translate_columns if col in headers]

        for row in reader:
            translated_row = [
                translate_to_chinese(cell) if index in translate_indices and is_english_text(cell, threshold) else cell
                for index, cell in enumerate(row)
            ]
            writer.writerow(translated_row)


def process_directory(input_directory_path, output_directory_path, translate_columns, threshold=0.6):
    # 确保输出目录存在
    os.makedirs(output_directory_path, exist_ok=True)

    # 获取输入目录下所有CSV文件
    csv_files = [os.path.join(input_directory_path, f) for f in os.listdir(input_directory_path) if f.endswith('.csv')]

    # 使用多线程并行处理每个CSV文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                translate_csv,
                csv_file,
                os.path.join(output_directory_path, f"translated_{os.path.basename(csv_file)}"),
                translate_columns,
                threshold
            ) for csv_file in csv_files
        ]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # 如果任务出现异常，会在此处抛出
            except Exception as e:
                print(f"Error processing file: {e}")


# 使用示例
input_directory = 'input'  # 输入CSV文件所在的目录路径
output_directory = 'output'  # 输出CSV文件保存的目录路径
translate_columns = ['question', 'answer', 'ground_truth']  # 需要翻译的列名称
process_directory(input_directory, output_directory, translate_columns, threshold=0.6)
