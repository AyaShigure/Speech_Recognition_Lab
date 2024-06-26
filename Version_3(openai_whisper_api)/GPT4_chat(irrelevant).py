import openai
import os

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import keyboard
import sys

from bcolors import bcolors

# Utilities
def PrintGPTHeader():
    print('[' +  bcolors.color256(fg=154) + 'OpenAI GPT4' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=154) + 'OpenAI GPT4' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
def PrintUserHeader():
    print('[' +  bcolors.color256(fg=214) + 'YOU' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=214) + 'YOU' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
def PrintSystemHeader():
    print('[' +  bcolors.FAIL + 'System' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.FAIL + 'System' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString

def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)

    print(headerString + ' ' +  f"Transcription is saved to {filename}")

def OpenAI_initilizations():
    # OpenAI 
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    # print(api_key)
    if api_key == None:
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.FAIL + '\nOpenAI API key error! Exiting..\n' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        os._exit(0)
    else:
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.OKGREEN + 'OpenAI API Key is loaded!' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.OKCYAN + 'Loading OpenAI client..' + bcolors.ENDC)
        client = openai.OpenAI(
        api_key = api_key,
        )
        print(headerString + ' ' + bcolors.OKGREEN + 'Client is loaded!' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
    try:
        os.mkdir('./processed_transcriptions')
    except:
        print('./processed_transcriptions already exists\n')

    return client

def call_GPT_for_postprocessing(GPT_Prompt):

    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{GPT_Prompt}"}
        ]
        )
        # print(userHeaderString + ' ' + bcolors.color256(fg=223) + f'{GPT_Prompt}' + bcolors.ENDC)
        GPT_response = completion.choices[0].message.content

        print(headerString + ' ' + bcolors.OKCYAN + GPT_response + bcolors.ENDC)
        os.system('say {}'.format(GPT_response))
        print(systemHeaderString + ' ' + 'Done..')
    except:
        print('error')

    post_processed_string = None
    return post_processed_string

if __name__ == '__main__':
    headerString = PrintGPTHeader()
    userHeaderString = PrintUserHeader()
    systemHeaderString = PrintSystemHeader()

    client = OpenAI_initilizations()

    while True:
        try:
            input_str = input(userHeaderString + bcolors.color256(fg=223))
            _ = call_GPT_for_postprocessing(input_str)
        except KeyboardInterrupt:
            print()
            print(systemHeaderString + ' ' + bcolors.FAIL + "Process interrupted by the user." + bcolors.ENDC)
            break
    
    print(systemHeaderString + ' ' + bcolors.FAIL + "System is shutting down." + bcolors.ENDC)
