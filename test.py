from googletrans import Translator

def translate_text(text, dest="en"):
    translator = Translator()
    translated = translator.translate(text, dest=dest)
    return translated.text


text = " پھر کیا ہیرا کیا خاک"


print(translate_text(text))