import language_tool_python

# Créer une instance de l'outil
tool = language_tool_python.LanguageTool('fr')  # 'fr' pour le français

# Texte à vérifier
text = "Bonjour, pour avoir du sons il faut bien que le vidéo projecteur sois allumer. Si il a pas de sons verrifier que Windows a bien du sons. Sinon il faut monter le sons directement sur le vidéo projecteur sois avec la télécommande si il en a une sinon directement sur le vidéo"

# Obtenir les corrections
matches = tool.check(text)

# Fonction pour afficher les options et obtenir le choix de l'utilisateur
def get_user_choice(options):
    print("Choisissez une correction :")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Ignorer cette correction")
    
    while True:
        try:
            choice = int(input("Votre choix (0-" + str(len(options)) + "): "))
            if 0 <= choice <= len(options):
                return choice - 1  # -1 car l'indexation commence à 0
            else:
                print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

# Corriger le texte en fonction des choix de l'utilisateur
corrected_text = text
offset = 0

for match in matches:
    print(f"\nErreur trouvée : {match.message}")
    print(f"Contexte : {match.context}")
    
    if match.replacements:
        choice = get_user_choice(match.replacements)
        if choice >= 0:  # Si l'utilisateur n'a pas choisi d'ignorer
            replacement = match.replacements[choice]
            start = match.offset + offset
            end = start + match.errorLength
            corrected_text = corrected_text[:start] + replacement + corrected_text[end:]
            offset += len(replacement) - match.errorLength
    else:
        print("Aucune suggestion disponible pour cette erreur.")

print("\nTexte corrigé :", corrected_text)