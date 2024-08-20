import os
import json
import numpy as np
import matplotlib.pyplot as plt


def plot_metrics_from_json_directory(json_dir, font_size=10):
    """
    从指定目录中读取所有JSON文件，并生成模型指标对比图。

    :param json_dir: 包含JSON文件的目录路径
    :param font_size: 字体大小，默认为10
    """
    # 获取目录下所有的JSON文件
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

    # 初始化一个字典来存储每个文件的指标数据
    metrics_data = {}

    # 读取并提取每个JSON文件的指标
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            metrics = data.get('metrics', {})
            metrics_data[os.path.basename(json_file).split('.')[0]] = {
                **metrics.get('overall_metrics', {}),
                **metrics.get('retriever_metrics', {}),
                **metrics.get('generator_metrics', {})
            }

    # 提取所有指标标签
    labels = list(next(iter(metrics_data.values())).keys())

    # 准备数据
    models = list(metrics_data.keys())
    data = np.array([[metrics_data[model].get(label, 0) for label in labels] for model in models])

    # 绘制图表
    fig, ax = plt.subplots(figsize=(18, 10))
    bar_width = 0.15
    index = np.arange(len(labels))

    for i, model_data in enumerate(data):
        plt.bar(index + i * bar_width, model_data, bar_width, label=models[i])

    # 添加标签、标题和图例
    plt.xlabel('Metrics', fontsize=font_size)
    plt.ylabel('Values', fontsize=font_size)
    plt.title('Comparison of Metrics Across Different Models', fontsize=font_size)
    plt.xticks(index + bar_width * (len(models) / 2), labels, rotation=45, ha="right", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.legend(title="Models", fontsize=font_size)

    plt.tight_layout()
    plt.show()

# 示例调用
# plot_metrics_from_json_directory('/path/to/your/json_directory', font_size=12)
