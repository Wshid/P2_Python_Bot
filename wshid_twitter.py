import tweepy
 
CONSUMER_KEY = 'yORbHBox3ejItINAsbQNHMTEV'
CONSUMER_SECRET = 'QTdCmRGeewcWR7fcdramz3xPVeeKRnlhGFVZ2y2N4rBpHVTEgD'
ACCESS_KEY = '2356214425-Hx5p8ACt9eVftBlrcChwQstz1ACckX7t2lUXhCt'
ACCESS_SECRET = 'uYONmjy48UH2fyDZF5lw4omyn8zs5E6hdgGU93Og9aRKA'

class wshid_twitter(object):
    
    # For setting authorization
    def __init__(self, c_key='yORbHBox3ejItINAsbQNHMTEV', c_sec='QTdCmRGeewcWR7fcdramz3xPVeeKRnlhGFVZ2y2N4rBpHVTEgD', a_key='2356214425-Hx5p8ACt9eVftBlrcChwQstz1ACckX7t2lUXhCt', a_sec='uYONmjy48UH2fyDZF5lw4omyn8zs5E6hdgGU93Og9aRKA'):
        self.c_key=CONSUMER_KEY
        self.c_sec=CONSUMER_SECRET
        self.a_key=ACCESS_KEY
        self.a_sec=ACCESS_SECRET
        self.auth = tweepy.OAuthHandler(self.c_key, self.c_sec)
        self.auth.set_access_token(self.a_key, self.a_sec)
        self.api = tweepy.API(auth_handler=self.auth, api_root='/1.1', secure=True)
        
        self.my_timeline=[]
        
    def mention(self, str):
        self.api.update_status(str)
        print("Success mention : \n\n\n%s" % str)
    
    def list_timeline(self):
        #print(tweepy.Cursor(self.api.user_timeline).items())
        for status in tweepy.Cursor(self.api.user_timeline).items(): #Object를 가져온다
        # process status here
            #self.process_status(status)
            self.my_timeline.append(status.text)
            
    def get_timeline_all(self):
        ret=""
        for i in range(len(self.my_timeline)):
            ret+=str(i+1)+" : "+self.my_timeline[i]+"\n"
        return ret
    
    def get_timeline(self, num): # 실제 인덱스는 0부터 시작하므로, 해당 번째에 맞게 출력
        return self.my_timeline[num-1]
            
"""
if __name__ == "__main__":
    tw=wshid_twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET);
    tw.list_timeline() # TimeLine 정보 로드
    print(tw.get_timeline(1)+"\n"=="두산 : 유희관\nNC : 스튜어트") # 실제 출력 부분
"""