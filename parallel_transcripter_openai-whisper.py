import openai
import os

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import keyboard
import sys

from bcolors import bcolors

def is_running_as_sudo():
    return os.geteuid() == 0

# Transcripter
def transcription_with_openai_whisper(openai_client, audio_file_path):
  audio_file= open(f"{audio_file_path}", "rb")

  transcription = openai_client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
#   print(transcription.text)
  return transcription.text

# Utilities
def PrintTranscripterHeader():
    print('[' +  bcolors.color256(fg=154) + 'OpenAI Whisper-1 Transcripter' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=154) + 'OpenAI Whisper-1 Transcripter' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
    
def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)
    
    print(headerString + ' ' +  f"Transcription is saved to {filename}")
        
    
# New file detector
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, openai_client, general_transcription_txt):
        self.client = openai_client
        self.general_transcription_txt = general_transcription_txt

    def on_created(self, event):
        if not event.is_directory and event.src_path[-1] != 't': # The second condition: file is not a txt (last char is not 't')  
            print(bcolors.ENDC + bcolors.BOLD + '====================================================================' + bcolors.ENDC)
            print(headerString + ' ' + bcolors.HEADER + 'New transcription.' + bcolors.ENDC)
            print(headerString + ' ' + bcolors.UNDERLINE + f'Current time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + bcolors.ENDC)
            print(headerString + ' ' + f"New file is created: {event.src_path}")
            # Transcribe the audio file
            try:
                if not DEBUG_MODE:
                    result = transcription_with_openai_whisper(self.client, event.src_path)
                else:
                    print('...Debug mode is on...')
                    result = 'Debug mode test string'
                print('--------------------------------------------------------------------------------')
                print(headerString + ' ' + 'Transcription:')
                print(bcolors.OKCYAN + result + bcolors.ENDC)
                # print(len(headerString + ' ' ) * ' ' + bcolors.OKCYAN + result["text"] + bcolors.ENDC)
                print('--------------------------------------------------------------------------------')

                save_string_to_file(result, './' + self.general_transcription_txt, mode='a')

            except:
                pass

def main():

    if DEBUG_MODE:
        print(headerString + ' ' + bcolors.WARNING + 'Debug mode is on, OpenAI API for Whisper-1 will not be called.' + bcolors.ENDC)
    print(headerString + ' ' + bcolors.OKCYAN+'Use command "sudo -E python3" to run the scripts!'+bcolors.ENDC)

    if is_running_as_sudo() != 1:
        # print(bcolors.BOLD + '\n===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.FAIL + 'Please run the script with sudo' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================\n' + bcolors.ENDC)

        os._exit(0)

    # OpenAI 
    api_key = os.getenv("OPENAI_API_KEY")
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


    # Load the pre-trained model
    general_transcription_txt = "transcription.txt"

    directory_to_monitor = "./segments"  # Dir to monitor
    event_handler = NewFileHandler(client, general_transcription_txt)
    observer = Observer()
    observer.schedule(event_handler, directory_to_monitor, recursive=False)
    
    
    observer.start()
    print(headerString + ' ' + bcolors.HEADER + "Monitoring directory for new files..." + bcolors.ENDC)

    detectionInterval = 1000 # ms
    try:
        while True:
            for i in range(detectionInterval):
                time.sleep(0.001)
                # exit via detection
                if keyboard.is_pressed('esc'): # Exit
                    print(headerString + ' ' + bcolors.OKBLUE + 'Transcripter is exiting...' + bcolors.ENDC)
                    observer.stop()
                    observer.join()
                    print(headerString + ' ' + bcolors.HEADER + 'Monitoring stopped.' + bcolors.ENDC)
                    sys.exit() 

    # exit via KeyboardInterruption
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print(headerString + ' ' + bcolors.HEADER + 'Monitoring stopped.' + bcolors.ENDC)
    print(headerString + ' ' + bcolors.FAIL + 'KeyboardInterruption is detected, shutting down..' + bcolors.ENDC)
    os._exit(0)


if __name__ == "__main__":
    # Debug mode switch
    DEBUG_MODE = False
    
    headerString = PrintTranscripterHeader()
    main() # Keyboard interruption is handeled in the main function.
    # PrintTranscripterHeader()