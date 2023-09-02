import pyttsx3
import speech_recognition as sr
from playsound import playsound
import datetime
import os
import time
import eyed3
import openai
import apikey
import wikipedia
import webbrowser



#TO BE DEVELOPED:
# need to work on todo list

# some of the variables used in main

error_log='error log.txt'
music_start_listen="sound.wav"
username='Snehanu'
chatStr=''

class assistant:
    '''
    the class for assistant.
    ''' 
    name="friday"#assistant name
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    tone_voice=voices[0].id#assistant voice
    
    '''
    set '1' for girl and '0' for boy
    '''
    engine.setProperty('voice',tone_voice)
    
    
    def speak(self,audio):
        '''
        Takes the string and speaks
        '''
        self.engine.say(audio)
        self.engine.runAndWait()
    
    def takeOrder(self):
        '''
        take the voice command for executing the orders after the assistant is activated
        '''
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            playsound(music_start_listen)
            r.pause_threshold=1
            audio = r.listen(source)
            try:
                print("Recognising....")
                order=r.recognize_google(audio, language="en-in")
                print(order)

            except Exception as e:
                with open(error_log, 'a') as f:
                    f.write(f'{datetime.datetime.now()}:{e}\n')
                self.speak("Sorry, I couldn't get it.")
                return "None"
            return order

    def takeorderoff(self):
        '''
         Helps to recognise if the user has called friday
        '''
        
        r=sr.Recognizer()
        with sr.Microphone() as source:
            # playsound(music_start_listen)#for testing when it is listening
            r.pause_threshold=1
            audio=r.listen(source)           
            try:
                order=r.recognize_google(audio, language="en-in")
                
            except Exception as e:
                with open(error_log, 'a') as f:
                    f.write(f'{datetime.datetime.now()}:{e}\n')
                return "None"
            return order

    def music_command(self):
        ''' take voice input from microphone '''
        r=sr.Recognizer()
        with sr.Microphone() as source:       
            print("Listening....")
            playsound(music_start_listen)
            r.  pause_threshold=1
            audio=r.listen(source)
            try:
                print("Recognising....")
                query=r.recognize_google(audio, language="en-IN")
                print(query)
            except Exception as e:
                with open(error_log, 'a') as f:
                    f.write(f'{datetime.datetime.now()}:{e}\n')
                self.speak("I couldn't get it.")
                return '-1'
        return query  
        
    def online_mesg(self):
        ''' 
        greets me as i enter 
        '''
        self.speak(f'I am online,{username}. You can call me whenever you want.')

    def wishMe(self):
        ''' 
        greets me as i exit
        '''
        hour=int(datetime.datetime.now().hour)
        if(hour>=20 and hour<3):
            self.speak(f'Good Night,{username}')
        else:
            self.speak("I am always here to help")
            self.speak('Have a Great Day ahead')

    def greetMe(self):
        self.speak(f'Hi{username}')

    def toindiantime(self):
        '''
        to convert the current 24-hour time to the 12-hour time.
        '''
        hour_now=int(datetime.datetime.now().hour)
        minute_now=int(datetime.datetime.now().minute)
        second_now=int(datetime.datetime.now().second)

        if hour_now>12:
            ind_hour=hour_now-12
            return f'{ind_hour}:{minute_now} p.m.'
        else:
            time_now=datetime.datetime.now().strftime('%H:%M')
            return f'{time_now} a.m.'
        

    def chatAI(self,query):
        
        global chatStr
        # print(chatStr)
        openai.api_key = apikey.apiKey
        chatStr += f"Snehanu: {query}\n Friday: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        try:
            self.speak(response["choices"][0]["text"])
            chatStr += f"{response['choices'][0]['text']}\n"
            return response["choices"][0]["text"]
        except Exception as e:
            with open("error.txt", "a") as f:
                f.write(str(e)+"\n")

    
#main method from where the actual working begin

if __name__=="__main__":

    Assistant=assistant()
    Assistant.online_mesg()
    while(True):#this will run when the assistant is asked to exit or has not been called
        '''
        can be killed ny calling the kill method
        and to enter into the main loop call the name of the assistant(By default it is set to Friday)
        '''
        
        on_command=Assistant.takeorderoff().lower()
        if Assistant.name in on_command:
            
            Assistant.greetMe()
            while(True):#the loop within which the main logic is present
                '''
                What it can do:
                
                1. search in Wikipedia for a topic
                2. open google.com
                3. play music from the directory (D:\music)
                4.say the current time
                5. not take an y command for some time(time is to be given in seconds)
                6. to exit say exit when the program will listen
                7. add and check the content of a todo list
                8. chat with you

                '''
                take_command=Assistant.takeOrder().lower()

                if 'exit' in take_command:
                    Assistant.speak('Thank You')
                    Assistant.wishMe()
                    break
                elif 'play music' in take_command or 'play song' in take_command or 'play a music' in take_command or 'next song' in take_command or 'play songs' in take_command :
                   
                    Assistant.speak("Do you want to change the folder(YES or NO)?")
                    while(True):
                        '''
                        changing the directory of music
                        '''
                        changepath=Assistant.takeOrder().lower()
                        if 'yes' in changepath:
                            Assistant.speak("Write the paths:")
                            
                            pathn=input("Path:")

                            with open('paths.txt', 'w') as f:
                                f.write(pathn)

                            break

                        elif 'no' in changepath:
                            break

                        else:
                            Assistant.speak('Please Say it again')
                            

                    with open('paths.txt','r') as c:
                        music_dir=c.readline()

                    song_list=os.listdir(music_dir)
                    i=0
                    list_song=[]

                    
                    while(True):
                        ''' 
                        to specify some of the details of the song to be played
                        
                        '''
                        Assistant.speak('Which song you want to play?')
                        song=Assistant.music_command().lower()
                        if '-1' not in song:
                            break
                        else:
                            Assistant.speak('Please say that again')

                    for item in song_list:
                        '''
                        to add the related songs that the user has specified
                        '''
                        if song in item.lower():

                            list_song.append(item)
                            print(f"{i} for {item}")
                            i+=1

                    isempty=True
                    decide=0


                    if len(list_song) == 0:
                        ''' 
                        to check if any song has been found or not
                        '''
                        Assistant.speak('No such songs found!')
                        Assistant.speak('Try again!')
                        isempty=False
                        
                    
                    while(isempty):
                        '''
                        selection of songs
                        '''
                        Assistant.speak('What did you choose:')

                        try:
                            decide=int(input("Enter your choice: "))
                            
                        except Exception:
                            Assistant.speak('Enter an integr value')
                            continue

                        if decide==-1 or decide >= len(list_song):
                            Assistant.speak('PLease say it again')
                            continue
                        break
                        

                    if isempty == True:
                        play_song=list_song[decide]
                        Assistant.speak("playing")
                        print("playing...")
                        os.startfile(music_dir+play_song)          
                        time.sleep(eyed3.load(os.path.join(music_dir,play_song)).info.time_secs+10)
                
                elif 'pause' in take_command:
                    delay=0
                    while(delay==0):
                        try:
                            Assistant.speak('By how much you want to delay')
                            delay=int(Assistant.takeOrder())
                            Assistant.speak(f"Program paused for {delay}")
                        except Exception as e:
                            with open(error_log, 'a') as f:
                                f.write(f'{datetime.datetime.now()}:{e}\n')
                            Assistant.speak('Please say that again')
                    time.sleep(delay)
                    Assistant.speak('Program resumed')
                
                elif 'wikipedia' in take_command or " search in wikipedia" in take_command or 'search wikipedia' in take_command:
                    Assistant.speak(f'searching in Wikipedia')
                    search_topic=take_command.replace('wikipedia ',"")
                    try:
                        result= wikipedia.summary(search_topic, sentences=2)
                        print (f"According to Wikipedia, {result}")
                        Assistant.speak(f"According to Wikipedia{result}")
                    except Exception as e:
                        with open(error_log, 'a') as f:
                            f.write(f"wikipedia summary error:{e}")
                            Assistant.speak(f" A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
                    
                    
                elif 'open google' in take_command:
                    Assistant.speak('Opening')
                    webbrowser.open('WWW.google.com')
                elif 'time' in take_command:
                    nowtime=datetime.datetime.now().strftime('%H:%M:%S')
                    print(nowtime)
                    Assistant.speak(f'The time is {nowtime}')
                elif 'open youtube' in take_command:
                    Assistant.speak('Opening')
                    webbrowser.open('WWW.youtube.com')
                    time.sleep(20)
                elif 'open todo list' in take_command or 'to do list' in take_command:                   
                    while(True):
                        Assistant.speak('Say append if  you want to add to the list or say check to check the list')
                        decide=Assistant.takeOrder().lower()          
                        if 'append' == decide:
                            while(True):
                                Assistant.speak('What you want to do')
                                do=Assistant.takeOrder()
                                Assistant.speak(f'At what time you want to  {do}') 
                                timetodo=Assistant.takeOrder()
                                if timetodo == 'None' or do =='None':
                                    Assistant.speak('sorry please say again')
                                else:
                                    break
                            with open('todo.txt' , 'a') as c:
                                c.write(f'At {timetodo} you have to {do}\n')
                            Assistant.speak('if you want to add more say to do list')
                            break
                        elif 'check' == decide:
                            Assistant.speak('Checking')
                            with open('todo.txt' , 'r') as c:
                                while(True):
                                    if c.readline() !='':
                                        Assistant.speak(c.readline())
                                    else:
                                        break
                                break
                        else:
                            Assistant.speak('sorry please say that again') 

                elif 'set a reminder' in take_command :#use a while loop for input if not recognised
                    Assistant.speak('What reminder to set:')
                    about=Assistant.takeOrder()
                    Assistant.speak('AT what time you want to {about}. Say the exact date followed by the time') 
                    rem_time=Assistant.takeOrder()
                    with open('reminder.txt' , 'a') as r:
                        r.write(f'{rem_time} ---> {about}')
                elif 'show reminders' in take_command or 'show reminder' in take_command:
                    Assistant.speak('showing')
                    os.startfile('.\\reminder.txt')
                    time.sleep(15)
                elif 'thank you' in take_command or 'thankyou' in take_command:
                    Assistant.speak(f"Your welcome{username}")
                else:
                    print("chatting")
                    Assistant.chatAI(take_command)
                   


        elif 'terminate' in on_command:
            Assistant.speak('Program terminating')
            print('terminated')
            break 
