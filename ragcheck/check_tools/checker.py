import os
from ragchecker import RAGResults, RAGChecker
from ragchecker.metrics import all_metrics


def evaluate_json(json_file_path, model='deepseek-chat', api_key='your_api_key',
                  api_base='https://api.deepseek.com/v1'):
    """
    评估单个JSON文件的RAG结果。

    :param json_file_path: 输入JSON文件的路径。
    :param model: 使用的模型名称，默认为 'deepseek-chat'。
    :param api_key: OpenAI API密钥。
    :param api_base: API的基础URL。
    :return: 评估后的RAGResults对象。
    """
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as fp:
        rag_results = RAGResults.from_json(fp.read())

    # 设置评估器
    evaluator = RAGChecker(
        extractor_name=model,
        checker_name=model,
        batch_size_extractor=32,
        batch_size_checker=32,
        openai_api_key=api_key,
        extractor_api_base=api_base,
        checker_api_base=api_base
    )

    # 执行评估
    evaluator.evaluate(rag_results, all_metrics)

    return rag_results


# # 示例调用
# json_file_path = "examples/checking_inputs.json"
# rag_results = evaluate_json(json_file_path, api_key='sk-aff8187171d643828da2280bf1846bc0')
# print(rag_results)
