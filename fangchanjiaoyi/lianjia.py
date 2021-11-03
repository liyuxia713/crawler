#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
爬取链家的在售房源信息和已交易房源信息
适合爬取少量小区的信息，因为需要手动提供小区的url，相关数据有几页等。
'''
import requests
import parsel
import time
import csv


def sellInfoByXiaoqu(xiaoquID, pagenum, xiaoquName):
    '''
    抓取指定小区的在售房源信息，写入csv文件
    @In:
        xiaoquID: 小区的id，用于拼接url
        pagenum: 在售页面的总数
        xiaoquName: 小区名字
    @out: 写入文件： 
        文件名： 小区名字_在售.csv
    '''
    f = open('%s_在售.csv' % xiaoquName, mode='w', encoding='utf-8-sig', newline='')
    fieldnames = ['页数', '序号', '标题', '挂牌价格', '单价', '几室', '面积', '朝向', '装修', '楼层', '年代', '楼型', '满几', '发布时间', '关注人数', 'url']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()


    num = 1
    for page in range(1, pagenum):
        print('===========================正在下载第{}页数据================================'.format(page))
        time.sleep(1)
        url = 'https://bj.lianjia.com/ershoufang/pg{}{}/'.format(page, xiaoquID)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        lis = selector.css('.sellListContent li')
        for li in lis:
            # 各字段初始化
            dit = {}
            for col in fieldnames:
                dit[col] = ''
            dit['页数'] = page
            dit['序号'] = num
            num += 1

            # 解析页面字段
            dit['标题']  = li.css('.title a::text').get()
            dit['url'] = li.css('.title a::attr(href)').get()
            dit['挂牌价格'] = li.css('.totalPrice span::text').get()
            dit['单价'] = li.css('.unitPrice span::text').get().replace('单价', '').replace('元/平米', '') #单价53036元/平米
            houseInfo = li.css('.houseInfo::text').get() #3室1厅 | 114.64平米 | 南 北 | 精装 | 低楼层(共34层) | 2014年建 | 板塔结合
            # 车位 | 34.07平米 | 北 | 2015年建 | 板塔结合
            followInfo = li.css('.followInfo::text').get() #25人关注 / 1个月以前发布
            tag = li.css('.tag span::text').getall()
            if houseInfo is not None:
                cols = ['几室', '面积', '朝向', '装修', '楼层', '年代', '楼型']
                values = houseInfo.split(' | ')
                if len(cols) == len(values):
                    for i in range(0, len(cols)):
                        dit[cols[i]] = values[i]
            if followInfo is not None:
                cols = ['关注人数', '发布时间']
                values = followInfo.split(' / ')
                for i in range(0, len(cols)):
                    dit[cols[i]] = values[i]
            for value in tag:
                if value.find('房本') >= 0:
                    dit['满几'] = value.replace('房本', '')
            csv_writer.writerow(dit)

            print(dit)


def dealInfoByXiaoqu(xiaoquID, pagenum, xiaoquName):
    '''
    抓取指定小区的已成交房源信息，写入csv文件
    @In:
        xiaoquID: 小区的id，用于拼接url
        pagenum: 在售页面的总数
        xiaoquName: 小区名字
    @out: 写入文件： 
        文件名： 小区名字_成交.csv
    '''
    f = open('%s_成交.csv' % xiaoquName, mode='w', encoding='utf-8-sig', newline='')
    fieldnames = ['页数', '序号', '小区名称', '小区建成日期', '楼层', '几室', '面积', '朝向', '装修', '交易价格', '交易日期', '单价', '满几', '挂牌价', '成交周期', 'url']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()

    num = 1
    for page in range(1, pagenum):
        print('===========================正在下载第{}页数据================================'.format(page))
        time.sleep(1)
        url = 'https://bj.lianjia.com/chengjiao/pg{}{}/'.format(page, xiaoquID)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        lis = selector.css('.listContent li')
        for li in lis:
            # 各字段初始化
            dit = {}
            for col in fieldnames:
                dit[col] = ''
            dit['页数'] = page
            dit['序号'] = num
            num += 1

            # 解析页面字段
            try:
                [xiaoqu, jishi, area] = li.css('.title a::text').get().split(' ')
                dit['小区名称']  = xiaoqu
                dit['几室'] = jishi
                dit['面积'] = area.replace('平米', '')
                dit['url'] = li.css('.title a::attr(href)').get()
                [orientation, zhuangxiu] = li.css('.houseInfo::text').get().split('|')
                dit['朝向'] = orientation
                dit['装修'] = zhuangxiu
                dit['交易价格'] = li.css('.totalPrice span::text').get()
                dit['交易日期'] = li.css('.dealDate::text').get()
                [totalfloor, houseyear]= li.css('.positionInfo::text').get().split(' ')
                dit['楼层'] = totalfloor
                dit['小区建成日期'] = houseyear
                dit['单价'] = li.css('.unitPrice span::text').get()
                a = li.css('.dealHouseInfo span::text').get()
                if a is not None:
                    dit['满几'] = a.replace('房屋', '')
                a = li.css('.dealCycleeInfo span::text').getall()
                if a is not None:
                    dit['挂牌价'] = a[0].replace('挂牌', '')
                    dit['成交周期'] = a[1].replace('成交周期', '')
            except:
                pass

            csv_writer.writerow(dit)

            print(dit)


if __name__ == '__main__':
    #dealInfoByXiaoqu('融泽家园', 47, '融泽家园')
    sellInfoByXiaoqu('融泽家园', 2, '融泽家园')
    #dealInfoByXiaoqu('rs国风美唐', 18, '国风美唐')
    #sellInfoByXiaoqu('rs国风美唐', 4, '国风美唐')
    #dealInfoByXiaoqu('c1111027381003', 77, '新龙城')
    #sellInfoByXiaoqu('c1111027381003', 5, '新龙城')
    #sellInfoByXiaoqu('c1111059006887', 3, '公园悦府')
    #dealInfoByXiaoqu('c1111059006887', 8, '公园悦府')
    #sellInfoByXiaoqu('rs金域华府', 4, '金域华府')
    #dealInfoByXiaoqu('rs金域华府', 13, '金域华府')