import os
import csv


def merge_csv_files(input_directory, output_csv_path, selected_headers):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(selected_headers)

        for filename in os.listdir(input_directory):
            if filename.endswith('.csv'):
                with open(os.path.join(input_directory, filename), 'r', encoding='utf-8') as infile:
                    reader = csv.DictReader(infile)
                    writer.writerows([[row.get(header, '') for header in selected_headers] for row in reader])


# 使用示例
input_directory = 'output'  # 输入CSV文件所在的目录路径
output_csv_path = 'merged_output.csv'  # 合并后的输出文件路径
selected_headers = ['question', 'contexts', 'ground_truth', 'evolution_type']  # 你要保留的列名列表

merge_csv_files(input_directory, output_csv_path, selected_headers)
