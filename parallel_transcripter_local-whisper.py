import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whisper
import datetime
import keyboard
import sys

from bcolors import bcolors
# Use bcolors.color256(fg=154) for recoder
def PrintTranscripterHeader():
    print('[' +  bcolors.color256(fg=154) + 'Transcripter' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=154) + 'Transcripter' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
    
def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)
    
    print(headerString + ' ' +  f"Transcription is saved to {filename}")
        
    
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, model, general_transcription_txt):
        self.model = model
        self.general_transcription_txt = general_transcription_txt

    def on_created(self, event):
        if not event.is_directory and event.src_path[-1] != 't': # The second condition: file is not a txt (last char is not 't')  
            print(bcolors.ENDC + bcolors.BOLD + '====================================================================\n' + bcolors.ENDC)
            print(headerString + ' ' + bcolors.HEADER + 'New transcription.' + bcolors.ENDC)
            print(headerString + ' ' + bcolors.UNDERLINE + f'Current time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + bcolors.ENDC)
            print(headerString + ' ' + f"New file is created: {event.src_path}")
            # Transcribe the audio file
            try:
                result = self.model.transcribe(f'{event.src_path}', fp16=False)

                print('--------------------------------------------------------------------------------')
                print(headerString + ' ' + 'Transcription:')
                print(bcolors.OKCYAN + result["text"] + bcolors.ENDC)
                # print(len(headerString + ' ' ) * ' ' + bcolors.OKCYAN + result["text"] + bcolors.ENDC)
                print('--------------------------------------------------------------------------------')

                filename = f"./segments/script_{event.src_path.strip('/Users/ayashigure/Desktop/speech_recognition_lab/segments/')}.txt"

                save_string_to_file(result["text"], filename, mode='a')
                save_string_to_file(result["text"], self.general_transcription_txt, mode='a')

            except:
                pass

def main():
    # Load the pre-trained model
    model = whisper.load_model("base")
    general_transcription_txt = "transcription.txt"

    directory_to_monitor = "./segments"  # Dir to monitor
    event_handler = NewFileHandler(model, general_transcription_txt)
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
                if keyboard.is_pressed('q'): # Exit
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


if __name__ == "__main__":
    headerString = PrintTranscripterHeader()

    main()
    # PrintTranscripterHeader()