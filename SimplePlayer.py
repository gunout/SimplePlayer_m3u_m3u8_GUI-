import tkinter as tk
from tkinter import filedialog, messagebox
import vlc
from tkinterdnd2 import DND_FILES, TkinterDnD

class M3UPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Lecteur M3U / M3U8")

        # Créer une instance VLC avec le support de PulseAudio
        self.instance = vlc.Instance('--aout=pulse')  # Utiliser PulseAudio
        self.player = self.instance.media_player_new()

        # Cadre pour le lecteur
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Liste des liens
        self.link_list = tk.Listbox(self.frame)
        self.link_list.pack()

        # Volume
        self.volume_scale = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume")
        self.volume_scale.set(50)  # Volume par défaut
        self.volume_scale.pack()
        self.volume_scale.bind("<Motion>", self.change_volume)

        # Bouton pour jouer le lien sélectionné
        self.play_button = tk.Button(self.frame, text="Jouer", command=self.play_selected)
        self.play_button.pack()

        # Bouton pour arrêter le stream
        self.stop_button = tk.Button(self.frame, text="Arrêter", command=self.stop_stream)
        self.stop_button.pack()

        # Bouton pour quitter l'application
        self.quit_button = tk.Button(self.frame, text="Quitter", command=self.master.quit)
        self.quit_button.pack()

        # Configuration du glisser-déposer
        self.link_list.drop_target_register(DND_FILES)
        self.link_list.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        file_path = event.data.strip('{}')  # Enlever les accolades
        if file_path.endswith(('.m3u', '.m3u8')):
            self.add_links_from_file(file_path)
        else:
            messagebox.showwarning("Avertissement", "Veuillez déposer un fichier M3U ou M3U8.")

    def add_links_from_file(self, file_path):
        self.link_list.delete(0, tk.END)  # Vider la liste
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Ignorer les lignes de commentaires
                        self.link_list.insert(tk.END, line)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier: {e}")

    def change_volume(self, event):
        volume = self.volume_scale.get()
        self.player.audio_set_volume(volume)

    def play_selected(self):
        selected_index = self.link_list.curselection()
        if selected_index:
            link = self.link_list.get(selected_index)
            media = self.instance.media_new(link)
            self.player.set_media(media)
            
            # Démarrer la lecture
            self.player.play()
            # Définir le volume après le démarrage
            self.change_volume(None)
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lien à jouer.")

    def stop_stream(self):
        self.player.stop()

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Utiliser TkinterDnD au lieu de tk.Tk()
    app = M3UPlayer(root)
    root.mainloop()
