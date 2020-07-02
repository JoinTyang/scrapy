# -*- coding: utf-8 -*-
import json
from copy import deepcopy

import scrapy


class XueersiSpider(scrapy.Spider):
    name = 'xueersi'
    allowed_domains = ['xueersi.com']
    start_urls = ['https://mall.xueersi.com/cs/grades']


    def parse(self, response):
        url = response.url
        print(url)
        grades = response.body
        grades = json.loads(grades.decode("utf-8"))
        print(grades)
        print(len(grades))
        for grade in grades:
            # item={}
            id = grade["id"]
            name = grade["name"]
            url = "https://mall.xueersi.com/courses/list/1/5/100/"+str(id)+"/0?switch_grade="+str(id)+\
                  "&switch_subject=-1&subjectId=0&curpage=1"
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        url = response.url
        print("url:  "+url)
        details = json.loads(response.body.decode())
        print("长度：")
        print(len(details))
        # detail_list = []
        for detail in details:
            detail_dict = {}
            detail_dict["name"] = detail["name"]
            detail_dict["secondTitle"] = detail["secondTitle"]
            detail_dict["id"] = detail["id"]
            detail_dict["class_id"] = detail["class"]["id"]
            detail_dict["price"] = {}
            detail_dict["price"]["origin"] = detail["price"]["origin"]
            detail_dict["price"]["resale"] = detail["price"]["resale"]
            detail_dict["subject_name"] = detail["subjects"][0]["name"]
            detail_dict["difficulty"] = detail["difficulty"]["alias"]
            detail_url = "http://www.xueersi.com/course-detail/"+str(detail_dict["id"])+"/"+str(detail_dict["class_id"])
            detail_dict["detail_url"] = detail_url

            yield detail_dict

        if len(details)==9:
            print("next++++++++++++++++++++++++++++++++++++++++++++++++++++")
            l=url.split("&")[:-1]
            s = 'curpage=' + str(int(url.split("&")[-1].split("=")[1]) + 1)
            l.append(s)
            next_url = "&".join(l)
            # next_url=url[:-1]+str(item["curpage"])
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_detail,meta={"item":deepcopy(detail_dict)})


