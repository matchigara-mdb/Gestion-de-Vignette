import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

#--------------------------------------
#      CONNEXION DE BASE DE DONNEES
#--------------------------------------

conn = sqlite3.connect("vignette_kinshasa_db")
cursor = conn.cursor()

#--------------------------------------
#      CREATION DES TABLES
#--------------------------------------

cursor.execute("""
               CREATE TABLE IF NOT EXISTS proprietaire(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nom TEXT,
                   commune TEXT,
                   adresse TEXT,
                   telephone TEXT
)
""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS vehicule(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   plaque TEXT,
                   marque TEXT,
                   proprietaire_id INTEGER,
                   FOREIGN KEY(proprietaire_id) REFERENCES 
                proprietaire(id)
)               
""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS vignette(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   vehicule_id INTEGER,
                   annee INTEGER,
                   montant REAL,
                   FOREIGN KEY(vehicule_id) REFERENCES 
                vehicule(id)                  
)              
""")
cursor.execute("""
               CREATE TABLE IF NOT EXISTS paiement(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   vignette_id INTEGER,
                   date_paiement TEXT,
                   montant_paye REAL,
                   FOREIGN KEY(vignette_id) REFERENCES 
                vignette(id)                   
)                  
""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS amende(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   vehicule_id INTEGER,
                   jours_retard REAL,
                   FOREIGN KEY(vehicule_id) REFERENCES 
                vehicule(id)
)
""")

conn.commit()

#--------------------------------------
#      CALCUL D'AMENDE
#--------------------------------------

def calcul_amnende(jours):
    return jours*500 # ce qui veut dire que le contrevenant payera 500 Fc par jour

#--------------------------------------
#      INTERFACE
#--------------------------------------

app = tk.Tk()
app.geometry("1000x600")
app.title("Système de Gestion des Vignettes-Kinshasa")

notebook = ttk.Notebook(app)
notebook.pack(fill="both", expand=True)

#--------------------------------------
#      DONNEES PROPRIETAIRE
#--------------------------------------

frame_proprietaire = tk.Frame(notebook)
notebook.add(frame_proprietaire, text="Proprietaire")

tk.Label(frame_proprietaire, text="Nom").grid(row=0, column=0)
entry_nom =tk.Entry(frame_proprietaire)
entry_nom.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_proprietaire, text="Commune").grid(row=1,column=0)
entry_commune = tk.Entry(frame_proprietaire)
entry_commune.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_proprietaire, text="Adresse").grid(row=2,column=0)
entry_adresse = tk.Entry(frame_proprietaire)
entry_adresse.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_proprietaire, text="Telephone").grid(row=3,column=0)
entry_telephone = tk.Entry(frame_proprietaire)
entry_telephone.grid(row=3, column=1, padx=5, pady=5)
tree_proprietaire = ttk.Treeview(frame_proprietaire, column=("ID", "Nom", "Commune", "Adresse", "Telephone"), show="headings")
for col in ("ID", "Nom", "Commune", "Adresse", "Telephone"):
    tree_proprietaire.heading(col, text=col)
    tree_proprietaire.grid(row=5, column=0, columnspan=2, pady=10)

def afficher_proprietaire():
    for row in tree_proprietaire.get_children():
        tree_proprietaire.delete(row)
    cursor.execute("SELCT * FROM proprietaire")
    for proprietaire in cursor.fetchall():
        tree_proprietaire.insert("", tk.END, values=proprietaire)
        

def ajouter_proprietaire():
    if not entry_nom.get() or not entry_commune.get() or not entry_adresse.get() or not entry_telephone.get():
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        return
        
    cursor.execute("INSERE DANS proprietaire(nom, commune, adresse, telephone) VALUES(?, ?, ?, ?)", entry_nom.get(), entry_commune.get(), entry_adresse.get(), entry_telephone.get())
    conn.commit()
    messagebox.showinfo("Succès", "Proprietaire ajouté")
    entry_nom.delete(0, tk.END)
    entry_commune.delete(0, tk.END)
    entry_adresse.delete(0, tk.END)
    entry_telephone.delete(0, tk.END)
    
    afficher_proprietaire()
    
    tk.Button(frame_proprietaire, text="Ajouter", command=ajouter_proprietaire).grid(row=4, column=1, pady=5)
    afficher_proprietaire()
    
frame_vehicule = ttk.Frame(notebook)
notebook.add(frame_vehicule, text="Vehicule")

tk.Label(frame_vehicule, text="Plaque").grid(row=0,column=0)
entry_plaque = tk.Entry(frame_vehicule)
entry_plaque.grid(row=0, column=1)

tk.Label(frame_vehicule, text="Marque").grid(row=1,column=0)
entry_marque = tk.Entry(frame_vehicule)
entry_marque.grid(row=1, column=1)

tk.Label(frame_vehicule, text="ID Poprietaire").grid(row=2,column=0)
entry_proprietaire_id = tk.Entry(frame_proprietaire)
entry_proprietaire_id.grid(row=2, column=1)

def ajouter_vehicule():
    cursor.execute("INSERT INTO vehicule(plaque, marque, proprietaire_id) VALUES(?, ?, ?, ?)", entry_plaque.get(), entry_marque.get(), entry_proprietaire_id.get())
    conn.commit()
    messagebox.showinfo("Succès", "Vehicule ajouté")
    
    tk.Button(frame_vehicule, text="Ajouter", command=ajouter_vehicule).grid(row=3, column=1)
    
    
frame_vignette = ttk.Frame(notebook)
notebook.add(frame_vignette, text="Vignette")

tk.Label(frame_vignette, text="ID Vehicule").grid(row=1,column=0)
entry_vehicule_id = tk.Entry(frame_vignette)
entry_vehicule_id.grid(row=0, column=1)

tk.Label(frame_vignette, text="Année").grid(row=1,column=0)
entry_annee = tk.Entry(frame_vignette)
entry_annee.grid(row=1, column=1)

tk.Label(frame_vignette, text="Montant").grid(row=2,column=1)
entry_montant = tk.Entry(frame_vignette)
entry_annee.grid(row=2, column=1)


def ajouter_vignette():
    cursor.execute("INSERT INTO vignette, vehicule_id, annee, montant) VALUES(?, ?, ?, ?)", entry_vehicule_id.get(), entry_annee.get(), entry_montant.get())
    conn.commit()
    messagebox.showinfo("Succès", "Vignette enregistrée")
    
    tk.Button(frame_vehicule, text="Ajouter", command=ajouter_vignette).grid(row=3, column=1)
    
    
    
frame_pay = ttk.Frame(notebook)
notebook.add(frame_pay, text="Paiement")

tk.Label(frame_pay, text="ID Vignette").grid(row=0,column=0)
entry_vignette_id = tk.Entry(frame_pay)
entry_vignette_id.grid(row=0, column=1)

tk.Label(frame_vignette, text="Montant payé").grid(row=1,column=0)
entry_montant_paye = tk.Entry(frame_pay)
entry_montant_paye.grid(row=1, column=1)


def ajouter_paiement():
    date = datetime.now().strftime("")
    cursor.execute("INSERT INTO paiement(vignette_id, date paiement, montant_paye) VALUES(?,?,?)", entry_vignette_id.get(), date, entry_montant_paye.get())
    conn.commit()
    messagebox.showinfo("Succès", "Paiement enregistré")
    
    tk.Button(frame_vehicule, text="AjoValider Paiement", command=" ajouter_paiement").grid(row=2, column=1)
    
    

frame_amende = ttk.Frame(notebook)
notebook.add(frame_amende, text="Amende")

tk.Label(frame_amende, text="ID Vehicule").grid(row=0,column=0)
entry_vehicule_amende = tk.Entry(frame_amende)
entry_vehicule_amende.grid(row=0, column=1)

tk.Label(frame_amende, text="Jours de retard").grid(row=1,column=0)
entry_jours = tk.Entry(frame_amende)
entry_jours.grid(row=1, column=1)

tk.Label(frame_vignette, text="Montant payé").grid(row=1,column=0)
entry_montant_paye = tk.Entry(frame_pay)
entry_montant_paye.grid(row=1, column=1)

label_resultat = tk.Label(frame_amende, text="Montant Amende:0FC")
label_resultat.grid(row=3, column=1)

def enregistrer_amende():
    jours = int(entry_jours.get()) 
    montant = calcul_amende(jours)
    cursor.execute("INSERT INTO paiement(vehicule_id, djours_retard, montant_amende) VALUES(?,?,?)", (entry_vehicule_id.get(), jours, montant))
    conn.commit()
    label_resultat.config(text=f"Montant Amende:{montant} FC")
    messagebox.showinfo("Succès", "Amende enregistrée")
    
    tk.Button(frame_amende, text="Calculer et Enregistrer", command=" enregistre_amende").grid(row=2, column=1)
    
    app.mainloop()
    conn.close()
    
    
    
    
    
    
    
    

