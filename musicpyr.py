from tkinter import *
from pygame import mixer as mixer
from tkinter import messagebox, filedialog
import os
from mutagen import mp3

root = Tk()
root.geometry('540x320')
root.title("Symphony")
root.iconbitmap("lib/music-img.ico")

def browse():
    global filename
    filename = filedialog.askopenfilename()

menubar = Menu(root)
root.config(menu=menubar)
submenu1 = Menu(menubar, tearoff=0)
submenu2 = Menu(menubar, tearoff=0)

menubar.add_cascade(label='File', menu=submenu1)
submenu1.add_command(label='Open File...', command=browse)
submenu1.add_command(label='Exit', command=lambda: root.destroy())

menubar.add_cascade(label='Help', menu=submenu2)
submenu2.add_command(label='About', command=lambda: messagebox.showinfo('Symphony', 'Music player designed using python and its frameworks'))

pause = PhotoImage(file="lib/pause.png")
play = PhotoImage(file="lib/play-button.png")
rewind = PhotoImage(file="lib/rewind-button.png")
stop = PhotoImage(file="lib/stop-button.png")
mutevol = PhotoImage(file="lib/mute.png")
unmute = PhotoImage(file="lib/speaker.png")

mixer.init()
global paused
paused = 0


def playMusic():
    global paused
    if paused==1:
        mixer.music.unpause()
        paused = 0
        statusBar['text']="Playing " + os.path.basename(filename)
        ppBtn['image']=pause
        ppBtn['command']=pauseMusic
    else:
        try:
            mixer.music.load(filename)
            text['text'] = ((os.path.basename(filename)).split("."))[0].upper()
            mixer.music.play()
            statusBar['text']="Playing " + os.path.basename(filename)   
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
mute = False
def volume(val):
    global vol
    global mute
    vol = int(val)/100
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

text = Label(root, text="Music is Life")
text.pack(pady=10)

statusBar = Label(root, text="Symphony Music Player", relief=SUNKEN, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

buttonFrame = Frame(root)
buttonFrame.pack(pady=10, side=BOTTOM)

rewindBtn = Button(buttonFrame, image=rewind, command=playMusic, bd=0)
rewindBtn.grid(row=0, column=0, padx=(5, 7))

ppBtn = Button(buttonFrame, image=play, command=playMusic, bd=0)
ppBtn.grid(row=0, column=1, padx=(1, 7))

stopBtn = Button(buttonFrame, image=stop, command=stopMusic, bd=0)
stopBtn.grid(row=0, column=2, padx=(1, 3))

muteBtn = Button(buttonFrame, image=mutevol, command=muteMusic, bd=0)
muteBtn.grid(row=0, column=3, padx=(25,5))

scale = Scale(buttonFrame, from_=0, to=100, orient=HORIZONTAL, showvalue=0, command=volume)
scale.set(60)
mixer.music.set_volume(.6)
scale.grid(row=0, column=4, pady=(2,0))


root.mainloop()