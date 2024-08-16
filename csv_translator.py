import os
from openai import OpenAI
import csv
import re

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


# 使用示例
input_csv = 'test.csv'  # 输入文件路径
output_csv = 'test_translated.csv'  # 输出文件路径
translate_columns = ['question', 'answer', 'ground_truth']  # 需要翻译的列名称
translate_csv(input_csv, output_csv, translate_columns, threshold=0.6)
