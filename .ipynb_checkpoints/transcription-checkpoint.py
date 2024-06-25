import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whisper

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)
    print(f"String saved to {filename}")
        
    
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file created: {event.src_path}")
            # Transcribe the audio file
            try:
                result = model.transcribe(f'{event.src_path}')
                print()
                print(bcolors.OKCYAN +  result["text"] + bcolors.ENDC)
                filename = f"./segments/script_{event.src_path.strip('/Users/ayashigure/Desktop/speech_recognition_lab/segments/')}.txt"
                save_string_to_file(result["text"], filename, mode='a')
                
                save_string_to_file(result["text"], general_transcription_txt, mode='a')

                print()
            except:

                print()

            
if __name__ == "__main__":
    # Load the pre-trained model
    model = whisper.load_model("base")

    directory_to_monitor = "./segments"  # Dir to monitor
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_monitor, recursive=False)
    
    general_transcription_txt = "transcription.txt"
    
    observer.start()
    print("Monitoring directory for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    print("\nMonitoring stopped.")
