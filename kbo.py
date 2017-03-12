##보니까 선발이 미정인 경우 파싱을 해오지 않음. 이를 예외처리 하거나 해야할듯

import requests
from bs4 import BeautifulSoup
import re #split을 사용하기 위함

URL_TODAY_TEAM="http://www.koreabaseball.com/Schedule/ScoreBoard/ScoreBoard.aspx" # 
URL_SCHEDULE="http://sports.news.naver.com/kbaseball/schedule/index.nhn" # 금일 예정된 경기에 대해 크롤링할 페이지

class kbo(object): #kbo 객체 생성
    
    def __init__(self, url_today_team):
        self.today_team=[] # 금일 경기하는 팀 정보
        self.today_starting=[] #금일 선발에 대한 정보
        #self.url_sb=requests.get(url_today_team) 사용하지 않음
    
  #  def list_today_team(self):
  #      get_url=requests.get(URL_TODAY_TEAM)
  #      soup=BeautifulSoup(self.url_sb.text, "lxml")
  #      data=str(soup.find_all("th", {"scope":"row"}))
  #      data=data.split("</th>")
  #      for i in range(len(data)-1):
  #          self.today_team.append(data[i].split("\">")[1])
    
    def list_starting(self): # 금일 선발투수와 팀을 가져온다
        url=requests.get(URL_SCHEDULE)
        soup=BeautifulSoup(url.text, "lxml") # BeautifulSoup를 사용하여 크롤링
        s_data=soup.find_all("span", {"class":"game_info"}) # <span class='game_info'...>에 관련하여 정보를 가져온다.
        s_data=str(s_data).split("</a></span>") # </a><span>를 delimiter로 사용하여 구분한다.
        
        for i in range(len(s_data)-1):
            self.today_starting.append(s_data[i].split("target=\"_blank\">")[1]) # target=... 관련한 것으로 split하여 첫번째 요소를 오늘 선발 목록에 추가한다.
        
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        #print(self.today_starting)
        
        t_data=soup.find_all("p", {"class" : "vs_team"})#.find_all("div", {"class":"vs_team"}) ###종속적으로 태그 가져오는 방법?
        t_data=str(t_data).split("</strong>")

        for i in range(len(t_data)-1):
            self.today_team.append(re.split("<strong>|home2\">", t_data[i])[1]) # 금일 경기하는 팀 정보를 가져온다.
        
    def get_today_team(self): # OOP(Object Oriented Programming), 금일 팀을 가져오는 메소드
        return self.today_team

            
    def get_today_starting(self): # OOP, 금일 선발을 가져오는 메소드
        return self.today_starting
    
    def get_today_num(self): # OOP, 금일 경기하는 팀의 수를 리턴하는 메소드
        return len(self.today_team)
    
    def get_today_play(self): # 금일 선발 및 팀을 출력
        ret="=== 오늘 선발투수 ===\n"
        for i in range(self.get_today_num()):
            ret+=self.today_team[i]+" : "+self.today_starting[i]+"\n"
        return ret

"""
if __name__=="__main__":
    kb1=kbo(URL_TODAY_TEAM)
    kb1.list_starting() # 금일 선발투수와 팀 목록을 가져온다.
    ret=""
    team_list=kb1.get_today_team() # 금일 팀 목록 저장
    start_list=kb1.get_today_starting() # 금일 선발 목록 저장
    #print(len(team_list))
    print(team_list[5])
    print(team_list)
    print(start_list)
    for i in range(len(team_list)):
        ret+="\t"+team_list[i]+" : "+start_list[i]+"\n"
    print(ret)
"""