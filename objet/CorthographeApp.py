from tkinter import*
import customtkinter as ctk
from tkinter.scrolledtext import*
from tkinter import StringVar, OptionMenu, messagebox
from objet.COrthographe import*
import pyperclip

class TextCorrectionApp:
    def __init__(self):
        self.__root = ctk.CTk()
        self.__root.maxsize(700,500)
        self.__root.minsize(700,500)
        self.corrector = COrthographe()  # Instancie l'objet de correction de texte
        self.error_vars = []  # Pour stocker les variables associées aux suggestions de correction
        self.__textCorrect = ""
        # Couleur et taille des texte 
        # Configuration de l'apparence
        ctk.set_appearance_mode("system") 
        ctk.set_default_color_theme("blue")
        ctheme = ctk.get_appearance_mode()
        if ctheme == "Dark" :
            background = ctk.ThemeManager.theme["CTk"]["fg_color"][1]
        else :
            background = ctk.ThemeManager.theme["CTk"]["fg_color"][0]
        styleText = ("Arial",15)
        styleTitre = ("Arial",25)
        # Configuration de la fenêtre principale
        self.__root.title("Correcteur de texte")
        # Frame
        self.__frameInText = ctk.CTkFrame(self.__root,width=700,height=500,fg_color=background)
        self.__frameCorrect =  ctk.CTkFrame(self.__root,width=700,height=500,fg_color=background)
        self.__frameOut =  ctk.CTkFrame(self.__root,width=700,height=500,fg_color=background)
        # Label de presentation 
        labelIn = ctk.CTkLabel(self.__frameInText,text="Phrase a corrigée :",fg_color=background,font=styleTitre)
        labelCorect = ctk.CTkLabel(self.__frameCorrect,text="Correction de la phrase :",fg_color=background,font=styleTitre)
        # Zone de texte pour entrer le texte à corriger
        self.__zoneTextIn = ScrolledText(self.__frameInText, wrap=WORD, width=80, height=10)
        # Bouton pour vérifier le texte
        self.__btnVerif = ctk.CTkButton(self.__frameInText, text="Vérifier le texte", command=self.__checkTexte,font=styleText)
        # Bouton pour appliquer les corrections
        self.__btnApply = ctk.CTkButton(self.__frameCorrect, text="Appliquer les corrections", command=self.__applyCorrection,font=styleText)
        # Zone de texte pour afficher les erreurs et corrections
        self.__zoneSortie = ScrolledText(self.__frameCorrect, wrap=WORD, width=80, height=15)
        # Label de sortie du texte 
        self.__labelOutCorrection = ctk.CTkLabel(self.__frameOut,justify="left",wraplength=400,fg_color=background,font=styleText)
        boutonCopy = ctk.CTkButton(self.__frameOut,text="Copier",command=self.__copyText,font=styleText)

        # Affichage
        labelIn.place(x=0,y=0)
        self.__zoneTextIn.place(relx=0.5, rely=0.5, anchor="center")
        self.__btnVerif.place(relx=0.5, rely=1.0, anchor="s")
        
        labelCorect.place(x=0,y=0)
        self.__zoneSortie.place(relx=0.5, rely=0.5, anchor="center")
        self.__btnApply.place(relx=0.5, rely=1.0, anchor="s")
        
        self.__labelOutCorrection.place(x=0,y=0)
        boutonCopy.place(relx=0.5, rely=1.0, anchor="s")
        
    
    def __checkTexte(self):
        self.__frameInText.pack_forget()
        self.__frameCorrect.pack()
        text = self.__zoneTextIn.get("1.0", END).strip()  # Récupère le texte de la zone de saisie
        self.matches = self.corrector.check_text(text)  # Vérifie le texte

        self.__zoneSortie.delete("1.0",END)  # Efface la zone de sortie
        self.error_vars = []  # Réinitialiser les variables des erreurs

        if self.matches:
            for i, match in enumerate(self.matches):
                error_message = f"Erreur {i + 1}: {match.message}\nContexte: {match.context}\n"
                self.__zoneSortie.insert(END, error_message)

                if match.replacements:
                    # Variable pour stocker le choix de l'utilisateur pour cette erreur
                    selected_correction = StringVar()
                    selected_correction.set("Ignorer")

                    # Ajoute les suggestions et "Ignorer" comme choix dans le menu déroulant
                    correction_choices = ["Ignorer"] + match.replacements
                    dropdown = OptionMenu(self.__zoneSortie, selected_correction, *correction_choices)
                    self.__zoneSortie.window_create(END, window=dropdown)

                    # Stocke la variable de correction dans la liste
                    self.error_vars.append(selected_correction)

                    # Ajoute une séparation entre chaque erreur
                    self.__zoneSortie.insert(END, "\n\n")
        else:
            self.__zoneSortie.insert(END, "Aucune erreur détectée.\n")
    
    def active(self):
        self.__frameInText.pack()
        self.__root.mainloop()
        
    
    def __applyCorrection(self):
        if not self.matches:
            messagebox.showinfo("Info", "Aucune correction à appliquer.")
            self.__frameCorrect.pack_forget()
            self.__frameInText.pack()
            return

        # Appliquer les corrections sélectionnées par l'utilisateur
        corrected_text = self.__zoneTextIn.get("1.0",END).strip()
        offset = 0

        for i, match in enumerate(self.matches):
            # Récupère le choix de correction de l'utilisateur pour cette erreur
            correction_choice = self.error_vars[i].get()

            if correction_choice != "Ignorer":
                replacement = correction_choice
                start = match.offset + offset
                end = start + match.errorLength
                corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
                offset += len(replacement) - match.errorLength

        # Met à jour la zone de texte avec le texte corrigé
        self.__textCorrect = corrected_text
        self.__labelOutCorrection.configure(text=corrected_text)
        self.__frameCorrect.pack_forget()
        self.__frameOut.pack()

        # Afficher une confirmation
        messagebox.showinfo("Info", "Les corrections ont été appliquées.")
    
    def __copyText(self):
        pyperclip.copy(self.__textCorrect)
        self.__frameOut.pack_forget()
        self.__frameInText.pack()
        self.__zoneTextIn.delete(1.0,END)
        messagebox.showinfo("Info","Texte corriger copier")