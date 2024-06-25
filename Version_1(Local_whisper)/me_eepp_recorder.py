import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import keyboard
import datetime
import sys
import time


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
def clear_line():
    # Move the cursor to the start of the line and clear the line
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()
    
def record_system_sound_loop(sample_rate, device=None, channels=2):
    # List to hold recorded audio data
    audio_data = []
    now = datetime.datetime.now()

#     def callback(indata, frames, time, status):
#         if status:
#             print(status, file=sys.stderr)
#         audio_data.append(indata.copy())
    
    def callback(indata, frames, time, status):
        nonlocal audio_data  # Ensure we're modifying the outer scope's audio_data
        if status:
            print(status, file=sys.stderr)
        try:
            audio_data.append(indata.copy())    
        except:
            print(bcolors.WARNING + 'WARNING_01, The incomming data maybe empty.' + bcolors.ENDC)
    
    # Main loop
    index = 1
    while True:
        # List to hold recorded audio data / clear the list
        # audio_data = []
        start_time = time.time()
        record_time = 60 # Record time before creating a wav file and loop
        print(bcolors.FAIL + f'\nRecord time is set to {record_time}s' + bcolors.ENDC)

        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback, device=device):
            while True:
                

                # print(bcolors.OKGREEN + f'Record timt: [{round(time.time()-start_time, 0)}/{record_time}]' + bcolors.ENDC)

                if keyboard.is_pressed('c') or time.time()-start_time > record_time: # Cut

                    try:
                        print(bcolors.HEADER + "Auto-segmenting... Creating wav segment..." + bcolors.ENDC)
                        # Save the audio data to a WAV file
                        now = datetime.datetime.now()
                        output_file = "./segments/Segment_{}_{}.wav".format(index, now)
                        
                        try:
                            audio_data = np.concatenate(audio_data, axis=0)
                        except:
                            print(bcolors.FAIL + 'audio_data maybe empty..' + bcolors.ENDC)
                        wavfile.write(output_file, sample_rate, audio_data)
                        print(f"Saved recording to {output_file}...")    
                        index += 1
                        print('Index is raised by 1..')

                        # Reset audio_data !! its a global list
                        audio_data = []
                        break
                    except:
                        print(bcolors.FAIL + '..ERROR_01..' + bcolors.ENDC)
                        break
                    
                if keyboard.is_pressed('q'): # Exit
                    print("Manual segmenting... Creating wav segment...")
                    # Save the audio data to a WAV file
                    now = datetime.datetime.now()
                    output_file = "./segments/Segment_{}_{}.wav".format(index, now)
                    
                    try:
                        audio_data = np.concatenate(audio_data, axis=0)
                    except:
                        print(bcolors.FAIL + 'audio_data maybe empty..' + bcolors.ENDC)
                        
                    wavfile.write(output_file, sample_rate, audio_data)
                    print(f"Saved recording to {output_file}...")    
                    
                    print(bcolors.OKBLUE + 'Exiting...' + bcolors.ENDC)
                    sys.exit() 


if __name__ == "__main__":
    
    ### Initializations ###
    sample_rate = 44100  # Sample rate in Hz

    # Check available devices
    devices = sd.query_devices()
    print(devices)

    # Device override
    micInOverrideFlag = False
    if micInOverrideFlag == True:
        print(bcolors.WARNING + 'Device override is activated' + bcolors.ENDC)
        selected_device = 'MacBook Pro麦克风'
        print(bcolors.WARNING + f'Override target device: {selected_device}.' + bcolors.ENDC)

        for device in devices:
            if selected_device in device['name']:  # Adjust this to match your system audio device's name
                print(f"Using device: {device['name']} with {device['max_input_channels']} channels")
                selected_device = device['index']
                break

    else:
        # Select the appropriate device (e.g., "Stereo Mix" or another system audio device)
        selected_device = None
        for device in devices:
            if 'Soundflower' in device['name']:  # Adjust this to match your system audio device's name
                print(f"Using device: {device['name']} with {device['max_input_channels']} channels")
                selected_device = device['index']
                break
    

    if selected_device is None:
        print("No suitable device found.")
    else:

        max_channels = sd.query_devices(selected_device)['max_input_channels']
        record_system_sound_loop(sample_rate, device=selected_device, channels=max_channels)
