from tkinter import*
from tkinter.scrolledtext import*
from tkinter import StringVar, OptionMenu, messagebox
from objet.COrthographe import*

class TextCorrectionApp:
    def __init__(self, ):
        self.__root = Tk()
        self.__root.maxsize(700,500)
        self.__root.minsize(700,500)
        self.corrector = COrthographe()  # Instancie l'objet de correction de texte
        self.error_vars = []  # Pour stocker les variables associées aux suggestions de correction
        
        # Configuration de la fenêtre principale
        self.__root.title("Correcteur de texte")
        self.__root.geometry("800x600")

        # Zone de texte pour entrer le texte à corriger
        self.text_area = ScrolledText(self.__root, wrap=WORD, width=80, height=10)
        self.text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
        
        # Bouton pour vérifier le texte
        self.check_button = Button(self.__root, text="Vérifier le texte", command=self.check_text)
        self.check_button.grid(column=0, row=1, padx=10, pady=10)

        # Bouton pour appliquer les corrections
        self.apply_button = Button(self.__root, text="Appliquer les corrections", command=self.apply_corrections)
        self.apply_button.grid(column=1, row=1, padx=10, pady=10)

        # Zone de texte pour afficher les erreurs et corrections
        self.output_area = ScrolledText(self.__root, wrap=WORD, width=80, height=15)
        self.output_area.grid(column=0, row=2, padx=10, pady=10, columnspan=2)
    
    def check_text(self):
        text = self.text_area.get("1.0", END).strip()  # Récupère le texte de la zone de saisie
        self.matches = self.corrector.check_text(text)  # Vérifie le texte

        self.output_area.delete("1.0",END)  # Efface la zone de sortie
        self.error_vars = []  # Réinitialiser les variables des erreurs

        if self.matches:
            for i, match in enumerate(self.matches):
                error_message = f"Erreur {i + 1}: {match.message}\nContexte: {match.context}\n"
                self.output_area.insert(END, error_message)

                if match.replacements:
                    # Variable pour stocker le choix de l'utilisateur pour cette erreur
                    selected_correction = StringVar()
                    selected_correction.set("Ignorer")

                    # Ajoute les suggestions et "Ignorer" comme choix dans le menu déroulant
                    correction_choices = ["Ignorer"] + match.replacements
                    dropdown = OptionMenu(self.output_area, selected_correction, *correction_choices)
                    self.output_area.window_create(END, window=dropdown)

                    # Stocke la variable de correction dans la liste
                    self.error_vars.append(selected_correction)

                    # Ajoute une séparation entre chaque erreur
                    self.output_area.insert(END, "\n\n")
        else:
            self.output_area.insert(END, "Aucune erreur détectée.\n")
    
    def active(self):
        self.__root.mainloop()
    
    def apply_corrections(self):
        if not self.matches:
            messagebox.showinfo("Info", "Aucune correction à appliquer.")
            return

        # Appliquer les corrections sélectionnées par l'utilisateur
        corrected_text = self.text_area.get("1.0",END).strip()
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
        self.text_area.delete("1.0", END)
        self.text_area.insert(END, corrected_text)

        # Afficher une confirmation
        messagebox.showinfo("Info", "Les corrections ont été appliquées.")