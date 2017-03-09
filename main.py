import time
import schedule
from kbo import *
from whsid_twitter import *
from fan_stadium import *
i=0

def tweet_schedule():
    global i
    i=i+1
    ret=str(i)+"\t printed"
    ws=whsid_twitter("yORbHBox3ejItINAsbQNHMTEV",'QTdCmRGeewcWR7fcdramz3xPVeeKRnlhGFVZ2y2N4rBpHVTEgD','2356214425-Hx5p8ACt9eVftBlrcChwQstz1ACckX7t2lUXhCt', 'uYONmjy48UH2fyDZF5lw4omyn8zs5E6hdgGU93Og9aRKA')
    ws.mention(ret)
    print(ret)

if __name__=="__main__":
    #print("It is main file")
    
    kb1=kbo("http://www.koreabaseball.com/Schedule/ScoreBoard/ScoreBoard.aspx")
    #ws=whsid_twitter("yORbHBox3ejItINAsbQNHMTEV",'QTdCmRGeewcWR7fcdramz3xPVeeKRnlhGFVZ2y2N4rBpHVTEgD','2356214425-Hx5p8ACt9eVftBlrcChwQstz1ACckX7t2lUXhCt', 'uYONmjy48UH2fyDZF5lw4omyn8zs5E6hdgGU93Og9aRKA')
    f1=fan_stadium()
    
    kb1.list_starting() # 팀과 선발을 가져온다
    ##team_list=kb1.get_today_team()
    ##start_list=kb1.get_today_starting()
    
    #ret="===금일 경기를 진행할 팀 : 선발투수===\n"
    #for i in range(len(team_list)):
    #    ret+="\t"+team_list[i]+" : "+start_list[i]+"\n"
    
    days=int(input("Evaluation Terms : "))
    players=int(input("The number of Top players : "))
    option=int(input("1 or 2, 1 means total point and 2 is average : "))
    print("Please wait... Calculating...")
    f1.crawl_player_data(3,days) #pages, days
    ret=f1.print_formatting(players, option) #players, option(1 or2, total or average)
    print(ret)
    #schedule.every(10).minutes.do(tweet_schedule)
    ##ws.mention(ret)
    
##    while(True):
##        schedule.run_pending()
##        time.sleep(1)