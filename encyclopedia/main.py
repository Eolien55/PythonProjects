import requests
from bs4 import BeautifulSoup
import time
import os
import json
import subprocess
import wikipedia
import speech_recognition as sr
import pyttsx3
import webbrowser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pyautogui
import wolframalpha
import googletrans as translate
import os
import codecs
import re

print("Hello from me")
translate_to = translate.Translator()
translate_from = translate.Translator()

app_id = "7W7ERW-9RH4E9287J"
client = wolframalpha.Client(app_id)


def ask_alpha(ask: str):
    global translate_to, translate_from, client
    ask = translate_to.translate(ask, src="fr", dest="en").text
    res = client.query(ask)
    for pod in res.pods:
        res = (
            translate_from.translate(
                pod["subpod"]["img"]["@alt"], src="en", dest="fr"
            ).text
            if pod["@title"] == "Result"
            else None
        )
        if res:
            return res


def oze():
    options = Options()
    options.binary_location = r"/lib/firefox/firefox"
    while 1:
        try:
            driver = webdriver.Firefox(
                executable_path=r"/home/elie/geckodriver",
                firefox_options=options,
            )
            driver.get("http://ozecollege.yvelines.fr")
            break
        except:
            pass
    usn = driver.find_element_by_id("input_1")
    pw = driver.find_element_by_id("input_2")
    submit = driver.find_element_by_id("SubmitCreds")
    usn.send_keys("elie.levaillant")
    pw.send_keys("Nescado2007")
    submit.submit()
    while 1:
        try:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if (
                    "https://0781105c.index-education.net/pronote/eleve.html?"
                    in driver.current_url
                ):
                    quit()
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                break
            menu = driver.find_element_by_xpath(
                "/html/body/app-root/div/div/oze-header/header/div/ul[1]/li[6]/oze-launcher/span/button/i"
            )
            menu.click()
            pronote = driver.find_element_by_xpath(
                "/html/body/app-root/div/div/oze-header/header/div/ul[1]/li[6]/oze-launcher/div/div[2]/div[1]/div[3]/div[3]/ozapp-icon-xs/a/oze-icon/i"
            )
            pronote.click()
            break
        except:
            pass


def ask_syno(mot: str, wordtype: str = ""):
    url = "https://www.cnrtl.fr/synonymie/" + mot + "/" + wordtype
    syno = [mot]
    html = requests.get(url).text
    html = BeautifulSoup(html, "html.parser")
    for i in html.find_all(class_="syno_format"):
        for il in i.find_all("a"):
            syno.append(il.text.strip())
    return syno


def scrapping_def(url: str):
    definition = []
    html = requests.get(url).text
    html = BeautifulSoup(html, "html.parser")
    for i in html.find_all(class_="tlf_parah"):
        c, d = [], []
        if "tlf_parah" not in str(i)[str(i).index("tlf_parah") + 2 :]:
            if i.find_all(class_="tlf_cdefinition"):
                for e in i.find_all(class_="tlf_cdefinition"):
                    c.append("Définition " + str(len(definition) + 1) + " : ")
                    c.append(e.text.strip())
            d.append(c)
            definition.append(d)
    return definition


def ask_def(mot: str, wordtype: str = ""):
    url = "https://www.cnrtl.fr/definition/" + mot + "/" + wordtype
    return scrapping_def(url)


def phonetique(mot: str):
    url = "https://fr.wiktionary.org/wiki/" + mot
    html = requests.get(url).text
    html = BeautifulSoup(html, "html.parser")
    for i in html.find_all(class_="API"):
        i = i.text.strip()
        return i[1:-1]


def search_wiki(subject: str, mode: str = "", lines: int = 3, mot: str = ""):
    wikipedia.set_lang("fr")
    page = wikipedia.page(subject)
    if mode:
        return wikipedia.summary(subject)
    elif mot:
        page = page.content
        mot = ask_syno(mot)
        for mots in mot:
            if mots in page:
                p = page.split(".")
                a1 = [i for i in range(len(p)) if mots in p[i]]
                for a in a1:
                    page = p[a] + "."
                    return page


def youtube(video: str = False):
    webbrowser.open("http://youtube.com")
    time.sleep(50)
    pyautogui.moveTo((875, 580))
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo((540, 380))
    pyautogui.click()
    pyautogui.write("0652475588")
    pyautogui.moveTo((810, 575))
    pyautogui.click()
    time.sleep(15)
    pyautogui.moveTo((810, 520))
    pyautogui.click()
    if video:
        time.sleep(12)
        pyautogui.moveTo((570, 105))
        pyautogui.click()
        pyautogui.write(video + "\n")


search_wiki("wikipedia")


def scan():
    pass
