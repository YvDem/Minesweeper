import tkinter as tk
import time


class Arbre:
    def __init__(self, racine=None):
        self.racine = racine
        self.gauche = None
        self.droite = None

    def ajouter_racine(self, valeur):
        if self.racine == None:
            self.racine = valeur
            return
        elif valeur > self.racine:
            if self.droite is None:
                self.droite = Arbre(valeur)
            return self.droite.ajouter_racine(valeur)
        elif valeur < self.racine:
            if self.gauche is None:
                self.gauche = Arbre(valeur)
            return self.gauche.ajouter_racine(valeur)
        else:
            return

    def retrouver_mot(self, mot):
        if self.racine == None:
            return False, None
        elif self.racine == mot:
            return True, None
        elif mot > self.racine:
            if self.droite is not None:
                return self.droite.retrouver_mot(mot)
        elif mot < self.racine:
            if self.gauche is not None:
                return self.gauche.retrouver_mot(mot)
        return False, self.racine


tree = Arbre()
with open('corpus_mots_fr.txt', 'r', encoding='utf-8') as file:
    for line in file:
        mot = line.strip()
        tree.ajouter_racine(mot)


def mot_present(mot):
    rep, rep1 = tree.retrouver_mot(str(mot))
    if rep:
        rep = f'Le mot «{mot}» fait partie de notre base de donnés 😊'
    else:
        rep = f'«{mot}» non trouvé, vouliez vous chercher «{rep1}» ?😥'
    return rep


# GUI
def get_text():
    texte = zone_texte.get()
    if texte == '':
        texte_recupere.config(text="Vous n'avez pas saisi de mot", font=(
            "Helvetica", 15, 'bold'), wraplength=300)
    else:
        start_time = time.time()
        texte = mot_present(texte)
        zone_texte.delete(0, tk.END)
        texte_recupere.config(text=texte, font=(
            "Helvetica", 15, 'bold'), wraplength=300)
        end_time = time.time()
        duration = end_time - start_time
        duree.config(text="Durée d'exécution: {:.12f} secondes".format(
            duration), font=("Helvetica", 10, 'bold'), wraplength=300)


def on_key_press(event):
    if event.keysym == 'Return':
        bouton.config(bg='blue', fg='white')
        get_text()


def on_key_release(event):
    if event.keysym == 'Return':
        bouton.config(bg='grey', fg='black')


def on_enter(e):
    bouton.config(bg='blue', fg='white')


def on_leave(e):
    bouton.config(bg='grey', fg='black')


# Créer une fenêtre
fenetre = tk.Tk()

# Récupérer la largeur et la hauteur de l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()

# Calculer la position de la fenêtre pour qu'elle soit centrée sur l'écran
x_pos = (largeur_ecran - 400) // 2
y_pos = (hauteur_ecran - 400) // 2

fenetre.geometry(f"400x400+{x_pos}+{y_pos}")
fenetre.title("APP2 : Structure de recherche")

label = tk.Label(fenetre, text="Bienvenue sur cette base de donnée ultra performante. Vous pouvez entrer le mot de votre choix dans la barre de recherche : ", font=(
    "Helvetica", 10), wraplength=300)
zone_texte = tk.Entry(fenetre, bd=0, highlightbackground='red',
                      highlightcolor='red', highlightthickness=2, width=30)
bouton = tk.Button(text="🔍 rechercher", font=("Helvetica", 10, 'bold'),
                   command=get_text, highlightbackground='blue', highlightcolor='blue', bg='grey')
espace1 = tk.Frame(fenetre, height=10)
espace2 = tk.Frame(fenetre, height=40)
espace3 = tk.Frame(fenetre, height=30)
espace4 = tk.Frame(fenetre, height=40)
texte_recupere = tk.Label(fenetre, text='')
espace5 = tk.Frame(fenetre, height=40)
duree = tk.Label(fenetre, text='')

espace1.pack()
label.pack()
espace2.pack()
zone_texte.pack()
espace3.pack()
bouton.pack()
espace4.pack()
texte_recupere.pack()
espace5.pack()
duree.pack()

zone_texte.bind('<KeyPress>', on_key_press)
zone_texte.bind('<KeyRelease>', on_key_release)
bouton.bind('<Enter>', on_enter)
bouton.bind('<Leave>', on_leave)
bouton.bind('<Button-1>')
zone_texte.bind('<Button-1>')
fenetre.mainloop()
