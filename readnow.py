import os
import logging

logging.basicConfig(level=logging.INFO)
# 指定文件夹路径
folder_path = './原文'
import re

# 获取指定路径下的所有文件和文件夹名称
all_names = os.listdir(folder_path)
from bs4 import BeautifulSoup
def replace(string):
    result = re.sub(r'\(.*?\)', '', string, re.S)


    return result
# 过滤出文件夹名称
folder_names = [replace(name) for name in all_names if os.path.isdir(os.path.join(folder_path, name))]
print(folder_names)
print(len(folder_names))


def make_valid_filename(filename):
    # 去除非法字符
    valid_filename = re.sub(r'[<>:"/\\|?*\s]', '', str(filename))

    # # 删除连续的空格
    # valid_filename = re.sub(r'\s+', ' ', valid_filename)

    return valid_filename


def read(i):
    with open(f'./小说详情/part{i}.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')
    title_element = soup.title
    # title_tag = soup.find('title')
    title = title_element.string
    # logging.info(str(title))
    return make_valid_filename(title)
    # a_element = soup.find_all('a', href=True)
    # for n in a_element:
    #     if '查看全部章节...' in n:
    #         text = n.text
    #         href = n['href']
    #         return href


start_num = 44070
reads = []
for i in range(start_num, start_num - 100 - 100 - 100 - 100 - 100 - 100, -1):
    try:
        string = read(i).split('_')[0]
        result = re.sub(r'\(.*?\)', '', string, re.S)
        reads.append(result)
    except FileNotFoundError as e:
        reads.append('不存在')
print(reads)
print(len(reads))
diff = list(set(folder_names) - set(reads))
print(diff)
print(len(diff))

# 打印文件夹名称
# for folder_name in folder_names:
#     print(folder_name)
