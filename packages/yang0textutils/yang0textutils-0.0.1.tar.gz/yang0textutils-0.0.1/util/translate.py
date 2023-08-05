from googletrans import Translator

translator = Translator()

def en2cn(str):
    return translator.translate(str, dest='zh-CN').text

def cn2en(str):
    return translator.translate(str).text