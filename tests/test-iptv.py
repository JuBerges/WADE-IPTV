# Importons les modules nécessaires
import os
import m3u8

#trouve le chemin de l'exec VLC sur mon pc 
def find_vlc_executable():
    # Liste des dossiers courants
    search_folders = ["C:\\", "C:\\Program Files (x86)\\", "C:\\Program Files\\"]

    # Nom de l'exécutable de VLC (peut varier en fonction de la version)
    vlc_executable = "vlc.exe"

    # Parcourons les dossiers et cherchons l'exécutable
    for folder in search_folders:
        vlc_path = os.path.join(folder, vlc_executable)
        if os.path.exists(vlc_path):
            return vlc_path

    # Si on n'a pas trouvé l'exécutable, retournons None
    return None


# Définissons le chemin vers le fichier M3U
m3u_file = "./jpn.m3u"

# Vérifions que le fichier existe
if not os.path.exists(m3u_file):
    print("Le fichier M3U spécifié n'existe pas.")
    exit()

# Créons un objet M3U8 à partir du fichier
try:
    m3u8_obj = m3u8.load(m3u_file)
except Exception:
    print("Erreur lors de la lecture du fichier M3U.")
    exit()

# Récupérons la liste des chaînes disponibles
channels = m3u8_obj.data["playlists"]

# Affiche la liste des chaînes et demande à l'utilisateur de choisir une ou plusieurs chaînes
selected_channels = []
for i, channel in enumerate(channels):
    print("{}. {}".format(i + 1, channel["name"]))

selected_channels_input = input("Choisissez une ou plusieurs chaînes (1-{}, séparées par des virgules): ".format(len(channels)))

# Vérifions que les chaînes sélectionnées sont valides
try:
    selected_channels = [int(ch) - 1 for ch in selected_channels_input.split(",")]
except ValueError:
    print("Entrée non valide.")
    exit()

for ch in selected_channels:
    if ch < 0 or ch >= len(channels):
        print("Chaîne sélectionnée non valide.")
        exit()

# Récupérons les flux vidéo des chaînes sélectionnées
video_streams = [channels[ch]["uri"] for ch in selected_channels]

# Utilisons un lecteur vidéo pour lire les flux vidéo (par exemple, VLC)
# Remplacez "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" avec
# le chemin vers l'exécutable de VLC sur votre ordinateur
vlc_path = find_vlc_executable()
for video_stream in video_streams:
    os.system('"{}" "{}"'.format(vlc_path, video_stream))
