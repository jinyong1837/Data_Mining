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

def get_team_url(result):
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
    return


def make_url_csv(GK, DF, MF, FW):
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


def get_meaningful_data(result, codes, real_codes):
    for code in codes:
        wd.get(mainUrl + code)
        time.sleep(1)
        
        try:
            # 버튼 클릭 대기
            button = wd.find_element(By.CLASS_NAME, 'css-a7bq51-FilterButton.e1tb2kvp1')
            button.click()
            
            # 페이지 소스 가져오기
            soupPlayer = BeautifulSoup(wd.page_source, 'html.parser')
            stats = soupPlayer.select("div.css-17js6f6-PlayerPageGridCSS.e17ysukt0 > div.css-14y4cbw-Column-LeftColumnCSS.e17ysukt1 > div.css-1wb2t24-CardCSS.e1mlfzv61")
            stats = stats[3]
            stats = stats.select("div.css-2duihq-StatTitle.e1uibvo11")
            
            for stat in stats:
                if stat.string in result:
                    result[stat.string] += 1
                else:
                    result[stat.string] = 1
            
            if len(stats) != 0:
                real_codes.append(code)
            
        except Exception as e:
            pass
    return


def make_evaluation_items_csv(GK, DF, MF, FW):
    gktemp = []; dftemp = []; mftemp = []; fwtemp = []
    for key, value in GK.items():
        if value == GK['경고']:
            gktemp.append(key)
    for key, value in DF.items():
        if value == DF['경고']:
            dftemp.append(key)
    for key, value in MF.items():
        if value == MF['경고']:
            mftemp.append(key)
    for key, value in FW.items():
        if value == FW['경고']:
            fwtemp.append(key)
    with open('evaluation items/gk.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in gktemp:
            writer.writerow([item])
    with open('evaluation items/df.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in dftemp:
            writer.writerow([item])
    with open('evaluation items/mf.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in mftemp:
            writer.writerow([item])
    with open('evaluation items/fw.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in fwtemp:
            writer.writerow([item])
    return


def main():
    teamCode = []
    TempGKCodes = []; TempDFCodes= []; TempMFCodes = []; TempFWCodes = []
    GKCodes = []; DFCodes= []; MFCodes = []; FWCodes = []
    playerStats = []
    GKStatDic = {}; DFStatDic = {}; MFStatDic = {}; FWStatDic = {}
    
    get_team_url(teamCode)
    get_player_url(TempGKCodes, TempDFCodes, TempMFCodes, TempFWCodes, teamCode)
    
    get_meaningful_data(GKStatDic, TempGKCodes, GKCodes)
    get_meaningful_data(DFStatDic, TempDFCodes, DFCodes)
    get_meaningful_data(MFStatDic, TempMFCodes, MFCodes)
    get_meaningful_data(FWStatDic, TempFWCodes, FWCodes)
    
    make_url_csv(GKCodes, DFCodes, MFCodes, FWCodes)
    make_evaluation_items_csv(GKStatDic, DFStatDic, MFStatDic, FWStatDic)

if __name__ == '__main__':
    main()