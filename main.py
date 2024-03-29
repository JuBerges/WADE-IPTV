import subprocess
import os
import tkinter as tk
from tkinter import ttk

# Définir les couleurs
WHITE = "#ffffff"
BLACK = "#000000"
PINK = "#ffc8c8"
GRAY = "#cccccc"
BLUE = "#007bff"
# Charge le fichier M3U
m3u_file = open("./assets/jpn.m3u")

# Lire chaque ligne du fichier M3U et enregistrer les informations sur les chaînes dans une liste
channels = []
for line in m3u_file:
    if line.startswith("#EXTINF"):
        # Lire l'information sur la chaîne (nom, groupe, etc.)
        channel_info = line[8:].strip().split(",")
        channels.append({
            "name": channel_info[1],
            "group": channel_info[0],
            # ...
        })
    elif line.startswith("http"):
        # Lire l'URL de la chaîne
        channels[-1]["url"] = line.strip()
# Trouve l'exe de vlc        
def find_vlc_executable():
        # Liste des dossiers courants
        search_folders = ["C:\\", "C:\\Program Files (x86)\\VIDEOLAN\\VLC\\", "C:\\Program Files\\", "C:\\Program Files\\VideoLAN\\VLC"]

        # Nom de l'exécutable de VLC (peut varier en fonction de la version)
        vlc_executable = "vlc.exe"

        # Parcourons les dossiers et cherchons l'exécutable
        for folder in search_folders:
            vlc_path = os.path.join(folder, vlc_executable)
            if os.path.exists(vlc_path):
                return vlc_path

class ErrorVLC(Exception):
    pass
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Wade IPTV")
        self.master.geometry("500x400")
        self.master.configure(bg=BLUE)
        self.create_widgets()

    def create_widgets(self):
        # Ajouter un label pour le titre
        
        title_label = tk.Label(self.master, text="Liste des chaînes", font=("Impact", 24), bg=BLUE, fg=WHITE)
        title_label.pack(pady=20)

        # Créer un frame pour la liste des chaînes
        channel_frame = tk.Frame(self.master, bg=BLUE)
        channel_frame.pack(side="left", fill="y")
        # Centrer l'élément dans le cadre en utilisant la méthode place
        channel_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Ajouter un canvas pour la liste des chaînes
        channel_canvas = tk.Canvas(channel_frame, bg=BLUE, highlightthickness=0)
        channel_canvas.pack(side="left", fill="y")

        # Ajouter un scrollbar pour la liste des chaînes
        channel_scrollbar = ttk.Scrollbar(channel_frame, orient="vertical", command=channel_canvas.yview)
        channel_scrollbar.pack(side="right", fill="y")

        channel_canvas.configure(yscrollcommand=channel_scrollbar.set)
        channel_canvas.bind("<Configure>", lambda e: channel_canvas.configure(scrollregion=channel_canvas.bbox("all")))

        # Ajouter un frame pour les boutons de chaque chaîne
        channel_buttons = tk.Frame(channel_canvas, bg=BLUE) 
        channel_canvas.create_window((0, 0), window=channel_buttons, anchor="nw")

        # Créer une liste de boutons pour chaque chaîne
        self.channel_btns = []
        for i, channel in enumerate(channels):
            # Créer un bouton pour la chaîne
            channel_btn = tk.Button(channel_buttons, text=channel["name"], width=40, height=2,
                                    bg=WHITE, fg=BLUE,
                                    activebackground=BLUE, activeforeground=WHITE,
                                    font=("Helvetica", 12),
                                    command=lambda url=channel["url"]: self.play_channel(url))
            channel_btn.pack(pady=5)

            self.channel_btns.append(channel_btn)

    def play_channel(self, url):
        vlc_path = find_vlc_executable()

        if vlc_path is not None:
            # Exécuter la commande "vlc" avec le lien m3u8 en tant qu'argument
            subprocess.Popen([vlc_path, url])
        else:
            raise ErrorVLC("Vous devez avoir VLC d'installé !")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
 