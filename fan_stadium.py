from bs4 import BeautifulSoup
import requests
import sys
import datetime
from datetime import timedelta
FS_RANK_URL="http://fs.sports.news.naver.com/player/rank/list?startDate="

def get_until_today(previous=0): #오늘 날짜 데이터를 -로 구분하여 표현한다
    #now=time.localtime()-1
    #date="%04d-%02d-%02d"%(now.tm_year, now.tm_mon, now.tm_mday)
    cal_date=datetime.date.today()-timedelta(days=int(previous))
    return cal_date
    

def making_rank_url(date,page_num):
    block1="http://fs.sports.news.naver.com/player/rank/list?startDate="
    block2="&hpType=0&rankType=D&searchText=&page="
    #now=time.localtime()
    return block1+str(date)+block2+str(page_num)

def sort_second_ele(x):
    return x[1]

class fan_stadium(object):
    
    def __init__(self):
        self.play_real_rank=[]
        self.play_name=[]
        #self.play_pos=[]
        self.play_score=[]
        self.play_team=[] #추후 선수별 팀 정보를 담을 변수
        self.play_count=[]
        self.play_avg=[]
        
        self.print_pages=0
        self.print_previous=0
        self.print_top_players=0
    def sort_play_avg_data(self, rev=True):
        self.play_avg.sort(key=sort_second_ele, reverse=rev)
            
    def sort_play_data(self, rev=True): #점수의 두번째 데이터로 정렬한다
        #print(self.play_score)
        self.play_score.sort(key=sort_second_ele, reverse=rev)
        #print(self.play_score)
    
    def get_highest_player(self, top_players, option=1):
        ret=[]
        print("options is : %d" % option)
        if option==1: #1인데 1넣으면 에러남 이유가 뭐지,..>?
            self.sort_play_data()
            sort_par=self.play_score
        elif option==2:
            self.sort_play_avg_data()
            sort_par=self.play_avg
        else:
            print("Please input 0(total) OR 1(average score")
            sys.exit(2)
        
        for i in range(top_players):
            for j in range(len(self.play_name)):
                if self.play_score[i][0]==self.play_name[j][0]:
                    ret.append([self.play_team[j][1], self.play_name[j][1], sort_par[i][1], self.play_count[j][1]])
                    break            
        self.top_players=top_players        
        return ret
    
    def crawl_player_data(self, pages, days):
        #url=self.url_fs_rank+str(date)+...
        #urlURL 가져오는 방법을 바꿔서 여러 페이지를 가져올 수 있도록 해야함
        previous_day=1
        #어제부터 5 기준으로 구하기로
        while(1):
            cur_page=1
            while(1):
                rank_url=making_rank_url(get_until_today(previous_day),cur_page)
                url=requests.get(rank_url)
                soup=BeautifulSoup(url.text, 'lxml')
                
                name_data=soup.find_all("td",{"class":"player"})
                name_data=str(name_data).split("</td>")
                point_data=soup.find_all("td", {"class":"total_point"})
                point_data=str(point_data).split("  </td>")
                
                #team_data=soup.find_all("td", {"class":"player"})
                team_data=str(name_data).split("<td class=\"player\"><img alt=")
                #print(team_data)
                #for i in range(1,len(team_data)):
                #    print(team_data[i].split('\" src=')[0].split("\"")[1])#team_data[i].split('\" src=')

                #team data는 나중에 가져오기로
                                
                #print(point_data)
                if(len(point_data)!=len(name_data)):
                    print("It is uncorrecd parsing, point data != name data")
                    
                for i in range(len(point_data)-1):
                    new_value=False
                    for j in range(len(self.play_name)):
                        #print(name_data[i].split("\"/> ")[1]+"\t\t"+self.play_name[j][1])
                        if name_data[i].split("\"/> ")[1]==self.play_name[j][1]:
                            #print(j+" , "+name_data[i].split("\"/> ")[1]) 
                            self.play_score[j][1]=self.play_score[j][1]+int(point_data[i].split("\"> ")[1])
                            self.play_count[j][1]=self.play_count[j][1]+1
                            self.play_avg[j][1]=self.play_score[j][1]/self.play_count[j][1]
                            #slef.play_count[j][1]++
                            new_value=True
                            break
                    if new_value==False:
                        self.play_score.append([len(self.play_score)-1, int(point_data[i].split("\"> ")[1])]) # 포인트 데이터
                        self.play_name.append([len(self.play_name)-1,name_data[i].split("\"/> ")[1]]) # 이름 데이터
                        self.play_count.append([len(self.play_count)-1,1]) # 출전 횟수를 저장하는 변수
                        self.play_avg.append([len(self.play_avg)-1,self.play_score[i][1]/self.play_count[i][1]])
                        if(i==len(point_data)-1):
                            continue
                        else:
                            self.play_team.append([len(self.play_team)-1, team_data[i+1].split('\" src=')[0].split("\"")[1]])
                #print(name_data)
                cur_page=cur_page+1
                
                if cur_page>pages:
                    break
                
            previous_day=previous_day+1
            if previous_day>days:
                break
        self.print_pages=pages
        self.print_previous=previous_day #함수가 정상적으로 실행되었는지를 판별하기 위해 가장 마지막에 변수를 초기화 한다
        
    def print_formatting(self, players, option=1): #몇 명의 선수를 출력할지 입력!'
        ret=""
        if(self.print_pages==0 and self.print_previous==0 and self.print_top_players==0): #아직 crawl 함수가 정상적으로 실행되지 않았음을 의미
            print("=== Please execute 'crawl_player_data' previously ===")
            sys.exit(1)
        else:
            #print("option value : %d" % option)
            if option==1:
                str_best="Best Total Pointer LINE-UP"
            elif option==2:
                str_best="Best Average pointer LINE-UP"
            else:    
                print(" twPlease input 1(total) OR 2(average score)")
                sys.exit(2)
            top=self.get_highest_player(players, option)
            ret="* "+str(get_until_today(self.print_previous))+" ~ "+str(get_until_today(1))+"\n* "+str_best+".\n"
            for i in range(len(top)):
                ret+="   "+str(i+1)+" :  "+top[i][0]+" - "+top[i][1]+" // "+str(top[i][2])+" pts // "+str(top[i][3])+" plays\n"
        return ret
            
"""
if __name__=="__main__":
    f1=fan_stadium()
    f1.crawl_player_data(1,1)
    
    #print(get_until_today(4))
    #for i in len(f1.play_name):
    #print(f1.play_name)
    #print(f1.play_name)
    #print(f1.play_score)
    #print(f1.get_highest_player(5))
    #for j in f1.play_name:
    #    print(j[1])
    #cal_date=datetime.date.today()-timedelta(days=1)
    #cal_date="%04d-%02d-%02d"%(cal_date.tm_year, cal_date.tm_mon, cal_date.tm_mday)
"""