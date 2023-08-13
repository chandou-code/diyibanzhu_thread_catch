import time
import requests
from bs4 import BeautifulSoup
import logging
import re
import os
import concurrent.futures
import queue
import concurrent.futures
from functools import partial

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建一个FileHandler用于写入日志文件
file_handler = logging.FileHandler('log_file.log')

# 将FileHandler添加到logger对象
logger = logging.getLogger()
logger.addHandler(file_handler)


class timelogging:
    def __init__(self, begin):
        self.nums = None
        self.begin = begin

    def show(self, now):
        return int(now - self.begin)

    # def base_handled(self, nums):
    #     self.nums = nums
    #     # print(self.nums)
    #
    # def handled(self, i):
    #     i = i.split('/')[1]
    #     c = int(i)
    #     # print(c)
    #     my_set = []
    #     my_set.append(c)
    #     my_set = set(my_set)
    #     nums = set(self.nums)
    #     diff = nums - my_set
    #     with open('continue.txt', 'w', encoding='utf-8') as f:
    #         f.write(str(diff))


class No2_dybz:
    def __init__(self):
        self.flag_contents = True
        self.flag_reback = None
        self.title = None
        self.flag = None
        self.start = None
        self.text = None
        self.num = 1
        self.index = 1
        self.contents = []
        self.u = None
        self.end = None
        # self.id = myid
        self.unloads = []

    def re_request(self, u):

        max_retries = 160
        retry_count = 0
        # response = None
        while retry_count < max_retries:
            # time.sleep(0.25)
            try:
                response = requests.get(u)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
                # break  # 如果请求成功，则跳出循环
            except:
                retry_count += 1
                logging.info(f'{u}重试{retry_count}')

    def make_valid_filename(self, filename):
        # 去除非法字符
        valid_filename = re.sub(r'[<>:"/\\|?*\s]', '', str(filename))
        return valid_filename

    def base_info(self, url):

        self.start = time.time()
        u = f'https://m.diyibanzhu.buzz/{url}/all_1/'
        # logging.info(f'base_info{url}')
        self.title = 'm.diyibanzhu.buzz | 502: Bad g'
        index = 0
        while self.title == 'm.diyibanzhu.buzz | 502: Bad g' or self.title == 'm.diyibanzhu.buzz | 502: Bad g' or self.title == 'm.diyibanzhu.buzz502Badg' or self.title == '':
            # print(self.title)
            # print(1)
            if index != 0:
                logging.info(f'{url}重新请求中,第{index}次重试')
            index += 1
            r = requests.get(u)
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            self.title = soup.find('title').text.split('_')[0][:-6]  # 我被金主扫地出门之后
            if index >= 25:
                return -1
        return self.make_valid_filename(self.title)

    def page_info(self, url, index, link, title):
        u = f'https://m.diyibanzhu.buzz/{url}/all_{index}/'
        html = self.re_request(u)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.text
        # print(text)
        a_tags = soup.find_all('a')
        for _ in range(6):
            del a_tags[0]
        for a in a_tags:
            if a.text != '尾页' and a.text != '书架' and a.text != '阅读记录' and a.text != '首页' and a.text != '下一页' and a.text != '上一页' and a.text != '阅读记录' and a.text != '阅读记录 ':
                title.append(a.text)
                link.append(a.get('href'))
        if '下一页' in text:
            self.num += 1
            # print('下一页')
            return self.page_info(url, self.num, link, title)
        else:
            self.num = 1
            return link, title

    def get_content(self, u, index, Big_title, title):
        if self.flag_contents:
            self.u = u
            # print(self.index)
            self.index = index
            if self.index == 1:
                # time.sleep(1)
                self.text = self.re_request(self.u)
                soup = BeautifulSoup(self.text, 'html.parser')
                content = soup.find('div', class_='novelcontent').get_text().replace('\n ', '').replace('　　',
                                                                                                        '').replace(
                    '   ',
                    '').replace(
                    '    ', '').replace('本章未完，请点击下一页继续阅读 》》上一章返回目录加入书签下一页', '').replace(
                    '上一页',
                    '').replace(
                    '返回目录', '').replace('加入书签', '').replace('下一章', '').replace(
                    '本章未完，请点击下一页继续阅读 》》',
                    '').replace('下一页', '').replace(
                    '上一章返回目录加入书签下一章', '').replace('上一章', '')
                self.contents.append(content)
            elif self.index != 1:
                p1 = self.u.split('.')[0]
                p2 = self.u.split('.')[1]
                p = self.u.split('.')[2]
                if '_' in p:
                    p = p.split('_')[0]

                u = f'{p1}.{p2}.{p}_{self.index}.html'
                # print(u)
                self.text = self.re_request(u)
                soup = BeautifulSoup(self.text, 'html.parser')
                content = soup.find('div', class_='novelcontent').get_text().replace('\n ', '').replace('　　',
                                                                                                        '').replace(
                    '   ',
                    '').replace(
                    '    ', '').replace('本章未完，请点击下一页继续阅读 》》上一章返回目录加入书签下一页', '').replace(
                    '上一页',
                    '').replace(
                    '返回目录', '').replace('加入书签', '').replace('下一章', '').replace(
                    '本章未完，请点击下一页继续阅读 》》',
                    '').replace('下一页', '').replace(
                    '上一章返回目录加入书签下一章', '').replace('上一章', '').replace('\n ', '')
                if content != self.contents[-1]:
                    self.contents.append(content)

                else:
                    logging.info(f'{u}最后两章一样')
                    self.flag_contents = False
            # print(self.contents)
            if '下一页' in self.text:
                self.text = ''
                self.index += 1
                # print(self.index)
                if self.flag_contents:
                    return self.get_content(u, self.index, Big_title, title)
                if not self.flag_contents:
                    logging.info(f'跳过错误章节{u}')
                    self.index = 1
                    content = self.contents
                    self.contents = []
                    content = ''.join(content)
                    self.creaft_DOM(Big_title)
                    self.save(title, content, Big_title)
            elif '下一章' in self.text:
                self.index = 1
                content = self.contents
                self.contents = []
                content = ''.join(content)
                self.creaft_DOM(Big_title)
                self.save(title, content, Big_title)
                # return content
            # return content

    def save(self, title, content, Big_title):
        with open(f'./原文/{self.make_valid_filename(Big_title)}/{self.make_valid_filename(title)}.txt', 'w',
                  encoding='utf-8') as f:
            f.write(content)

    def creaft_DOM(self, dom):
        folder_path = './原文'
        file_name = dom
        file_path = os.path.join(folder_path, self.make_valid_filename(file_name))
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def time_diff(self, big, url):
        self.end = time.time()
        logging.info(f'{big}总耗时:{timelogging.show(self.end)}s,{url}')

    def check_txt_files_exist(self, t, title, big_title):
        folder_path = f'./原文/{self.make_valid_filename(big_title)}'
        file_name = f'{self.make_valid_filename(title[t])}.txt'
        file_path = os.path.join(folder_path, self.make_valid_filename(file_name))
        # print(file_path)
        if os.path.exists(file_path):
            # logging.info(file_path + '文件存在')
            return True
        else:
            logging.info(f'{file_path.encode("gbk", "ignore").decode("gbk")} 文件不存在')
            return False

    def save_list(self, list, title, url, bigtitle):
        with open('list_and_title.txt', 'a', encoding='utf-8') as f:
            f.write(str(list) + '|' + str(title) + '|' + str(bigtitle) + '|' + str(url) + '\n')

    def get_new_list(self, title, Big_title, link):
        unload_B = []
        for t in range(len(title)):
            unload_B.append(self.check_txt_files_exist(t, title, Big_title))
        new_link = []
        new_title = []
        for u in range(len(unload_B)):
            if not unload_B[u]:
                # print('新')
                new_link.append(link[u])
                new_title.append(title[u])
        if new_title:
            return new_link, new_title
        else:
            return None

    def del_unexpect(self, title, big_title):
        import os
        folder_path = f'./原文/{self.make_valid_filename(big_title)}'

        # 使用os.listdir获取文件夹中所有文件和文件夹的名称列表
        file_names = os.listdir(folder_path)

        # 循环打印文件名
        for file_name in file_names:
            print(file_name)

    def read_local_info(self):
        file_path = 'list_and_title.txt'

        try_encodings = ['UTF-8', 'Windows-1254', 'GBK', 'ISO-8859-1']

        for encoding in try_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    print(content)
                break
            except UnicodeDecodeError:
                continue

    def main(self, i):
        url = i
        url = f'{url // 1000}/{url}'
        link = []
        title = []
        self.flag_reback = True
        Big_title = self.base_info(url)
        if Big_title == -1:
            return
            # if not self.flag:
        # print(self.flag)
        link, title = self.page_info(url, 1, link, title)
        self.save_list(link, title, url, Big_title)
        index = 0
        while self.flag_reback:
            index += 1
            result = self.get_new_list(title, Big_title, link)
            if result is None:
                self.flag_reback = False
                logging.info(f'{Big_title}已补全')
                # 在这里处理没有返回值的情况
                # 例如执行其他操作或者设置默认值
                pass
            else:
                new_link, new_title = result
                # 继续处理得到的新链接和新标题
                max = len(new_link) + 1
                if max > 20:
                    max = 21
                task_queue = queue.Queue()

                for i in range(len(new_link)):
                    partial_task_function = partial(task_function2, new_link[i], 1, Big_title, new_title[i])
                    task_queue.put(partial_task_function)

                with concurrent.futures.ThreadPoolExecutor(max_workers=max) as executor:
                    while not task_queue.empty():
                        task = task_queue.get()
                        executor.submit(task)

                    executor.shutdown()
                self.time_diff(Big_title, url)
                if index == 5:
                    self.flag_reback = False

    # def if_txt(self):


def task_function(i):
    obj = No2_dybz()
    obj.main(i)
    # 执行任务的代码

import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']

    print("Detected Encoding:", encoding)
    print("Confidence:", confidence)

    return encoding

def read_file(file_path, encoding):
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        content = file.read()

    return content


def task_function2(link, num, bigtitle, title):
    obj2 = No2_dybz()
    obj2.get_content(link, num, bigtitle, title)


def my_run():
    task_queue = queue.Queue()
    # lists = []

    for i in range(38690, 1, -1):
        # lists.append(i)
        task_queue.put(i)

    # timelogging.base_handled(lists)
    # 创建多线程池
    num_threads = 50  # 线程数
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交任务给线程池执行
        while not task_queue.empty():
            task = task_queue.get()
            executor.submit(task_function, task)

        # 等待所有任务完成
        executor.shutdown()


if __name__ == '__main__':
    timelogging = timelogging(time.time())
    try1 = No2_dybz()
    # 文件路径
    file_path = 'list_and_title.txt'

    # 检测编码方式
    # encoding = detect_encoding(file_path)

    # 以正确的编码方式读取文件内容到内存中
    content = read_file(file_path, 'Windows-1254')
    print(content)

    # try1.read_local_info()
    # my_run()
    # title = ['分卷(1)', '分卷(2)', '分卷(3)', '分卷(4)', '分卷(5)', '分卷(6)', '分卷(7)', '分卷(8)', '分卷(9)',
    #          '分卷(10)', '分卷(11)', '分卷(12)', '分卷(13)', '分卷(14)', '分卷(15)', '分卷(16)', '分卷(17)', '分卷(18)',
    #          '分卷(19)', '分卷(20)', '分卷(21)', '分卷(22)', '分卷(23)', '分卷(24)', '分卷(25)', '分卷(26)', '分卷(27)',
    #          '分卷(28)', '分卷(29)', '分卷(30)', '分卷(31)', '分卷(32)', '分卷(33)', '分卷(34)', '分卷(35)']

    # try1.del_unexpect()
