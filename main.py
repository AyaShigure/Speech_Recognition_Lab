import os
import multiprocessing
import subprocess
from bcolors import bcolors
import datetime

def PrintSystemHeader():
    # print('[' +  bcolors.FAIL + 'System' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.FAIL + 'Main' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString

def run_script(script_name):
    subprocess.call(['python3.10-intel64', script_name])

if __name__ == "__main__":

    systemHeaderString = PrintSystemHeader()
    # Create two processes
    try:
        os.mkdir('segments')
    except:
        print(systemHeaderString + ' ' + bcolors.CYAN + './segments is already created' + bcolors.ENDC)

    try:
        p1 = multiprocessing.Process(target=run_script, args=('parallel_transcripter_openai-whisper.py',))
        p2 = multiprocessing.Process(target=run_script, args=('parallel_recoder.py',))

        # Start both processes
        p1.start()
        p2.start()

        # Wait for both processes to complete
        p1.join()
        p2.join()
    except:
        print(systemHeaderString + ' ' + bcolors.FAIL + 'Keyboard interrupted, shutting down the system.' + bcolors.ENDC)
        p1.terminate()
        p2.terminate()

    print(systemHeaderString + ' ' + bcolors.FAIL + 'Execution is completed.' + bcolors.ENDC)
