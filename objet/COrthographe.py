import language_tool_python

class COrthographe:
    def __init__(self, language='fr'):
        """
        Initialise l'outil LanguageTool pour la correction linguistique.
        :param language: Le code de langue pour LanguageTool (par défaut 'fr' pour français).
        """
        self.tool = language_tool_python.LanguageTool(language)
        self.corrected_text = ""
        self.matches = []
    
    def check_text(self, text):
        """
        Vérifie le texte et retourne les erreurs trouvées par LanguageTool.
        :param text: Le texte à vérifier.
        :return: Liste des erreurs détectées.
        """
        self.matches = self.tool.check(text)
        self.corrected_text = text  # Initialise le texte corrigé avec l'original
        return self.matches
    
    def apply_correction(self, match_index, replacement_index):
        """
        Applique la correction choisie par l'utilisateur pour une erreur spécifique.
        :param match_index: L'indice de l'erreur à corriger.
        :param replacement_index: L'indice de la correction à appliquer.
        :return: Le texte corrigé.
        """
        if match_index < 0 or match_index >= len(self.matches):
            raise ValueError("Index d'erreur invalide")
        
        match = self.matches[match_index]
        if replacement_index < 0 or replacement_index >= len(match.replacements):
            raise ValueError("Index de remplacement invalide")

        replacement = match.replacements[replacement_index]
        start = match.offset
        end = start + match.errorLength
        self.corrected_text = self.corrected_text[:start] + replacement + self.corrected_text[end:]

        return self.corrected_text
    
    def ignore_correction(self, match_index):
        """
        Ignore une correction pour une erreur spécifique.
        :param match_index: L'indice de l'erreur à ignorer.
        :return: Le texte corrigé sans appliquer la correction.
        """
        if match_index < 0 or match_index >= len(self.matches):
            raise ValueError("Index d'erreur invalide")
        
        # Ne fait rien, simplement retourne le texte inchangé
        return self.corrected_text

    def get_corrected_text(self):
        """
        Retourne le texte corrigé.
        :return: Le texte corrigé.
        """
        return self.corrected_text

    def reset(self):
        """
        Réinitialise l'outil de correction pour un nouveau texte.
        """
        self.corrected_text = ""
        self.matches = []
