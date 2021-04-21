from main import *
import threading
import colored

begin, commande = True, (os.system, ("oze",))

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", "voices[0].id")


def execute():
    global commande
    print(commande)
    if commande:
        if type(commande) == tuple:
            ex = threading.Thread(target=commande[0], args=commande[1])
        else:
            ex = threading.Thread(target=commande)
        ex.start()
        process()()
    else:
        pass


def speak(text: str):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio, language="fr-FR")
    except:
        pass
    return data


def run():
    global begin, commande
    while True:
        print(colored.stylize("ok", colored.fg("blue")))
        if begin:
            return
            data = "assistant"
        else:
            data = listen().lower()
        if "assistant" in data:
            begin = False
            data.replace("assistant", "")
            speak("J'écoute")
            while True:
                data = listen().lower()
                if "wikipédia" in data:
                    data = data.replace("wikipédia", "")
                    speak(search_wiki(data, "summary"))
                elif "synonyme" in data:
                    data = data.replace("synonyme ", "")
                    speak(ask_syno(data))
                elif "définition" in data:
                    data = data.replace("définition", "").replace(" ", "")
                    speak(ask_def(data, ""))
                elif "openoffice" in data or "open office" in data:
                    speak("Ouverture d'openoffice...")
                    subprocess.Popen(r"libreoffice")
                elif "firefox" in data:
                    speak("Ouverture de firefox...")
                    subprocess.Popen(r"firefox")
                elif "steam" in data:
                    speak("Ouverture de steam...")
                    subprocess.Popen(r"steam")
                elif "discord" in data:
                    speak("Ouverture de discord...")
                    subprocess.Popen(r"discord")
                elif "ccleaner" in data:
                    speak("Ouverture de ccleaner...")
                    subprocess.Popen(r"ccleaner")
                elif "pronote" in data:
                    speak("Ouverture d'Oze..")
                    commande = oze
                    return
                elif "youtube" in data:
                    speak("Ouverture de YouTube...")
                    commande = youtube
                    return
                elif "analyse" in data:
                    speak("Analyse en cours")
                    commande = scan
                    return
                elif "au revoir" in data:
                    speak("Au revoir")
                    break
                else:
                    print(
                        colored.stylize("Obtention des résultats...", colored.fg("red"))
                    )
                    try:
                        res = ask_alpha(data)
                    except:
                        res = None
                    if res:
                        speak(res)
                    else:
                        speak("Répétez s'il-vous-plaît")
        elif "au revoir" in data:
            commande = False
            print(colored.stylize("Bye !", colored.fg("blue")))
            break


class process:
    def __call__(self):
        run()
        execute()


process()()
execute()
