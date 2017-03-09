##보니까 선발이 미정인 경우 파싱을 해오지 않음. 이를 예외처리 하거나 해야할듯

import requests
from bs4 import BeautifulSoup
import re #split을 사용하기 위함

URL_TODAY_TEAM="http://www.koreabaseball.com/Schedule/ScoreBoard/ScoreBoard.aspx"
URL_SCHEDULE="http://sports.news.naver.com/kbaseball/schedule/index.nhn"

class kbo(object):
    
    def __init__(self, url_today_team):
        self.today_team=[]
        self.today_starting=[]
        self.url_sb=requests.get(url_today_team)
    
  #  def list_today_team(self):
  #      get_url=requests.get(URL_TODAY_TEAM)
  #      soup=BeautifulSoup(self.url_sb.text, "lxml")
  #      data=str(soup.find_all("th", {"scope":"row"}))
  #      data=data.split("</th>")
  #      for i in range(len(data)-1):
  #          self.today_team.append(data[i].split("\">")[1])
    
    def list_starting(self): #금일 선발투수와 팀을 가져온다
        url=requests.get(URL_SCHEDULE)
        soup=BeautifulSoup(url.text, "lxml")
        s_data=soup.find_all("span", {"class":"game_info"})
        s_data=str(s_data).split("</a></span>")
        ##print(s_data)
        for i in range(len(s_data)-1):
            self.today_starting.append(s_data[i].split("target=\"_blank\">")[1])
        
        t_data=soup.find_all("p", {"class" : "vs_team"})#.find_all("div", {"class":"vs_team"}) ###종속적으로 태그 가져오는 방법?
        t_data=str(t_data).split("</strong>")
        #print(t_data)
        for i in range(len(t_data)-1):
            self.today_team.append(re.split("<strong>|home2\">", t_data[i])[1])
        
    def get_today_team(self):
        return self.today_team
        #for i in range(len(self.today_team)):
        #    print(self.today_team[i])  
            
    def get_today_starting(self):
        return self.today_starting
        #for i in range(len(self.today_starting)):
        #    print(self.today_starting[i])
    
    def get_today_num(self):
        return len(self.today_team)

if __name__=="__main__":
    kb1=kbo(URL_TODAY_TEAM)
    kb1.list_starting()
    ret=""
    team_list=kb1.get_today_team()
    start_list=kb1.get_today_starting()
    #print(len(team_list))
    print(team_list[5])
    print(team_list)
    print(start_list)
    for i in range(len(team_list)):
        ret+="\t"+team_list[i]+" : "+start_list[i]+"\n"
    print(ret)
