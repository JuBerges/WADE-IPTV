import os
#trouve le chemin de l'exec VLC sur mon pc 
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