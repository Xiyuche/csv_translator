import os
from ragcheck.check_tools.checker import evaluate_json

def batch_evaluate_json(input_dir, model, api_key, api_base, output_dir=None):
    """
    批量评估指定目录下的所有JSON文件。

    :param input_dir: 输入JSON文件的目录。
    :param model: 使用的模型名称。
    :param api_key: OpenAI API密钥。
    :param api_base: API的基础URL。
    :param output_dir: 评估结果保存的目录。默认为 "output_json"。
    """
    # 设置默认的输出目录
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'output_json')

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取输入目录下的所有JSON文件
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    for json_file in json_files:
        json_file_path = os.path.join(input_dir, json_file)

        # 评估单个JSON文件
        rag_results = evaluate_json(json_file_path, model=model, api_key=api_key, api_base=api_base)

        # 保存评估结果到新的JSON文件
        output_json_path = os.path.join(output_dir, json_file)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            f.write(rag_results.to_json(indent=2, ensure_ascii=False))

# # 示例调用
# input_dir = '/Users/xiyuchen/PycharmProjects/csv_translator/ragcheck/input_json'
# output_dir = '/Users/xiyuchen/PycharmProjects/csv_translator/ragcheck/output_json'
# batch_evaluate_json(input_dir, model=model, api_key=openai_api_key, api_base=api_base, output_dir=output_dir)
