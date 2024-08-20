import os
import pandas as pd
import json


def convert_csv_to_json(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取input目录下的所有CSV文件
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(input_dir, csv_file)
        df = pd.read_csv(csv_path)

        results = []
        for idx, row in df.iterrows():
            query_id = str(idx)
            query = row['question']
            gt_answer = row['ground_truth']
            response = row['answer']

            # 初始化retrieved_context，并将doc_id从"000"开始计数
            retrieved_context = []
            context_list = row['contexts'].split('|||')  # 假设contexts用"|||"分隔
            for doc_idx, context in enumerate(context_list):
                doc_id = f"{doc_idx:03d}"
                retrieved_context.append({
                    "doc_id": doc_id,
                    "text": context.strip()
                })

            # 添加占位context
            if len(retrieved_context) < 2:
                retrieved_context.append({
                    "doc_id": f"{len(retrieved_context):03d}",
                    "text": "结束内容。"
                })

            result = {
                "query_id": query_id,
                "query": query,
                "gt_answer": gt_answer,
                "response": response,
                "retrieved_context": retrieved_context
            }
            results.append(result)

        # 保存为JSON文件，文件名与CSV对应
        json_file = os.path.join(output_dir, os.path.splitext(csv_file)[0] + '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({"results": results}, f, ensure_ascii=False, indent=2)


# 示例调用
input_dir = '/ragcheck/input_csv'  # CSV文件的路径
output_dir = 'output'  # 转换后JSON文件的保存路径
convert_csv_to_json(input_dir, output_dir)
