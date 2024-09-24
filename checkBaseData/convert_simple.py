import json
import opencc

# 创建 OpenCC 实例，用于简体转繁体
converter = opencc.OpenCC('s2t')  # 's2t' 表示从简体到繁体

# 读取 JSON 文件
with open('location.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 定义一个递归函数用于遍历和转换 JSON 中的字符串
def convert_json(data):
    if isinstance(data, dict):
        return {key: convert_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_json(item) for item in data]
    elif isinstance(data, str):
        return converter.convert(data)
    else:
        return data

# 转换 JSON 数据
converted_data = convert_json(data)

# 将转换后的数据写入新文件
with open('location2.json', 'w', encoding='utf-8') as file:
    json.dump(converted_data, file, ensure_ascii=False, indent=4)

print("转换完成！")