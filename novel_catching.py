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

logging.basicConfig(level=logging.INFO)


class timelogging:
    def __init__(self, begin):
        self.nums = None
        self.begin = begin

    def show(self, now):
        return int(now - self.begin)

    def base_handled(self, nums):
        self.nums = nums
        # print(self.nums)

    def handled(self, i):
        i = i.split('/')[1]
        c = int(i)
        # print(c)
        my_set = []
        my_set.append(c)
        my_set = set(my_set)
        nums = set(self.nums)

        with open('continue.txt', 'w', encoding='utf-8') as f:
            f.write(f'尚未完成:{str(nums - my_set)}')


class No2_dybz:
    def __init__(self, myid):
        self.title = None
        self.flag = None
        self.start = None
        self.text = None
        self.num = 1
        self.index = 1
        self.contents = []
        self.u = None
        self.end = None
        self.id = myid

    def re_request(self, u):
        max_retries = 16
        retry_count = 0
        response = None
        while retry_count < max_retries:
            try:
                response = requests.get(u)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
                # break  # 如果请求成功，则跳出循环
            except requests.exceptions.RequestException as e:
                # logging.info(f"请求错误: {e}")
                if isinstance(e, requests.exceptions.ConnectionError):
                    retry_count += 1
                    # logging.info(f"{u}重试次数: {retry_count}")
                else:
                    break  # 如果不是连接错误，则立即停止重试

    def make_valid_filename(self, filename):
        # 去除非法字符
        valid_filename = re.sub(r'[<>:"/\\|?*\s]', '', str(filename))
        return valid_filename

    def base_info(self, url):

        self.start = time.time()
        u = f'https://m.diyibanzhu.buzz/{url}/all_1/'

        self.title = 'm.diyibanzhu.buzz | 502: Bad g'
        index = 0
        while self.title == 'm.diyibanzhu.buzz | 502: Bad g' or self.title == 'm.diyibanzhu.buzz | 502: Bad g' or self.title == 'm.diyibanzhu.buzz502Badg':
            # print(self.title)
            # print(1)
            if index != 0:
                logging.info(f'title重新请求中,第{index}次重试')
            index += 1
            r = requests.get(u)
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            self.title = soup.find('title').text.split('_')[0][:-6]  # 我被金主扫地出门之后
        folder_path = './原文'
        file_name = self.title
        file_path = os.path.join(folder_path, self.make_valid_filename(file_name))
        if os.path.exists(file_path):
            logging.info(self.title + '已下载')
            self.flag = True
        return self.title

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
        self.u = u
        self.index = index
        # print(self.index)
        if self.index == 1:
            self.text = self.re_request(self.u)
            soup = BeautifulSoup(self.text, 'html.parser')
            content = soup.find('div', class_='novelcontent').get_text().replace('\n ', '').replace('　　', '').replace(
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
            content = soup.find('div', class_='novelcontent').get_text().replace('\n ', '').replace('　　', '').replace(
                '   ',
                '').replace(
                '    ', '').replace('本章未完，请点击下一页继续阅读 》》上一章返回目录加入书签下一页', '').replace(
                '上一页',
                '').replace(
                '返回目录', '').replace('加入书签', '').replace('下一章', '').replace(
                '本章未完，请点击下一页继续阅读 》》',
                '').replace('下一页', '').replace(
                '上一章返回目录加入书签下一章', '').replace('上一章', '').replace('\n ', '')
            self.contents.append(content)
        # print(self.contents)
        if '下一页' in self.text:
            self.text = ''
            self.index += 1
            # print(self.index)
            return self.get_content(u, self.index, Big_title, title)
        else:
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

    def time_diff(self, big, i):
        self.end = time.time()
        logging.info(f'{big}总耗时:{timelogging.show(self.end)}s')
        with open('config.txt', 'a', encoding='utf-8') as f:
            f.write(f'{big}耗时 {self.end - self.start}+\n')
        timelogging.handled(i)

    def main(self, i):
        # print(i)
        # for i in range(1, 100):
        url = i
        url = f'{url // 1000}/{url}'
        link = []
        title = []
        Big_title = self.base_info(url)
        if not self.flag:
            # print(self.flag)
            link, title = self.page_info(url, 1, link, title)

            max = len(link)
            if max > 20:
                max = 20

            task_queue = queue.Queue()
            for i in range(len(link)):
                partial_task_function = partial(task_function2, link[i], 1, Big_title, title[i])
                task_queue.put(partial_task_function)

            with concurrent.futures.ThreadPoolExecutor(max_workers=max) as executor:
                while not task_queue.empty():
                    task = task_queue.get()
                    executor.submit(task)

                executor.shutdown()
            self.time_diff(Big_title, url)


if __name__ == '__main__':
    timelogging = timelogging(time.time())


    def task_function(i):
        obj = No2_dybz(i)
        obj.main(i)
        # 执行任务的代码
    def task_function2(link, num, bigtitle, title):
        obj2 = No2_dybz(link)
        obj2.get_content(link, num, bigtitle, title)
    task_queue = queue.Queue()
    lists = []
    for i in range(44603, 1, -1):
        lists.append(i)
        task_queue.put(i)

    timelogging.base_handled(lists)
    # 创建多线程池
    num_threads = 20  # 线程数
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交任务给线程池执行
        while not task_queue.empty():
            task = task_queue.get()
            executor.submit(task_function, task)

        # 等待所有任务完成
        executor.shutdown()
