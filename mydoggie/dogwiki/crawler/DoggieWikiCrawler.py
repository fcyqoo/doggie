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
        for i in range(ord("A"), ord("Z") + 1):
            url = "http://www.goupu.com.cn/dog/s-4-0-" + chr(i) + "-0-0-0-0.html"
            yield url

    def get_html(self, url):

        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print("fail in :", url)

    def data_config(self, control_config):

        config = [

            {
                "name": "name",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[2]" % control_config.i,
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "english_name",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[3]" % control_config.i,
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "personality",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[4]" % control_config.i,
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "price",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[5]/a" % control_config.i,
                "data_type": "text",
                "data_num": 1
            },
            {
                "name": "image",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[1]/a/img" % control_config.i,
                "data_type": "image",
                "data_num": 1
            },
            {
                "name": "detail_url",
                "xpath": "/html/body/div[2]/div/div[1]/div[2]/ul/li[%d]/div[6]/dl/dd[1]/a" % control_config.i,
                "data_type": "url",
                "data_num": 1
            },


        ]
        return config

    def get_data(self, html):

        data_list = []
        control_config = ControlConfig()

        for i in range(1, 22):
            data_node = {}
            control_config.i = i
            config = self.data_config(control_config)

            for node in config:
                xpath = node['xpath']
                name = node['name']
                data_type = node['data_type']

                html_etree = etree.HTML(html)
                html_data = html_etree.xpath(xpath)

                try:
                    if data_type == 'text' and html_data:
                        data_node[name] = html_data[0].text

                    if data_type == 'image':
                        print(">>>>image")
                        data_node[name] = html_data[0].attrib['src']

                    if data_type == "url":
                        print(">>>>>url")
                        data_node[name] = html_data[0].attrib['href']

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
        for url in self.get_url():
            print("url:", url)

            html = self.get_html(url)
            data += self.get_data(html)

        self.save_data("./../data/base.json", data)


if __name__ == "__main__":

    doggieWikiCrawler = DoggieWikiCrawler()
    doggieWikiCrawler.do_crawler()

    pass





