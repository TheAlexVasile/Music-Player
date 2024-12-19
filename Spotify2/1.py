import pygame
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import random
import numpy as np

from numpy.random import shuffle


class Spotify2:
    def __init__(self,root):
        self.root=root#atribuie parametrul root variabilei self.root si permite modificarea ferestrei root
        self.root.title("Spotify 2") #titlul ferestrei
        self.root.geometry("1060x355") #dimensiunea ferestrei
        self.root.configure(bg="#3c468c")
        self.root.resizable(False,False) #fereastra nu poate fi redimensionata nici pe orizontala, nici pe verticala

        s=ttk.Style()
        s.theme_use('clam')
        s.configure('.',background='#140f32',foreground='#d8e1f0')#. - stil standard
        s.configure('Tframe',background='#140f32',foreground='#140f32')#modifica aspectul cadrului
        s.configure('TButton',font=('Calibri',12),background='#140f32',foreground='#d8e1f0',activebackground='#3c468c',activeforeground='#3c468c')#aspectul butoanelor
        s.configure('Tlabel',font=('Calibri',12),background='#d8e1f0',foreground='#d8e1f0')#aspectul etichetelor
        s.configure('TScale',background='white')#aspectul sliderului

        pygame.init()
        pygame.mixer.init()

        self.playlist_frame=tk.Frame(self.root)#creaza cadrul playlistului (din stanga)
        self.playlist_frame.grid(row=0,column=0,padx=10,pady=10)
        self.playlist=tk.Listbox(self.playlist_frame,width=80,height=20) #chenarul din stanga
        self.playlist.configure(bg="#d8e1f0")
        self.playlist.pack(fill=tk.BOTH,expand=True)#chenarul se extinde si pe verticala si pe orizontala
        self.playlist.bind("<<ListboxSelect>>",self.play_selected)
        #cadrul principal
        self.control_frame=ttk.Frame(self.root)
        self.control_frame.grid(row=0,column=1,padx=10,pady=10)
        self.control_frame.configure(border=1,relief="groove",borderwidth=6,height=80)
        #cadru 2 - pentru afisarea melodiei curente
        self.control_frame2=ttk.Frame(self.control_frame)
        self.control_frame2.grid(row=0,column=0,padx=10,pady=0)
        self.control_frame2.configure(border=1,borderwidth=1)
        #cadru 3 - pentru butoane
        self.control_frame3=ttk.Frame(self.control_frame)
        self.control_frame3.grid(row=1,column=0,padx=10,pady=10)
        self.control_frame3.configure(border=1,borderwidth=1)
        #cadru 4 - pentru audio
        self.control_frame4=ttk.Frame(self.control_frame)
        self.control_frame4.grid(row=2,column=0,padx=10,pady=10)
        self.control_frame4.configure(border=1,borderwidth=1)
        #cadru 5 - pentru progress bar
        self.control_frame5=ttk.Frame(self.control_frame)
        self.control_frame5.grid(row=3,column=0,padx=10,pady=10)
        self.control_frame5.configure(border=1,borderwidth=1)
        #cadru 6 - pentru butonul de selectat melodii
        self.control_frame6=ttk.Frame(self.control_frame)
        self.control_frame6.grid(row=4,column=0,padx=10,pady=10)
        self.control_frame6.configure(border=1,borderwidth=1)
        #buton start-stop
        self.play_var=tk.StringVar()
        self.play_var.set("|>")
        self.start_stop_button=ttk.Button(self.control_frame3,textvariable=self.play_var,command=self.start_stop,width=4)
        self.start_stop_button.grid(row=1,column=2,padx=10,pady=10)
        #buton melodia anterioara
        self.skip_backward_button=ttk.Button(self.control_frame3,text="<<",command=self.skip_backward,width=4)
        self.skip_backward_button.grid(row=1,column=0,padx=10,pady=10)
        #buton melodia urmatoare
        self.skip_forward_button=ttk.Button(self.control_frame3,text=">>",command=self.skip_forward,width=4)
        self.skip_forward_button.grid(row=1,column=5,padx=10,pady=10)
        #buton +5 secunde
        self.advance_button=ttk.Button(self.control_frame3,text="+5",width=4,command=self.advance)
        self.advance_button.grid(row=1,column=4,padx=10,pady=10)
        #buton -5 secunde
        self.reverse_button=ttk.Button(self.control_frame3,text="-5",width=4,command=self.reverse)
        self.reverse_button.grid(row=1,column=1,padx=10,pady=10)
        #eticheta cu melodia curenta
        self.status_var=tk.StringVar()
        self.status_var.set("")
        self.status_label=ttk.Label(self.control_frame2,textvariable=self.status_var)
        self.status_label.grid(row=0,column=0,padx=10,pady=10)
        self.status_label.configure(font=("Calibri",16))
        #slider volum
        self.volume_var=tk.DoubleVar()
        self.volume_scale=ttk.Scale(self.control_frame4,orient="horizontal",from_=0,to=1,variable=self.volume_var,command=self.set_volume)
        self.volume_scale.grid(row=0,column=1,padx=10,pady=10)
        #shuffle
        self.shufflevar=tk.IntVar() #variabila atribuita unui buton, cu un parametru numar intreg
        self.shuffle=tk.Checkbutton(self.control_frame4,text='Shuffle',variable=self.shufflevar,onvalue=1,offvalue=0,background='#140f32',fg='#3c468c',activebackground='#140f32')
        self.shuffle.grid(row=0,column=0)
        #loop
        self.loopvar=tk.IntVar()
        self.loop=tk.Checkbutton(self.control_frame4,text='Loop',variable=self.loopvar,onvalue=1,offvalue=0,background='#140f32',fg='#3c468c',activebackground='#140f32')
        self.loop.grid(row=0,column=2)
        ##buton de ales melodiile
        self.import_button=ttk.Button(self.control_frame6,text="Alege melodiile",command=self.import_music)
        self.import_button.grid(row=0,column=0,padx=10,pady=10)
        #bara progres
        self.progress_bar=ttk.Progressbar(self.control_frame5,orient="horizontal",length=400,mode="determinate") #determinate inseamna ca indica progresul
        self.progress_bar.grid(row=0,column=1,padx=0,pady=10)
        #eticheta cu timpul trecut
        self.present_time=ttk.Label(self.control_frame5,text="00:00")
        self.present_time.grid(row=0,column=0,padx=10,pady=10)
        #eticheta cu durata melodiei
        self.total_time=ttk.Label(self.control_frame5,text="00:00")
        self.total_time.grid(row=0,column=2,padx=10,pady=10)
        #melodia curenta
        self.current_song=""

        self.paused=False
        self.cumulative_time=0 #variabila saltul cu 5 secunde - fara ea, saltul merge doar odata, apoi se reseteaza timpul
        #variabila a constructorului care retine lungimea melodiei, pentru a trece la urmatoarea melodie cand cea curenta s-a sfarsit.
        self.song_length_g=0

#functie pentru selectie
    def play_selected(self,event):
        #print(event)
        self.cumulative_time=0
        selected_song=self.playlist.get(self.playlist.curselection())
        self.current_song=selected_song
        pygame.mixer.music.load(self.current_song)
        name,ext=os.path.splitext(self.current_song) #afla locatia + numele si extensia melodiei
        index=name.rfind('/') #afla ultima pozitie a caracterului /
        name=name[(index+1):] #elimina caracterele pana la ultimul '/'
        self.status_var.set(name)
        self.progress_bar["maximum"]=pygame.mixer.Sound(self.current_song).get_length()
        self.song_length_g=pygame.mixer.Sound(self.current_song).get_length()
        #print(self.song_length_g)
        self.update_progressbar()
        songlength=pygame.mixer.Sound(self.current_song).get_length()#aflam durata melodiei si o afisam la dreapta de progress bar
        minutes,seconds=divmod(int(songlength),60)
        self.total_time.config(text="{:02d}:{:02d}".format(minutes,seconds))
        pygame.mixer.music.play()
        self.play_var.set("||")
#functie pentru inceput de la un anumit timp
    #def play_new_time(self,new):

#functie pentru butonul start stop
    def start_stop(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused=False
            self.play_var.set("||")
        else:
            pygame.mixer.music.pause()
            self.paused=True
            self.play_var.set("|>")
#functie pentru melodia anterioara
    def skip_backward(self):
        selection=self.playlist.curselection()
        self.playlist.curselection()
        if selection:
            prev_song_nr=int(selection[0])-1
            if prev_song_nr >=0:
                self.cumulative_time=0
                self.progress_bar["value"]=0
                prev_song=self.playlist.get(prev_song_nr)
                self.playlist.selection_clear(0,tk.END) #curata si actualizeaza selectia
                self.playlist.selection_set(prev_song_nr)
                self.playlist.activate(prev_song_nr)
                self.current_song=prev_song
                pygame.mixer.music.load(self.current_song)
                name, ext = os.path.splitext(self.current_song)  # afla locatia + numele si extensia melodiei
                index = name.rfind('/')  # afla ultima pozitie a caracterului /
                name = name[(index + 1):]  # elimina caracterele pana la ultimul '/'
                self.status_var.set(name)
                songlength=pygame.mixer.Sound(self.current_song).get_length()#aflam durata melodiei si o afisam la dreapta de progress bar
                minutes,seconds=divmod(int(songlength),60)
                self.total_time.config(text="{:02d}:{:02d}".format(minutes,seconds))
                pygame.mixer.music.play()
                self.progress_bar["maximum"]=pygame.mixer.Sound(self.current_song).get_length()
                if self.paused:
                    self.start_stop()
            else:
                messagebox.showwarning("Eroare","Este prima melodie.")
        else:
            messagebox.showerror("Eroare","Nu e selectata nicio melodie.")

    #functie pentru butonul de sarit la melodia urmatoare
    def skip_forward(self):
        self.cumulative_time=0
        selection=self.playlist.curselection()
        if selection:
            next_song_nr=int(selection[0])+1
            if next_song_nr <self.playlist.size():
                self.cumulative_time=0
                self.progress_bar["value"]=0
                next_song=self.playlist.get(next_song_nr)
                self.playlist.selection_clear(0,tk.END) #curata si actualizeaza selectia
                self.playlist.selection_set(next_song_nr)
                self.playlist.activate(next_song_nr)
                self.current_song=next_song
                pygame.mixer.music.load(self.current_song)
                name, ext = os.path.splitext(self.current_song)  # afla locatia + numele si extensia melodiei
                index = name.rfind('/')  # afla ultima pozitie a caracterului /
                name = name[(index + 1):]  # elimina caracterele pana la ultimul '/'
                self.status_var.set(name)
                self.song_length_g = pygame.mixer.Sound(self.current_song).get_length()
                songlength=pygame.mixer.Sound(self.current_song).get_length()#aflam durata melodiei si o afisam la dreapta de progress bar
                #print(songlength)
                minutes,seconds=divmod(int(songlength),60)
                self.total_time.config(text="{:02d}:{:02d}".format(minutes,seconds))
                pygame.mixer.music.play()
                self.progress_bar["maximum"]=pygame.mixer.Sound(self.current_song).get_length()
                if self.paused:
                    self.start_stop()
            else:
                messagebox.showwarning("Eroare","Este ultima melodie.")
        else:
            messagebox.showerror("Eroare","Nu e selectata nicio melodie.")
#functie pentru sliderul de volum
    def set_volume(self,val):
        volume=float(val)
        pygame.mixer.music.set_volume(volume)
#functie pentru selectat melodiile
    def import_music(self):
        file_paths=filedialog.askopenfilenames(
            title="Alege melodiile",
            filetypes=[("Audio Files", "*.mp3")]
        )
        for file_path in file_paths:
            if file_path not in self.playlist.get(0,tk.END):
                self.playlist.insert(tk.END,file_path)
#functie pentru trecut la urmatoarea melodie pe shuffle
    def shuffle_songs(self):
        selection = self.playlist.curselection()
        playlistlen=self.playlist.size()
        if playlistlen==1:
            pass
        else:
            current_song_index=int(selection[0])
            indexlist=np.arange(0,playlistlen,1)
            shuffled_song_index=current_song_index
            while shuffled_song_index==current_song_index:
                shuffled_song_index=random.choice(indexlist)
            #print(shuffled_song_index)
            self.cumulative_time=0
            self.progress_bar["value"]=0
            shuffled_song=self.playlist.get(shuffled_song_index)
            self.playlist.selection_clear(0,tk.END)
            self.playlist.selection_set(shuffled_song_index)
            self.playlist.activate(shuffled_song_index)
            self.current_song=shuffled_song
            pygame.mixer.music.load(self.current_song)
            name,ext=os.path.splitext(self.current_song)
            index=name.rfind('/')
            name=name[(index+1):]
            self.status_var.set(name)
            self.song_length_g=pygame.mixer.Sound(self.current_song).get_length()
            minutes,seconds=divmod(int(self.song_length_g),60)
            self.total_time.config(text="{:02d}:{:02d}".format(minutes,seconds))
            pygame.mixer.music.play()
            self.progress_bar["maximum"]=self.song_length_g

#functie pentru avansat cu 5 secunde
    def advance(self):
        if pygame.mixer.music.get_busy():
            #playlistlen=self.playlist.size
            current_offset=pygame.mixer.music.get_pos()/1000
            self.cumulative_time+=current_offset
            self.cumulative_time+=5
            if(self.cumulative_time+0.1>=pygame.mixer.Sound(self.current_song).get_length()):
                if self.loopvar.get()==1:
                    pygame.mixer.music.play(start=0.0)
                    self.cumulative_time = 0
                else:
                    if self.shufflevar.get()==1 and self.playlist.size()>1:
                        self.shuffle_songs()
                    else:
                        self.skip_forward()
            else:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(start=self.cumulative_time)
                self.update_progressbar()
#functie pentru intoarcere cu 5 secunde
    def reverse(self):
        if pygame.mixer.music.get_busy():
            current_offset=pygame.mixer.music.get_pos()/1000
            self.cumulative_time+=current_offset
            self.cumulative_time=max(self.cumulative_time-5,0)
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=self.cumulative_time)
            self.update_progressbar()
#functie pentru actualizarea progressbar
    def update_progressbar(self):
        current_time=pygame.mixer.music.get_pos()/1000 #afla timpul trecut in milisecunde si il transforma in secunde
        elapsed_time=int(self.cumulative_time+current_time)
        self.progress_bar["value"]=elapsed_time
        minutes,seconds=divmod(int(elapsed_time),60)
        self.present_time.config(text="{:02d}:{:02d}".format(minutes,seconds))
        timediff=self.song_length_g-(self.cumulative_time+current_time)
        #print(self.song_length_g-(self.cumulative_time+current_time))
        #print(self.loopvar.get())
        if timediff<=0.1:
            #print("ceva")
            if self.loopvar.get()==1:
                pygame.mixer.music.play(start=0.0)
                self.cumulative_time=0
                current_time=0
            else:
                if self.shufflevar.get()==1:
                    self.shuffle_songs()
                else:
                    self.skip_forward()
        self.root.after(100,self.update_progressbar)
root=tk.Tk() #creaza o fereastra
Spotify2(root) #creaza o instanta a clasei Spotify2
root.mainloop() #porneste aplicatia