from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

mainUrl = "https://www.fotmob.com"
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def save_in_val_list(gk, df, mf, fw):
    with open('evaluation items/gk.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gk.append(row[0])
    with open('evaluation items/df.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            df.append(row[0])
    with open('evaluation items/mf.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mf.append(row[0])
    with open('evaluation items/fw.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fw.append(row[0])
    return


def save_in_url_list(gk, df, mf, fw):
    with open('url/gk_url.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gk.append(row[0])
    with open('url/df_url.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            df.append(row[0])
    with open('url/mf_url.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mf.append(row[0])
    with open('url/fw_url.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fw.append(row[0])
    return

def get_player_info(result, urls, eval):
    for url in urls:
        wd.get(mainUrl + url)
        
        try:
            # 버튼 클릭 대기
            button = wd.find_element(By.CLASS_NAME, 'css-a7bq51-FilterButton.e1tb2kvp1')
            button.click()
            
            # 페이지 소스 가져오기
            soupPlayer = BeautifulSoup(wd.page_source, 'html.parser')
            source = soupPlayer.select("div.css-17js6f6-PlayerPageGridCSS.e17ysukt0 > div.css-14y4cbw-Column-LeftColumnCSS.e17ysukt1 > div.css-1wb2t24-CardCSS.e1mlfzv61")
            
            # 선수 정보를 담을 리스트
            temp = []
            
            # 선수 이름, 키, 나이, 시장 가치 가져오기
            info = source[0]
            name = info.select("div.css-1l2h5po-NameAndTeam.e1uunyvp4 > h1.css-zt63wq-PlayerNameCSS.e1uunyvp1")
            temp.append(name[0].string)
            height_and_age = info.select("div.css-to3w1c-StatValueCSS.e55tcbm4")
            height = height_and_age[0].select("span")
            temp.append(height[0].string)
            age = height_and_age[2].select("span")
            temp.append(age[0].string)
            value = height_and_age[5].select("span")
            temp.append(value[0].string)
            
            # 선수 출전 시간 가져오기
            time = source[1]
            time = time.select("div.css-170fd60-StatValue.e1ahduwc5 > span")
            temp.append(time[4].string)
            
            # 선수 기록 가져오기
            stats = source[3]
            records = stats.select("div.css-17zw5kc-StatCSS.e1uibvo13 > div.css-jb6lgd-StatValue.e1uibvo12 > span")
            stats = stats.select("div.css-2duihq-StatTitle.e1uibvo11")
            
            for stat, record in zip(stats, records):
                if stat.string in eval:
                    temp.append(record.string)
                else:
                    pass
            
            result.append(temp)
        
        except Exception as e:
            pass
    return


def main():
    gkeval = []; dfeval = []; mfeval = []; fweval = []
    gkurl = []; dfurl = []; mfurl = []; fwurl = []
    gkstats = []; dfstats = []; mfstats = []; fwstats = []
    
    save_in_val_list(gkeval, dfeval, mfeval, fweval)
    save_in_url_list(gkurl, dfurl, mfurl, fwurl)
    
    get_player_info(gkstats, gkurl, gkeval)
    get_player_info(dfstats, dfurl, dfeval)
    get_player_info(mfstats, mfurl, mfeval)
    get_player_info(fwstats, fwurl, fweval)
    
    with open('players info/gk.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in gkstats:
            writer.writerow(item)
    with open('players info/df.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in dfstats:
            writer.writerow(item)
    with open('players info/mf.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in mfstats:
            writer.writerow(item)
    with open('players info/fw.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in fwstats:
            writer.writerow(item)

if __name__ == '__main__':
    main()