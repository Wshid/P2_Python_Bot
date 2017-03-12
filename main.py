import time
import schedule
from kbo import *
from wshid_twitter import *
from fan_stadium import *
global next_config

ment_count=0
iv="" #첫번째 실행여부 판단
is_frun=True
next_config=[]

def input_checker(i_msg, e_msg, *args): #입력받은 변수 / 에러시 출력할 메세지/ 보기 인자
    while(True):
        ret=input(i_msg)
        for i in args:
            if(i==ret):
                return i
        print(e_msg)
    return "ERROR"

def tw_schedule(): # cloud9에서 idle Session의 시간을 검증하는 함수
    #print("BB")
    global iv, is_frun, next_config
    ws=wshid_twitter()
    print("in tw_schedule")
    choice=next_config[0] # choice, days, players, option을 저장한 리스트
    
    print("choice : %d"%choice)
    
    if(is_frun==True):
        ws.mention(iv)
        is_frun=False #스위칭을 하여, 다음부터 실행되지 않도록 함
    else:
        if(choice==1):
            kb1=kbo("http://www.koreabaseball.com/Schedule/ScoreBoard/ScoreBoard.aspx")
            kb1.list_starting()
            ment=kb1.get_today_play()
        elif(choice==2):
            f1=fan_stadium()
            print("Please wait... Calculating...")
            f1.crawl_player_data(3,next_config[1]) #pages, days
            ment=f1.print_formatting(next_config[2], next_config[3])        #### 리스트
            #args는 차례대로,days, players, options를 의미
        else:
            print("Error on tw_schedule, incorrect choice value")
            sys.exit(4)
    
        ws.list_timeline()
        if(ment==(ws.get_timeline(1)+"\n")): #개행추가 이유 : 실제 ment를 만들때 개행이 추가됨
            print("Already exists same content on Timeline. Not upload the mention")
            # prev mention과 올릴 정보가 같으면 403(Forbidden)애러 발생. 사전 방지
        else:
            ws.mention(ment)

def tw_operate():
    global ment_count
    ment_count+=1
    is_tw=input_checker("if you twitting information regular terms? (y/n) ", "Please Input \'y\' or \'n\'", "y", "n")
    if is_tw=="y":
        stand=input_checker("term standard(minute, hour, day) : ", "Please Input \'minute\', \'hour\' or \'day\'", "minute", "hour", "day")
        if(stand=="minute"):
            term=int(input("Please Input Terms : "))
            print("Ment Counting... %d" % ment_count)
            schedule.every(term).minutes.do(tw_schedule) ####
        elif(stand=="hour"):
            term=int(input("Please Input Terms : "))
            print("Ment Counting... %d" % ment_count)
            schedule.every(term).hour.do(tw_schedule) ####
        else:
            while(True):
                hour=int(input("Please Input hour : "))
                if(hour<0 or hour >24):
                    print("Please Input hour, 0<=hour<=24")
                else:
                    break

            while(True):
                minute=int(input("Please Input minutes : "))
                if(minute<0 or minute >60):
                    print("Please Input hour, 0<=minute<=60")
                else:
                    break
            ontime=str(hour)+":"+str(minute)
            print("Ment Counting... %d" % ment_count)
            schedule.every().day.at(ontime).do(tw_schedule) ####
        
        while(True):
            schedule.run_pending() # 현재 상태를 1초마다 확인
            time.sleep(1)

def cm_operate(choice): # 금일 선발, 팀출력, 통계정보를 연산
    global iv
    ret=[]
    if(choice==1):
        kb1=kbo("http://www.koreabaseball.com/Schedule/ScoreBoard/ScoreBoard.aspx")
        kb1.list_starting()
        ment=kb1.get_today_play() #ment를 업데이트 하여, 추후 twit에 사용
        print(ment)
            ##team_list=kb1.get_today_team()
        ##start_list=kb1.get_today_starting()
        
        #ret="===금일 경기를 진행할 팀 : 선발투수===\n"
        #for i in range(len(team_list)):
        #    ret+="\t"+team_list[i]+" : "+start_list[i]+"\n"
        ret.append(choice)
        
    elif choice==2:
        f1=fan_stadium()
        days=int(input("Evaluation Terms(Until Today) : "))
        players=int(input("The number of Top players\n(if num>3, Can't set Regular task) : "))
        option=int(input("1 or 2, 1 means total point and 2 is average : "))
        print("Please wait... Calculating...")
        f1.crawl_player_data(3,days) #pages, days
        ment=f1.print_formatting(players, option) #players, option(1 or2, total or average)
        ret+=[choice, days, players, option] ####
        print(ment)
    else:
        print("ERROR")
    
    iv=ment
    return ret

if __name__=="__main__":
    choice=int(input_checker("Wshid Bot, Get KBO Info.==========\nPlease choice below menu =========\n1. Today's Line-up \n2. Compile Statistics of Best Player\n==============================\n", "\n\nPlease Input 1 or 2\n", "1", "2"))
    #print("choice is %d" %choice)
    next_config=cm_operate(choice) # 리스트 값의 반환값을 가진다.
    #print("NEXT CONFIG")
    #print(next_config)
    if(choice==2 and next_config[2]>3):
        pass
    else:
        tw_operate()

    #schedule.every(1).minutes.do(tw_schedule)
    ##ws.mention(ret)
    
##    while(True):
##        schedule.run_pending()
##        time.sleep(1)

"""
def twitter_mention(text):
    ws=wshid_twitter()
    ws.mention(text)
    #schedule.every(10).minutes.do(job)
    #schedule.every().hour.do(job)
    #schedule.every().day.at("10:30").do(job)
    #schedule.every().monday.do(job)
    #schedule.every().wednesday.at("13:15").do(job)
"""    