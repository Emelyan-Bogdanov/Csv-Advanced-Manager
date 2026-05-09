import requests
import json
from colorama import Fore , Style

from colorama import init, Fore, Back, Style

init(convert=True)

def getDeepAiAnswer(query: str):
    url = "https://api.deepai.org/hacking_is_a_serious_crime"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "api-key": "tryit-29313838055-92efd3f13305fd73765982f1e4bd8c0b",
        "Origin": "https://deepai.org",
        "Connection": "keep-alive"
    }

    # Use `files` to simulate multipart/form-data
    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, '[{"role":"user","content":"hi ,%s "}]' % query),
        "model": (None, "gpt-oss-120b"),
        "session_uuid": (None, "bb3d57a9-405f-40e9-a6dc-0a831175d7b4"),
        "hacker_is_stinky": (None, "very_stinky"),
        "enabled_tools": (None, '["image_generator","image_editor"]')
    }

    response = requests.post(url, headers=headers, files=files)
    return response.text


def yellow(s):
	return f"{Fore.YELLOW}{s}{Style.RESET_ALL}"

def green(s):
	return f"{Fore.GREEN}{s}{Style.RESET_ALL}"


import click

@click.command()
@click.option("-chat",default="" , help="tell the assistant something")
@click.option("-create",default="",help="create a file and let the assistant generate its content")
@click.option("-description",default="",help="give the description that the assistant would generate content")
def main(chat=None, create=None , description=None):
    
    Content = ""
    filename = ""
    path = "" 
    
    # chat
    if chat.strip() != "" :
        print(f"[Start chat mode]")
        input("type enter to continue...")
        while True :
            print(f"{Fore.YELLOW}>>",end="")
            i = input()
            print(Style.RESET_ALL,end="")
            r = getDeepAiAnswer(i)
            print(green(f"[Assistant] : {r}"))
            print()
    
    # get the description
    if description.strip() != "" and description is not None :
        system = "i want you to generate a file content wich is a code , and i want you only to returns the content of that file with no desciption or non language syntaxe , here is the task : "
        r = getDeepAiAnswer(f"{system}{description} , only returns the content ofthe file  , no description")
        Content = r
    
        
    # else create file
    if create.strip() != "" and  create is not None :
        # create folder
        with open(f"{filename}","w") as file :
            file.write(description)
    
main()