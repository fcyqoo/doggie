# coding: utf-8
import requests
from lxml import etree
import json
import os

class ControlConfig():
    i = 0  # 循环控制器
    j = 0
    k = 0
    z = 0
    m = 0
    n = 0


class DoggieWikiCrawler(object):

    def get_url(self):

        with open("./../data/base.json", "r") as f:
            r = f.read()
            data = json.loads(r)

        url_list = []
        for node in data:
            url = node['detail_url']
            if url in url_list:
                continue
            url_list.append(url)

        return url_list

    def get_html(self, url):

        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print("fail in :", url)

    def data_config(self, control_config=None):

        config = [

            {
                "name": "chinese_name",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/span",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "english_name",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/a",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "other_name",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[1]/td[1]/a[2]",
                "data_type": "table",
                "data_num": 1
            },
            {
                "name": "homeland",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[2]/td[1]/a[2]",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "dog_size",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[2]/td[2]/a[2]",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "dog_type",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[3]/td[2]/a[2]",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "dog_personality",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[6]/td/a[2]",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "dog_description",
                "xpath": "/html/body/div[2]/div[3]/div[2]/ul/li[3]/div[2]/p",
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "dog_age_min",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[5]/td[1]/a[2]",
                "data_type": "range_min",
                "data_num": 1
            },
            {
                "name": "dog_age_max",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[5]/td[1]/a[2]",
                "data_type": "range_max",
                "data_num": 1
            },
            {
                "name": "dog_price_refer",
                "xpath": "/html/body/div[2]/div[2]/div/div[2]/table/tr[5]/td[2]/a[2]",
                "data_type": "price",
                "data_num": 1
            },

        ]
        return config

    def get_data(self, html):

        data_list = []
        config = self.data_config()

        data_node = {}

        for node in config:
            xpath = node['xpath']
            name = node['name']
            data_type = node['data_type']

            html_etree = etree.HTML(html)
            html_data = html_etree.xpath(xpath)

            try:
                if name == 'table':
                    data_node[name] = html_data[0].text

                if data_type == 'text' and html_data:
                    data_node[name] = html_data[0].text

                if data_type == 'image':
                    print(">>>>image")
                    data_node[name] = html_data[0].attrib['src']

                if data_type == "url":
                    print(">>>>>url")
                    data_node[name] = html_data[0].attrib['href']

                if data_type == "range_min":
                    data_node[name] = html_data[0].text.split('-')[0]

                if data_type == "range_max":
                    data_node[name] = html_data[0].text.split('-')[1]

            except Exception as ex:

                print(ex)

            # import pdb
            # pdb.set_trace()

        if data_node:
            data_list.append(data_node)

        print(">>>:", data_list, len(data_list))

        return data_list

    def save_data(self, path, data):
        json_str = json.dumps(data)
        with open(path, 'w') as f:
            f.write(json_str)

    def do_crawler(self):
        data = []

        url_list = self.get_url()

        for url in url_list:
            print("url:", url)

            html = self.get_html(url)
            data += self.get_data(html)

        self.save_data("./../data/info.json", data)


if __name__ == "__main__":

    doggieWikiCrawler = DoggieWikiCrawler()
    doggieWikiCrawler.do_crawler()

    pass





