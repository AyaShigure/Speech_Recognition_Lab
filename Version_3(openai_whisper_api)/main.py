import os
import multiprocessing
import subprocess

def run_script(script_name):
    subprocess.call(['python3.10-intel64', script_name])

if __name__ == "__main__":
    # Create two processes
    try:
        os.mkdir('segements')
    except:
        print('./segements is already created')
    p1 = multiprocessing.Process(target=run_script, args=('parallel_transcripter_openai-whisper.py',))
    p2 = multiprocessing.Process(target=run_script, args=('parallel_recoder.py',))

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to complete
    p1.join()
    p2.join()

    print("Both scripts have finished executing.")
