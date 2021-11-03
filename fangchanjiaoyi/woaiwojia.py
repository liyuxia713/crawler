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
    f = open('%s_在售_我爱我家.csv' % xiaoquName, mode='w', encoding='utf-8-sig', newline='')
    fieldnames = ['页数', '序号', '标题', '挂牌价格', '单价', '几室', '面积', '朝向', '装修', '楼层', '年代', '楼型', '满几', '发布时间', '关注人数', 'url']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()


    num = 1
    for page in range(1, pagenum):
        print('===========================正在下载第{}页数据================================'.format(page))
        time.sleep(1)
        url = 'https://bj.5i5j.com/ershoufang/n{}/_{}/?wscckey=fc79b57125b315d6_1604753284'.format(page, xiaoquID)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Host':'bj.5i5j.com',
            'Cookie':'yfx_c_g_u_id_10000001=_ck18081719592816058111722915307; yfx_mr_n_10000001=baidu%3A%3Amarket_type_ppzq%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3Abj.5i5j.com%3A%3A%3A%3A%3A%3A%25E5%25B7%25A6%25E4%25BE%25A7%25E6%25A0%2587%25E9%25A2%2598%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3A160%3A%3Apmf_from_adv%3A%3Abj.5i5j.com%2F; yfx_mr_f_n_10000001=baidu%3A%3Amarket_type_ppzq%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3Abj.5i5j.com%3A%3A%3A%3A%3A%3A%25E5%25B7%25A6%25E4%25BE%25A7%25E6%25A0%2587%25E9%25A2%2598%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3A160%3A%3Apmf_from_adv%3A%3Abj.5i5j.com%2F; yfx_key_10000001=; _ga=GA1.2.1273546397.1534507170; _gid=GA1.2.550673808.1534507170; ershoufang_cookiekey=%5B%22%257B%2522url%2522%253A%2522%252Fershoufang%252Fhuilongguan%253Fzn%253D%25E5%259B%259E%25E9%25BE%2599%25E8%25A7%2582%2522%252C%2522x%2522%253A%2522116.34232%2522%252C%2522y%2522%253A%252240.07642%2522%252C%2522name%2522%253A%2522%25E5%259B%259E%25E9%25BE%2599%25E8%25A7%2582%2522%252C%2522total%2522%253A903%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fershoufang%252F_%2525E5%25259B%25259E%2525E9%2525BE%252599%2525E8%2525A7%252582%253Fzn%253D%2525E5%25259B%25259E%2525E9%2525BE%252599%2525E8%2525A7%252582%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E5%259B%259E%25E9%25BE%2599%25E8%25A7%2582%2522%252C%2522total%2522%253A%25220%2522%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fershoufang%252F_%2525E6%2525B2%2525A7%2525E5%2525B7%25259E%253Fzn%253D%2525E6%2525B2%2525A7%2525E5%2525B7%25259E%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E6%25B2%25A7%25E5%25B7%259E%2522%252C%2522total%2522%253A%25220%2522%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fershoufang%252Fsubway%252Fss227%253Fzn%253D%25E5%258C%2597%25E4%25BA%25AC%25E8%25A5%25BF%25E7%25AB%2599%2522%252C%2522x%2522%253A%2522116.32785%2522%252C%2522y%2522%253A%252239.900659%2522%252C%2522name%2522%253A%2522%25E5%258C%2597%25E4%25BA%25AC%25E8%25A5%25BF%25E7%25AB%2599%2522%252C%2522total%2522%253A7%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fershoufang%252F_%2525E5%25258C%252597%2525E4%2525BA%2525AC%253Fzn%253D%2525E5%25258C%252597%2525E4%2525BA%2525AC%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E5%258C%2597%25E4%25BA%25AC%2522%252C%2522total%2522%253A%25220%2522%257D%22%5D; PHPSESSID=fc7nsge60ke6rd0qq67tqtji0t; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1534507171,1534580017; _Jo0OQK=1D2AE2E67E6421679A4B7178E87CA6A8C29565C26CCD4F7C8792B1BB9E0427D8C38F695D683F619358B323F95E0E7F58EE9B1F49E79B8CFFC450CAE96B56B94820FC57212F12283777C840763663251ADEB840763663251ADEB4A0CDD8122A5BE5F6ECAC92C8E815B0AGJ1Z1fA==; domain=bj; _gat=1; yfx_f_l_v_t_10000001=f_t_1534507168588__r_t_1534658789575__v_t_1534677148504__r_c_2; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1534677149',
        }

        response = requests.get(url=url, headers=headers)
        response = requests.get(url=url)
        print(response.text)
        selector = parsel.Selector(response.text)
        lis = selector.css('.pList li')
        print(lis)
        lis = selector.css('.ListCon div')
        print(lis)
        for li in lis:
            print(li)
            # 各字段初始化
            dit = {}
            for col in fieldnames:
                dit[col] = ''
            dit['页数'] = page
            dit['序号'] = num
            num += 1

            # 解析页面字段
            dit['标题']  = li.css('.listCon a::text').get()
            dit['url'] = 'https://bj.5i5j.com/{}'.format(li.css('.title a::attr(href)').get())
            dit['挂牌价格'] = li.css('.jia p::text').get()
            print(dit)
            continue
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
