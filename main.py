import pygame
import subprocess
from helpers.get_vlc_path import find_vlc_executable

# Charger le fichier M3U
m3u_file = open("./data/jpn.m3u")

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

# Initialiser Pygame
pygame.init()
# Créer une fenêtre
window = pygame.display.set_mode((800, 600))
# Charger une police de caractères pour afficher le texte
font = pygame.font.Font(None, 24)

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
# Variable pour stocker la chaîne sélectionnée
selected_channel = None

# Boucle principale pour afficher l'interface graphique
while selected_channel is None:
    # Traiter les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selected_channel = "EXIT"
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Récupérer les coordonnées de la souris
            mouse_x, mouse_y = event.pos

            # Vérifier si la souris a cliqué sur un bouton
            for i, channel in enumerate(channels):
                # Calculer les coordonnées du bouton
                button_x = 10
                button_y = 10 + i * 30
                button_w = 780
                button_h = 24

                # Vérifier si la souris a cliqué sur le bouton
                if (button_x <= mouse_x <= button_x + button_w) and (button_y <= mouse_y <= button_y + button_h):
                    selected_channel = channel
                    break

    # Effacer l'écran
    window.fill(BLACK)

    # Afficher les boutons pour chaque chaîne
    for i, channel in enumerate(channels):
        # Calculer les coordonnées du bouton
        button_x = 10
        button_y = 10 + i * 30
        button_w = 780
        button_h = 24

        # Dessiner un rectangle pour le bouton
        pygame.draw.rect(window, PINK, (button_x, button_y, button_w, button_h))

        # Afficher le nom de la chaîne sur le bouton
        text = font.render(channel["name"], True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (button_x + button_w // 2, button_y + button_h // 2)
        window.blit(text, text_rect)

    # Mettre à jour l'affichage
    pygame.display.update()

# Si l'utilisateur a quitté l'application, quitter
if selected_channel == "EXIT":
    pygame.quit()
    exit()
vlc_path = find_vlc_executable()
# Lire la chaîne sélectionnée
#print(selected_channel["url"])
#print(vlc_path)
if vlc_path  != None:
    # Exécutez la commande "vlc" avec le lien m3u8 en tant qu'argument
    subprocess.run([vlc_path, selected_channel["url"]])



