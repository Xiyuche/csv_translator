import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def process_json_metrics(json_dir, font_size=10):
    summary_data = {}

    # 获取目录下所有的JSON文件
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            model_name = os.path.basename(json_file).split('.')[0]

            # 提取results中的每个metrics，构建DataFrame
            metrics_list = [result['metrics'] for result in data['results']]
            df = pd.DataFrame(metrics_list)
            df.index = [f"query_{i}" for i in range(len(df))]

            # 计算均值和标准误
            mean_values = df.mean()
            stderr_values = df.sem()  # SEM is standard deviation divided by sqrt of count

            # 将标准误添加到DataFrame中
            df.loc['stderr'] = stderr_values

            # 打印完整的表格，并附带数值和网格
            print(f"Metrics Table for {model_name}:\n", df, "\n")
            print(df.to_string(index=True, col_space=12, justify='center'))

            # 将结果保存到summary_data中
            summary_data[model_name] = {
                'mean': mean_values,
                'stderr': stderr_values
            }

    # 按照指定顺序排列
    desired_order = [
        'precision', 'recall', 'f1', 'claim_recall',
        'context_precision', 'context_utilization',
        'noise_sensitivity_in_relevant', 'noise_sensitivity_in_irrelevant',
        'hallucination', 'self_knowledge', 'faithfulness'
    ]

    # 调整顺序并绘制图表
    plot_summary_metrics(summary_data, font_size, desired_order)


def plot_summary_metrics(summary_data, font_size, desired_order):
    labels = desired_order
    models = list(summary_data.keys())
    means = np.array([summary_data[model]['mean'][labels].values for model in models])
    stderrs = np.array([summary_data[model]['stderr'][labels].values for model in models])

    # 绘制图表
    fig, ax = plt.subplots(figsize=(18, 10))
    bar_width = 0.15
    index = np.arange(len(labels))

    for i, mean in enumerate(means):
        bars = plt.bar(index + i * bar_width, mean, bar_width, yerr=stderrs[i], capsize=5, label=models[i])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.005, round(yval, 2), ha='center',
                     fontsize=font_size * 0.75)

    # 添加网格
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加标签、标题和图例
    plt.xlabel('Metrics', fontsize=font_size)
    plt.ylabel('Values', fontsize=font_size)
    plt.title('Comparison of Metrics Across Different Models (with Standard Error)', fontsize=font_size)
    plt.xticks(index + bar_width * (len(models) / 2), labels, rotation=45, ha="right", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.legend(title="Models", fontsize=font_size)

    plt.tight_layout()
    plt.show()

# 示例调用

