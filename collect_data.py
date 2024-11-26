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

def get_team_url(result):
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    wd.get(mainUrl + "/ko/leagues/47/overview/premier-league")
    time.sleep(1)
    
    teams = wd.find_elements(By.CLASS_NAME, 'css-jlnv70-TeamLink.exhos731')
    for team in teams:
        team_url = team.get_attribute('href')
        team_url = team_url.replace('/overview', '/squad')
        result.append(team_url)
    return


def get_player_url(GK, DF, MF, FW, team_url):
    for team in team_url:
        html = urllib.request.urlopen(team)
        soupTeam = BeautifulSoup(html, 'html.parser')
        playerPosition = soupTeam.select("div.css-10a1gry-SquadTilesWrapper.e1kl3u1z2")
        
        for i in range(1, 5):
            playerCodes = playerPosition[i].select("a")
            if i == 1:
                for code in playerCodes:
                    GK.append(code['href'])
            elif i == 2:
                for code in playerCodes:
                    DF.append(code['href'])
            elif i == 3:
                for code in playerCodes:
                    MF.append(code['href'])
            elif i == 4:
                for code in playerCodes:
                    FW.append(code['href'])

    with open('url/gk_url.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for code in GK:
            writer.writerow([code])
    with open('url/df_url.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for code in DF:
            writer.writerow([code])
    with open('url/mf_url.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for code in MF:
            writer.writerow([code])
    with open('url/fw_url.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for code in FW:
            writer.writerow([code])
    return


def stat_cnt(result, codes):
    for code in codes:
        wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wd.get(mainUrl + code)
        
        try:
            # 버튼 클릭 대기
            button = wd.find_element(By.CLASS_NAME, 'css-a7bq51-FilterButton.e1aie6871')
            button.click()
            
            # 페이지 로드 대기
            time.sleep(1)
            
            # 페이지 소스 가져오기
            soupPlayer = BeautifulSoup(wd.page_source, 'html.parser')
            stats = soupPlayer.select("div.css-2duihq-StatTitle.e1uibvo11")
            
            for stat in stats:
                if stat.string in result:
                    result[stat.string] += 1
                else:
                    result[stat.string] = 1
            
        except Exception as e:
            print()
    
    print(result)
    return


def get_player_info(result, codes):
    for code in codes:
        wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wd.get(mainUrl + code)
        
        try:
            # 버튼 클릭 대기
            button = wd.find_element(By.CLASS_NAME, 'css-a7bq51-FilterButton.e1aie6871')
            button.click()
            
            # 페이지 로드 대기
            time.sleep(1)
            
            # 페이지 소스 가져오기
            soupPlayer = BeautifulSoup(wd.page_source, 'html.parser')
            stats = soupPlayer.select("div.css-jb6lgd-StatValue.e1uibvo12 > span") 
            
            temp = []
            for stat in stats:
                temp.append(stat.string)
            result.append(temp)
        
        except Exception as e:
            print()
        
    wd.quit()
            
    return


def main():
    teamCode = []
    GKCodes = []; DFCodes= []; MFCodes = []; FWCodes = []
    playerStats = []
    GKStatDic = {}; DFStatDic = {}; MFStatDic = {}; FWStatDic = {}
    
    get_team_url(teamCode)
    get_player_url(GKCodes, DFCodes, MFCodes, FWCodes, teamCode)
    
    # stat_cnt(GKStatDic, GKCodes)
if __name__ == '__main__':
    main()