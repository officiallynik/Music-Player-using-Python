from tkinter import *
from pygame import mixer as mixer
from tkinter import messagebox, filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import time
import threading
import os
from mutagen.mp3 import MP3

root = ThemedTk(theme="arc")
root.geometry('540x350')
root.title("Symphony")
root.iconbitmap("lib/music-img.ico")

def browse():
    global filename
    filename = filedialog.askopenfilename()
    add_to_playlist(filename)

playlist = []
index = 0
def add_to_playlist(filename):
    if(len(filename)>0):
        global index
        playlist.append(filename)
        songs.insert(index, os.path.basename(filename))
        index+=1

def remove():
    playlist.pop(songs.curselection()[0])
    songs.delete(songs.curselection()[0])

menubar = Menu(root)
root.config(menu=menubar)
submenu1 = Menu(menubar, tearoff=0)
submenu2 = Menu(menubar, tearoff=0)

menubar.add_cascade(label='File', menu=submenu1)
submenu1.add_command(label='Open File...', command=browse)

menubar.add_cascade(label='Help', menu=submenu2)
submenu2.add_command(label='About', command=lambda: messagebox.showinfo('Symphony', 'Music player designed using python and its frameworks by NIKHIL'))

pause = PhotoImage(file="lib/pause.png")
play = PhotoImage(file="lib/play-button.png")
rewind = PhotoImage(file="lib/rewind-button.png")
stop = PhotoImage(file="lib/stop-button.png")
mutevol = PhotoImage(file="lib/mute.png")
unmute = PhotoImage(file="lib/speaker.png")

mixer.init()
global paused
paused = 0

def details():
    if(songs.curselection()):
        num = songs.curselection()[0]
    else:
        num = playnum
    inf = MP3(playlist[num])
    tim = int(inf.info.length)
    # progressText['text'] = '{:02d}:{:02d}/{:02d}:{:02d}'.format(0, 0, time//60, time%60)
    # progress['value']=50
    t = threading.Thread(target=showprogress, args=(abs(tim),))
    t.start()

playnum=0
def showprogress(t):
    global paused
    global playnum
    x=0
    while x<=t and mixer.music.get_busy():
        if paused==1:
            continue
        else:
            progressText['text'] = '{:02d}:{:02d}/{:02d}:{:02d}'.format(x//60, x%60, t//60, t%60)
            progress['value']=(x/t)*100
            time.sleep(1)
            x+=1
    time.sleep(2.5)
    if x==t+1 and playnum+1<len(playlist):
        stopMusic()
        progress['value']=0
        x=0
        playnum+=1
        playMusic()


            
def playMusic():
    global playnum
    global paused
    if paused==1:
        mixer.music.unpause()
        paused = 0
        statusBar['text']="Playing " + os.path.basename(filename)
        ppBtn['image']=pause
        ppBtn['command']=pauseMusic
    else:
        try:
            if(songs.curselection()):
                num = songs.curselection()[0]
            else:
                num = playnum
            mixer.music.load(playlist[num])
            text['text'] = ((os.path.basename(playlist[num])).split("."))[0].upper()
            mixer.music.play()
            details()
            statusBar['text']="Playing " + os.path.basename(playlist[num])   
            ppBtn['image']=pause
            ppBtn['command']=pauseMusic
        except:
            messagebox.showwarning('file load error', 'There is no file to be played. Please load a file first.')
            statusBar['text']='Please selete a file to play'
            browse()
        

def stopMusic():
    mixer.music.stop()
    ppBtn['image']=play
    ppBtn['command']=playMusic
    statusBar['text']='Music Stopped'

def pauseMusic():
    global paused
    paused = 1
    mixer.music.pause()
    ppBtn['image']=play
    ppBtn['command']=playMusic
    statusBar['text']="Music Paused"

def repeatMusic():
    stopMusic()
    time.sleep(1)
    playMusic()

mute = False
def volume(val):
    global vol
    global mute
    vol = float(val)/100
    mixer.music.set_volume(vol)
    if vol>0:
        muteBtn['image'] = unmute
        mute = False
    else:
        muteBtn['image'] = mutevol
        mute = True

def muteMusic():
    global mute
    if mute:
        muteBtn['image']=unmute
        scale.set(60)
        mixer.music.set_volume(.6)
        mute = False
    else:
        muteBtn['image']=mutevol
        scale.set(0)
        mixer.music.set_volume(0)
        mute = True

text = ttk.Label(root, text='PLAY AWESOME, LIVE AWESOME')
text.pack(pady=10)

statusBar = Label(root, text="Symphony Music Player", bg='#38dff5', anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

buttonFrame = Frame(root)
buttonFrame.pack(pady=10, side=BOTTOM)

rewindBtn = Button(buttonFrame, image=rewind, command=repeatMusic, bd=0)
rewindBtn.grid(row=1, column=0, padx=(5, 7))

ppBtn = Button(buttonFrame, image=play, command=playMusic, bd=0)
ppBtn.grid(row=1, column=1, padx=(1, 7))

stopBtn = Button(buttonFrame, image=stop, command=stopMusic, bd=0)
stopBtn.grid(row=1, column=2, padx=(1, 3))

muteBtn = Button(buttonFrame, image=mutevol, command=muteMusic, bd=0)
muteBtn.grid(row=1, column=3, padx=(25,5))

scale = ttk.Scale(buttonFrame, from_=0, to=100, orient=HORIZONTAL, command=volume)
scale.set(60)
mixer.music.set_volume(.6)
scale.grid(row=1, column=4, pady=(2,0))

detailFrame = Frame(root)
detailFrame.pack(side=BOTTOM, pady=3)

progress = ttk.Progressbar(detailFrame, orient = HORIZONTAL, length=450, mode = 'determinate')
progress.grid(row=0, column=0)

progressText = Label(detailFrame, text="00:00/00:00")
progressText.grid(row=0, column=1, padx=7, pady=1)

addFrame = Frame(root)
addFrame.pack(side=BOTTOM, pady=3)
add = ttk.Button(addFrame, text='ADD', command=browse)
add.grid(row=0, column=0, padx=2)
delt = ttk.Button(addFrame, text='DELETE', command=remove)
delt.grid(row=0, column=1, padx=2)
songs = Listbox(root, bd=1, bg='#aaff9c', width=40)
songs.pack(side=BOTTOM, pady=(0,8))

def close():
    stopMusic()
    root.destroy()
submenu1.add_command(label='Exit', command=close)

root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()