import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import keyboard
import datetime
import sys
import time

from bcolors import bcolors
# Use bcolors.OKGREEN for recoder
def PrintReoderHeader():
    print('[' +  bcolors.OKGREEN + 'Recoder' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']')
    headerString = '[' +  bcolors.OKGREEN + 'Recoder' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString

def record_system_sound_loop(sample_rate, device=None, channels=2):
    # List to hold recorded audio data
    audio_data = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def callback(indata, frames, time, status):
        nonlocal audio_data  # Ensure we're modifying the outer scope's audio_data
        if status:
            print(status, file=sys.stderr)
        try:
            audio_data.append(indata.copy())    
        except:
            print(headerString + ' ' +  bcolors.WARNING + 'WARNING_01, The incomming data maybe empty.' + bcolors.ENDC)
    
    # Main loop
    index = 1
    while True:
        # List to hold recorded audio data / clear the list
        # audio_data = []
        start_time = time.time()
        record_time = 60 # Record time before creating a wav file and loop
        print(headerString + ' ' +  bcolors.WARNING + f'Record time is set to {record_time}s' + bcolors.ENDC)

        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback, device=device):
            while True:
                

                # print(bcolors.OKGREEN + f'Record timt: [{round(time.time()-start_time, 0)}/{record_time}]' + bcolors.ENDC)

                if keyboard.is_pressed('c') or time.time()-start_time > record_time: # Cut

                    try:
                        print(headerString + ' ' +  bcolors.BOLD + "Auto-segmenting..." + bcolors.ENDC)
                        # Save the audio data to a WAV file
                        now = datetime.datetime.now()
                        output_file = "./segments/Segment_{}_{}.wav".format(index, now)
                        
                        try:
                            audio_data = np.concatenate(audio_data, axis=0)
                        except:
                            print(headerString + ' ' +  bcolors.FAIL + 'audio_data maybe empty..' + bcolors.ENDC)
                        wavfile.write(output_file, sample_rate, audio_data)
                        print(headerString + ' ' +  f"Saved recording to {output_file}...")    
                        index += 1
                        print(headerString + ' ' +  'Index is raised by 1..')

                        # Reset audio_data !! its a global list
                        audio_data = []
                        break
                    except:
                        print(headerString + ' ' +  bcolors.FAIL + '..ERROR_01_UNKNOWN REASON..' + bcolors.ENDC)
                        break
                    
                if keyboard.is_pressed('q'): # Exit
                    print(headerString + ' ' +  bcolors.BOLD + 'Manual segmenting... Creating wav segment...' + bcolors.ENDC)
                    # Save the audio data to a WAV file
                    now = datetime.datetime.now()
                    output_file = "./segments/Segment_{}_{}.wav".format(index, now)
                    
                    try:
                        audio_data = np.concatenate(audio_data, axis=0)
                    except:
                        print(headerString + ' ' +  bcolors.FAIL + 'audio_data maybe empty..' + bcolors.ENDC)
                        
                    wavfile.write(output_file, sample_rate, audio_data)
                    print(headerString + ' ' +  f"Saved recording to {output_file}...")    
                    
                    print(headerString + ' ' +  bcolors.OKBLUE + 'Exiting...' + bcolors.ENDC)
                    sys.exit() 

def main():

    ### Initializations ###
    sample_rate = 44100  # Sample rate in Hz

    # Check available devices
    devices = sd.query_devices()
    print('====================================================================')
    print(devices)
    print('====================================================================')

    # Device override
    micInOverrideFlag = False
    # print(micInOverrideFlag)
    if micInOverrideFlag == True:
        print(headerString + ' ' +  bcolors.WARNING + 'Device override is activated' + bcolors.ENDC)
        selected_device = 'MacBook Pro麦克风'
        print(headerString + ' ' +  bcolors.WARNING + f'Override target device: {selected_device}.' + bcolors.ENDC)

        for device in devices:
            if selected_device in device['name']:  # Adjust this to match your system audio device's name
                print(headerString + ' ' + bcolors.WARNING + f"Using device: {device['name']} with {device['max_input_channels']} channels" + bcolors.ENDC)
                selected_device = device['index']
                break

    else:
        # Select the appropriate device (e.g., "Stereo Mix" or another system audio device)
        print(headerString + ' ' +  'Microphone input overrideFlag is False')
        selected_device = None
        for device in devices:
            if 'Soundflower' in device['name']:  # Adjust this to match your system audio device's name
                print(headerString + ' ' + bcolors.WARNING + f"Using device: {device['name']} with {device['max_input_channels']} channels" + bcolors.ENDC)
                selected_device = device['index']
                break
    

    if selected_device is None:
        print(headerString + ' ' +  "No suitable device found.")
    else:
        # Check available devices
        devices = sd.query_devices()
        max_channels = sd.query_devices(selected_device)['max_input_channels']
        record_system_sound_loop(sample_rate, device=selected_device, channels=max_channels)


if __name__ == "__main__":
    # Device overridey
    micInOverrideFlag = False

    headerString = PrintReoderHeader()
    main()
    # PrintReoderHeader()