#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from requests import get
import shutil


def download_file(url):
    with get(url, stream=True) as r:
        with open("server.jar", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("done downloading server.jar")


def let_user_pick(options):
    print("Please choose:")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None


def yes_no_question(question):
    answer = input(question + " (Y/n)").strip.lower()
    if answer in ['yes', 'y']:
        return True
    elif answer in ['no', 'n']:
        return False
    else:
        yes_no_question(question)


def get_versions(server_type):

    response = get('https://getbukkit.org/download/' +
                   server_type).content.decode()
    soup = bs(response, 'html.parser')

    divs = soup.find_all("div", {"class": "col-sm-3"})

    versions = []
    for div in divs:
        if div != None:
            subtag = div.find('h2')
            if subtag != None:
                version = subtag.text
                if version != None:
                    versions.append(version)
    return versions


server_types = ["craftbukkit", "spigot"]

if __name__ == '__main__':
    server_type = server_types[let_user_pick(server_types)]
    versions = get_versions(server_type)
    version = versions[let_user_pick(versions)]
    jar_url = "https://download.getbukkit.org/{}/{}-{}.jar".format(
        server_type, server_type, version)
    print("SERVER TYPE:{}\nSERVER VERSION:{}\n starting download from {}...".format(
        server_type, version, jar_url))
    download_file(jar_url)
    eulaF = open("eula.txt", 'w')
    eulaF.write('eula=true')
    eulaF.close()
