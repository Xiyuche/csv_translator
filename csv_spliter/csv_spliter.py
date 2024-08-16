import pandas as pd
import os
import shutil


def split_csv_and_zip(file_path, output_directory, rows_per_file=10, chunk_size=10000):
    # 创建输出目录，如果不存在
    os.makedirs(output_directory, exist_ok=True)

    # 计算总共需要多少个子文件
    total_rows = 0
    chunk_no = 0

    # 分块读取和处理CSV文件
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        total_rows += len(chunk)
        num_files = (total_rows + rows_per_file - 1) // rows_per_file

        for i in range(0, len(chunk), rows_per_file):
            start_row = i
            end_row = start_row + rows_per_file
            sub_df = chunk.iloc[start_row:end_row]

            if sub_df.empty:
                continue

            # 文件名使用总行数进行标识，避免与其他分块文件冲突
            sub_file_path = os.path.join(output_directory, f'split_file_{chunk_no + 1}.csv')
            sub_df.to_csv(sub_file_path, index=False)
            chunk_no += 1


    return 0


# 示例用法
csv_file_path = 'merged_translated_output.csv'  # 输入的CSV文件路径
output_dir = './'  # 输出的子文件目录

# 执行拆分和压缩任务
split_csv_and_zip(csv_file_path, output_dir)

print(f'done.')
