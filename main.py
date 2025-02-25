import datetime,wikipedia,webbrowser,os,random,requests,pyautogui,playsound,subprocess,time
import urllib.request,bs4 as bs,sys,threading
import Annex,wolframalpha
from helper import takeCommand, find_and_open_app, find_and_open_document, ai_assistant
from ttkthemes import themed_tk
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk,Image
import sqlite3,pyjokes,pywhatkit
from functools import partial
import getpass,calendar
import speech_recognition as SR
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration




try:
    app=wolframalpha.Client("JPK4EE-L7KR3XWP9A")  #API key for wolframalpha
except Exception as e:
    pass

#setting chrome path
chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe %s"
recogniser= SR.Recognizer()

def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True

def CommandsList():
    '''show the command to which voice assistant is registered with'''
    os.startfile('Commands List.txt')

def clearScreen():
    ''' clear the scrollable text box'''
    SR.scrollable_text_clearing()

def greet():
    conn = sqlite3.connect('Lobox.db')
    mycursor=conn.cursor()
    hour=int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        mycursor.execute('select sentences from goodmorning')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=12 and hour<18:
        mycursor.execute('select sentences from goodafternoon')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=18 and hour<21:
        mycursor.execute('select sentences from goodevening')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    else:
        mycursor.execute('select sentences from night')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    conn.commit()
    conn.close()
    SR.speak("\nMyself Bobox Assistant. How may I help you?")

def mainframe():
    """Logic for execution task based on query"""
    SR.scrollable_text_clearing()
    greet()
    query_for_future=None
    try:
        while(True):
            query = SR.takeCommand().lower()
            query=SR.takeCommand().lower()     
            if there_exists(['search wikipedia for','from wikipedia'],query):
                SR.speak("Searching wikipedia...")
                if 'search wikipedia for' in query:
                    query=query.replace('search wikipedia for','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
                elif 'from wikipedia' in query:
                    query=query.replace('from wikipedia','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
            elif there_exists(['wikipedia'],query):
                SR.speak("Searching wikipedia....")
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #jokes
            elif there_exists(['tell me joke','tell me a joke','tell me some jokes','i would like to hear some jokes',"i'd like to hear some jokes",
                            'can you please tell me some jokes','i want to hear a joke','i want to hear some jokes','please tell me some jokes',
                            'would like to hear some jokes','tell me more jokes'],query):
                SR.speak(pyjokes.get_joke(language="en", category="all"))
                query_for_future=query
            elif there_exists(['one more','one more please','tell me more','i would like to hear more of them','once more','once again','more','again'],query) and (query_for_future is not None):
                SR.speak(pyjokes.get_joke(language="en", category="all"))

            #asking for name
            elif there_exists(["what is your name","what's your name","tell me your name",'who are you'],query):
                SR.speak("My name is Bobox Assistant and I'm here to serve you.")
            #How are you
            elif there_exists(['how are you'],query):
                conn = sqlite3.connect('Lobox.db')
                mycursor=conn.cursor()
                mycursor.execute('select sentences from howareyou')
                result=mycursor.fetchall()
                temporary_data=random.choice(result)[0]
                SR.updating_ST_No_newline(temporary_data+'😃\n')
                SR.nonPrintSpeak(temporary_data)
                conn.close()
            #what is my name
            elif there_exists(['what is my name','tell me my name',"i don't remember my name"],query):
                SR.speak("Your name is "+str(getpass.getuser()))

            #calendar
            elif there_exists(['show me calendar','display calendar'],query):
                SR.updating_ST(calendar.calendar(2021))

            #google, youtube and location
            #playing on youtube
            elif there_exists(['open youtube and play','on youtube'],query):
                if 'on youtube' in query:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('on youtube',''))
                else:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('open youtube and play ',''))
                
            elif there_exists(['play some songs on youtube','i would like to listen some music','i would like to listen some songs','play songs on youtube'],query):
                SR.speak("Opening youtube")
                pywhatkit.playonyt('play random songs')
                
            elif there_exists(['open youtube','access youtube'],query):
                SR.speak("Opening youtube")
                webbrowser.get(chrome_path).open("https://www.youtube.com")
                
            elif there_exists(['open google and search','google and search'],query):
                url='https://google.com/search?q='+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                
            #image search
            elif there_exists(['show me images of','images of','display images'],query):
                url="https://www.google.com/search?tbm=isch&q="+query[query.find('of')+3:]
                webbrowser.get(chrome_path).open(url)
                
            elif there_exists(['search for','do a little searching for','show me results for','show me result for','start searching for'],query):
                SR.speak("Searching.....")
                if 'search for' in query:
                    SR.speak(f"Showing results for {query.replace('search for','')}")
                    pywhatkit.search(query.replace('search for',''))
                elif 'do a little searching for' in query:
                    SR.speak(f"Showing results for {query.replace('do a little searching for','')}")
                    pywhatkit.search(query.replace('do a little searching for',''))
                elif 'show me results for' in query:
                    SR.speak(f"Showing results for {query.replace('show me results for','')}")
                    pywhatkit(query.replace('show me results for',''))
                elif 'start searching for' in query:
                    SR.speak(f"Showing results for {query.replace('start searching for','')}")
                    pywhatkit(query.replace('start searching for',''))
                time.sleep(2) 
                SR.speak("What else would you like me to do?")
                
            elif there_exists(['app', "up"],query):
                app_name= query[4:].strip()
                SR.speak("Searching App ")
                if not find_and_open_app(app_name):
                    SR.speak("Opening App ")
                    try:
                        subprocess.run(app_name, check=True)
                    except:
                        print("App Not found")
                        SR.speak("Application not found.")
            elif there_exists(['document'],query):
                documentName= query[9:].strip()
                SR.speak("Searching Document...")
                if not find_and_open_document(documentName):
                    SR.speak("Document Not found")
                else:
                    SR.speak("Document Opened")

            elif there_exists(['open google'],query):
                SR.speak("Opening google")
                webbrowser.get(chrome_path).open("https://www.google.com")
                time.sleep(2)  # Give a moment for browser to open
                SR.speak("What else would you like me to do?")
            elif there_exists(['find location of','show location of','find location for','show location for'],query):
                if 'of' in query:
                    url='https://google.nl/maps/place/'+query[query.find('of')+3:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    time.sleep(2)  # Give a moment for browser to open
                    SR.speak("What else would you like me to do?")
                elif 'for' in query:
                    url='https://google.nl/maps/place/'+query[query.find('for')+4:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    time.sleep(2) 
                    SR.speak("What else would you like me to do?")
            elif there_exists(["what is my exact location","What is my location","my current location","exact current location"],query):
                url = "https://www.google.com/maps/search/Where+am+I+?/"
                webbrowser.get().open(url)
                SR.speak("Showing your current location on google maps...")
                time.sleep(2) 
                SR.speak("What else would you like me to do?")
            elif there_exists(["where am i"],query):
                Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                loc = Ip_info['region']
                SR.speak(f"You must be somewhere in {loc}")

            #who is searcing mode
            elif there_exists(['who is','who the heck is','who the hell is','who is this'],query):
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=1)
                SR.speak("According to wikipdedia:  ")
                SR.speak(results)

            elif query.startswith("model"):
                user_input=query.replace("model","")
                SR.speak("Searching....")
                try:
                    results= ai_assistant(user_input)
                    SR.speak("According to Ai:  ")
                    SR.speak(results)
                except:
                    SR.speak("Sorry, I'm not able to understand it.")
              
           

            # top 5 news
            elif there_exists(['top 5 news','top five news','listen some news','news of today'],query):
                news=Annex.News(scrollable_text)
                news.show()

            #whatsapp message
            elif there_exists(['open whatsapp messeaging','send a whatsapp message','send whatsapp message','please send a whatsapp message'],query):
                whatsapp=Annex.WhatsApp(scrollable_text)
                whatsapp.send()
                del whatsapp
            #what is meant by
            elif there_exists(['what is meant by','what is mean by'],query):
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #taking photo
            elif there_exists(['take a photo','take a selfie','take my photo','take photo','take selfie','one photo please','click a photo'],query):
                takephoto=Annex.camera()
                Location=takephoto.takePhoto()
                os.startfile(Location)
                del takephoto
                SR.speak("Captured picture is stored in Camera folder.")

            #bluetooth file sharing
            elif there_exists(['send some files through bluetooth','send file through bluetooth','bluetooth sharing','bluetooth file sharing','open bluetooth'],query):
                SR.speak("Opening bluetooth...")
                os.startfile(r"C:\Windows\System32\fsquirt.exe")

            #play game
            elif there_exists(['would like to play some games','play some games','would like to play some game','want to play some games','want to play game','want to play games','play games','open games','play game','open game'],query):
                SR.speak("We have 2 games right now.\n")
                SR.updating_ST_No_newline('1.')
                SR.speak("Stone Paper Scissor")
                SR.updating_ST_No_newline('2.')
                SR.speak("Snake")
                SR.speak("\nTell us your choice:")
                while(True):
                    query=SR.takeCommand().lower()
                    if ('stone' in query) or ('paper' in query):
                        SR.speak("Opening stone paper scissor...")
                        sps=Annex.StonePaperScissor()
                        sps.start(scrollable_text)
                    elif ('snake' in query):
                        SR.speak("Opening snake game...")
                        import Snake
                        Snake.start()
                        break
                    else:
                        SR.speak("It did not match the option that we have. \nPlease say it again.")

            #makig note
            elif there_exists(['make a note','take note','take a note','note it down','make note','remember this as note','open notepad and write'],query):
                SR.speak("What would you like to write down?")
                data=SR.takeCommand()
                n=Annex.note()
                n.Note(data)
                SR.speak("I have a made a note of that.")

            #flipping coin
            elif there_exists(["toss a coin","flip a coin","toss"],query):
                moves=["head", "tails"]
                cmove=random.choice(moves)
                playsound.playsound('quarter spin flac.mp3')
                SR.speak("It's " + cmove)

            #time and date
            elif there_exists(['the time'],query):
                strTime =datetime.datetime.now().strftime("%H:%M:%S")
                strDay=datetime.date.today().strftime("%B %d, %Y")
                SR.speak(f"Sir, the time is {strTime}\nThe date is {strDay}")
            elif there_exists(['the date'],query):
                strDay=datetime.date.today().strftime("%B %d, %Y")
                SR.speak(f"Today is {strDay}")
            elif there_exists(['what day it is','what day is today','which day is today',"today's day name please"],query):
                SR.speak(f"Today is {datetime.datetime.now().strftime('%A')}")

            #opening software applications
            elif there_exists(['open chrome'],query):
                SR.speak("Opening chrome")
                os.startfile(r'C:\Program Files \Google\Chrome\Application\chrome.exe')
            elif there_exists(['open notepad plus plus','open notepad++','open notepad ++'],query):
                SR.speak('Opening notepad++')
                os.startfile(r'C:\Program Files\Notepad++\notepad++.exe')
            elif there_exists(['open notepad','start notepad'],query):
                SR.speak('Opening notepad')
                os.startfile(r'C:\Windows\notepad.exe')
                
            elif there_exists(['open ms paint','open mspaint','open microsoft paint','start microsoft paint','start ms paint'],query):
                SR.speak("Opening Microsoft paint....")
                os.startfile('C:\Windows\System32\mspaint.exe')
            elif there_exists(['show me performance of my system','open performance monitor','performance monitor','performance of my computer','performance of this computer'],query):
                os.startfile("C:\Windows\System32\perfmon.exe")
            elif there_exists(['open snipping tool','snipping tool','start snipping tool'],query):
                SR.speak("Opening snipping tool....")
                os.startfile("C:\Windows\System32\SnippingTool.exe")
                
            elif there_exists(['open code','open visual studio ','open vs code'],query):
                SR.speak("Opeining vs code")
                codepath=r"C:\Users\Christian\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                os.startfile(codepath)
            elif there_exists(['open file manager','file manager','open my computer','my computer','open file explorer','file explorer','open this pc','this pc'],query):
                SR.speak("Opening File Explorer")
                os.startfile("C:\Windows\explorer.exe")
            elif there_exists(['powershell'],query):
                SR.speak("Opening powershell")
                os.startfile(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe')
            elif there_exists(['cmd','command prompt','command prom','commandpromt',],query):
                SR.speak("Opening command prompt")
                os.startfile(r'C:\Windows\System32\cmd.exe')
            elif there_exists(['open whatsapp'],query):
                SR.speak("Opening whatsApp")
                os.startfile(r'C:\Users\Christian\AppData\Local\WhatsApp\WhatsApp.exe')
                
            elif there_exists(['open settings','open control panel','open this computer setting Window','open computer setting Window'   ,'open computer settings','open setting','show me settings','open my computer settings'],query):
                SR.speak("Opening settings...")
                os.startfile('C:\Windows\System32\control.exe')
            elif there_exists(['open your setting','open your settings','open settiing window','show me setting window','open voice assistant settings'],query):
                SR.speak("Opening my Setting window..")
                sett_wind=Annex.SettingWindow()
                sett_wind.settingWindow(root)
            elif there_exists(['open vlc','vlc media player','vlc player'],query):
                SR.speak("Opening VLC media player")
                os.startfile(r"C:\Program Files\VideoLAN\VLC\vlc.exe")

            #password generator
            elif there_exists(['suggest me a password','password suggestion','i want a password'],query):
                m3=Annex.PasswordGenerator()
                m3.givePSWD(scrollable_text)
                del m3
            #screeshot
            elif there_exists(['take screenshot','take a screenshot','screenshot please','capture my screen', 'a screenshot' , "screenshot"],query):
                SR.speak("Taking screenshot")
                SS=Annex.screenshot()
                SS.takeSS()
                SR.speak('Captured screenshot is saved in Screenshots folder.')
                del SS
                SR.speak("What's would you like to do next?")

            #voice recorder
            elif there_exists(['record my voice','start voice recorder','voice recorder'],query):
                VR=Annex.VoiceRecorer()
                VR.Record(scrollable_text)
                del VR

            #text to speech conversion
            elif there_exists(['text to speech','convert my notes to voice'],query):
                SR.speak("Opening Text to Speech mode")
                TS=Annex.TextSpeech()
                del TS

            #weather report
            elif there_exists(['weather report','temperature'],query):
                Weather=Annex.Weather()
                Weather.show(scrollable_text)

            #shutting down system
            elif there_exists(['exit','quit','shutdown','shut up','goodbye','shut down'],query):
                SR.speak("shutting down")
                sys.exit()

            elif there_exists(['none'],query):
                pass
            elif there_exists(['stop the flow','stop the execution','halt','halt the process','stop the process','stop listening','stop the listening'],query):
                SR.speak("Listening halted.")
                break
            #it will give online results for the query
            elif there_exists(['search something for me','to do a little search','search mode','i want to search something'],query):
                SR.speak('What you want me to search for?')
                query=SR.takeCommand()
                SR.speak(f"Showing results for {query}")
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

            #what is the capital
            elif there_exists(['what is the capital of','capital of','capital city of'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

            elif there_exists(['temperature'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    SR.speak("Internet Connection Error, Please check your internet connection.")
            elif there_exists(['+','-','*','x','/','plus','add','minus','subtract','divide','multiply','divided','multiplied'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    SR.speak("Internet Connection Error, Please check your internet connection.")


            else:
                SR.speak("Sorry it did not match with any commands that i'm registered with. Please say it again.")
    except Exception as e:
        pass

def gen(n):
    for i in range(n):
        yield i

class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        mainframe()

def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()
if __name__=="__main__":
    #tkinter code
    root = themed_tk.ThemedTk()
    root.set_theme("clam")
    
    # Set window size and center it on screen
    width, height = 800, 500
    x = int(root.winfo_screenwidth()/2 - width/2)
    y = int(root.winfo_screenheight()/2 - height/2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    # Make the window resizable
    root.resizable(1, 1)  # Changed from 0, 0 to 1, 1
    root.title("Bobox Assistant")
    root.iconbitmap('Lobox.ico')
    
    # Modern color scheme - blue theme
    colors = {
        'primary': '#1a5276',      # Dark blue for main background
        'secondary': '#2980b9',    # Medium blue for accents
        'highlight': '#3498db',    # Bright blue for highlights/hover
        'text_area_bg': '#ecf0f1', # Light gray-blue for text area
        'text': '#2c3e50',         # Dark blue-gray for text
        'white': '#ffffff',        # White for contrast text
        'button_hover': '#2471a3'  # Darker blue for button hover
    }
    
    root.configure(bg=colors['primary'])
    
    # Top menu bar
    myMenu = tk.Menu(root, bg=colors['text_area_bg'], fg=colors['text'])
    m1 = tk.Menu(myMenu, tearoff=0, bg=colors['text_area_bg'], fg=colors['text'])
    m1.add_command(label='Commands List', command=CommandsList)
    myMenu.add_cascade(label="Help", menu=m1)
    
    stng_win = Annex.SettingWindow()
    myMenu.add_cascade(label="Settings", command=partial(stng_win.settingWindow, root))
    myMenu.add_cascade(label="Clear Screen", command=clearScreen)
    root.config(menu=myMenu)
    
    # Make all frames expandable with window resizing
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    # Header with title and status (using grid instead of pack)
    header_frame = tk.Frame(root, bg=colors['primary'], height=50)
    header_frame.grid(row=0, column=0, sticky='ew')
    header_frame.grid_columnconfigure(1, weight=1)  # Make middle column expandable
    
    # Title text
    title_label = tk.Label(header_frame, text="BOBOX ASSISTANT", 
                           font=('Segoe UI', 18, 'bold'), 
                           fg=colors['white'], bg=colors['primary'])
    title_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    
    # Empty expandable middle frame
    middle_frame = tk.Frame(header_frame, bg=colors['primary'])
    middle_frame.grid(row=0, column=1, sticky='ew')
    
    # Status indicator (right aligned)
    status_frame = tk.Frame(header_frame, bg=colors['primary'])
    status_frame.grid(row=0, column=2, padx=20, pady=10, sticky='e')
    
    status_indicator = tk.Canvas(status_frame, width=15, height=15, bg=colors['primary'], 
                                highlightthickness=0)
    status_indicator.create_oval(2, 2, 13, 13, fill='#95a5a6', outline='')  # Gray when not active
    status_indicator.pack(side='left', padx=(0, 5))
    
    status_text = tk.Label(status_frame, text="Idle", font=('Segoe UI', 10),
                          fg=colors['white'], bg=colors['primary'])
    status_text.pack(side='left')
    
    # Main content area
    content_frame = tk.Frame(root, bg=colors['primary'])
    content_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 20))
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)
    
    # Text display area with custom styling
    text_frame = tk.Frame(content_frame, bg=colors['secondary'], padx=2, pady=2)
    text_frame.grid(row=0, column=0, sticky='nsew')
    text_frame.grid_columnconfigure(0, weight=1)
    text_frame.grid_rowconfigure(0, weight=1)
    
    scrollable_text = scrolledtext.ScrolledText(
        text_frame,
        state='disabled',
        wrap=tk.WORD,
        font=('Segoe UI', 11),
        bg=colors['text_area_bg'],
        fg=colors['text'],
        padx=10,
        pady=10,
        relief='flat'
    )
    scrollable_text.grid(row=0, column=0, sticky='nsew')
    
    # Bottom control bar
    control_frame = tk.Frame(root, bg=colors['primary'], height=70)
    control_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
    control_frame.grid_columnconfigure(1, weight=1)  # Middle column expands
    
    # Function to change button color on hover
    def on_enter(e):
        e.widget['bg'] = colors['button_hover']
        
    def on_leave(e):
        if e.widget == mic_button:
            e.widget['bg'] = colors['secondary']
        else:
            e.widget['bg'] = colors['secondary']
    
    # Left side with mic button and speak label
    mic_frame = tk.Frame(control_frame, bg=colors['primary'])
    mic_frame.grid(row=0, column=0, sticky='w')
    
    # Speak label
    speak_label = tk.Label(mic_frame, text="SPEAK:", 
                          font=('Segoe UI', 13, 'bold'),
                          fg=colors['white'], bg=colors['primary'])
    speak_label.pack(side='left', padx=(0, 15))
    
    # Ensure mic button is displayed by using try-except to handle image loading
    try:
        mic_img = Image.open("Mic.png")
        mic_img = mic_img.resize((60, 60), Image.Resampling.LANCZOS)
        mic_img = ImageTk.PhotoImage(mic_img)
        
        # Create a visible button frame with a distinctive background
        mic_button_frame = tk.Frame(mic_frame, bg=colors['highlight'], padx=3, pady=3)
        mic_button_frame.pack(side='left')
        
        mic_button = tk.Button(
            mic_button_frame,
            image=mic_img,
            bg=colors['secondary'],
            activebackground=colors['highlight'],
            relief='flat',
            borderwidth=0,
            command=Launching_thread
        )
        mic_button.image = mic_img  # Keep a reference to prevent garbage collection
        mic_button.pack()
    except Exception as e:
        # Fallback if image can't be loaded
        print(f"Error loading mic image: {e}")
        mic_button = tk.Button(
            mic_frame,
            text="🎤",  # Microphone emoji as fallback
            font=('Segoe UI', 24),
            bg=colors['secondary'],
            fg=colors['white'],
            activebackground=colors['highlight'],
            activeforeground=colors['white'],
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=10,
            command=Launching_thread
        )
        mic_button.pack(side='left')
    
    mic_button.bind("<Enter>", on_enter)
    mic_button.bind("<Leave>", on_leave)
    
    # Middle spacer that will expand
    middle_spacer = tk.Frame(control_frame, bg=colors['primary'])
    middle_spacer.grid(row=0, column=1, sticky='ew')
    
    # Right-aligned buttons
    button_bar = tk.Frame(control_frame, bg=colors['primary'])
    button_bar.grid(row=0, column=2, sticky='e')
    
    # Button style
    button_style = {
        'font': ('Segoe UI', 10),
        'bg': colors['secondary'],
        'fg': colors['white'],
        'activebackground': colors['highlight'],
        'activeforeground': colors['white'],
        'relief': 'flat',
        'borderwidth': 0,
        'padx': 15,
        'pady': 8
    }
    
    # Clear screen button
    clear_btn = tk.Button(button_bar, text="Clear Screen", command=clearScreen, **button_style)
    clear_btn.pack(side='left', padx=5)
    clear_btn.bind("<Enter>", on_enter)
    clear_btn.bind("<Leave>", on_leave)
    
    # Settings button
    settings_btn = tk.Button(
        button_bar, 
        text="Settings", 
        command=lambda: stng_win.settingWindow(root), 
        **button_style
    )
    settings_btn.pack(side='left', padx=5)
    settings_btn.bind("<Enter>", on_enter)
    settings_btn.bind("<Leave>", on_leave)
    
    # Help button
    help_btn = tk.Button(button_bar, text="Commands List", command=CommandsList, **button_style)
    help_btn.pack(side='left', padx=5)
    help_btn.bind("<Enter>", on_enter)
    help_btn.bind("<Leave>", on_leave)
    
    # Setting up objects
    SR = Annex.SpeakRecog(scrollable_text)
    
    def update_status(is_listening=False):
        if is_listening:
            status_indicator.itemconfig(1, fill='#2ecc71')  # Green
            status_text.config(text="Listening...")
        else:
            status_indicator.itemconfig(1, fill='#95a5a6')  # Gray
            status_text.config(text="Idle")
    
    # Handle window resize events
    def on_resize(event):
        # Update any elements that need to adjust with window size
        pass  # Add specific resize handling if needed
        
    root.bind("<Configure>", on_resize)
    
    root.mainloop()