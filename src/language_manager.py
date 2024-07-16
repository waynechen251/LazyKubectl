import json

class LanguageManager:
    def __init__(self, language_file='src/languages/languages.json', default_language='en-US'):
        self.language_file = language_file
        self.current_language = default_language
        self.load_languages()

    def load_languages(self):
        with open(self.language_file, 'r', encoding='utf-8') as f:
            self.languages = json.load(f)

    def set_language(self, language):
        if language in self.languages['title'].keys():
            self.current_language = language
        else:
            print(f"Language '{language}' not found. Using default language '{self.current_language}'.")

    def translate(self, key):
        return self.languages.get(key, {}).get(self.current_language, key)

    def get_available_languages(self):
        return self.languages['available-languages']
