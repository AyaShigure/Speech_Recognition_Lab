# Notes:
# 1. This script could record system output audio via sunflower(2ch)
# 2. To listen to the sound via headset, while recording the system sound: Multi-output must be set in 'Audio MIDI Setup' app
# 3. Press 'q' to quit and save

# ToDo:

# 1. Create folder for each presentation automatically, containing 1)Raw record, 2)All Segments
# 2. Calculate transscript for both 1)Raw record and 2)All segments
# 3. Real-time with segments? (But need gpt-api then)

# 4. Start recording (with py script)-> Press key to cut and create project folder -> Loop and record till key press 
#                                                                  \-> Calculate the transscript with another script(at jupyter lab) -> GPT


import sys
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import keyboard

def record_system_sound(sample_rate, output_file, device=None, channels=2):
    # List to hold recorded audio data
    audio_data = []

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_data.append(indata.copy())

    # Start the recording
    print("Recording... Press 'q' to stop.")
    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback, device=device):
        while True:
            if keyboard.is_pressed('q'):
                print("Recording stopped.")
                break

    # Convert list to numpy array
    audio_data = np.concatenate(audio_data, axis=0)

    # Save the audio data to a WAV file
    wavfile.write(output_file, sample_rate, audio_data)
    print(f"Saved recording to {output_file}")

if __name__ == "__main__":
    sample_rate = 44100  # Sample rate in Hz
    output_file = "system_sound_output.wav"  # Output file name

    # Check available devices
    devices = sd.query_devices()
    print(devices)

    # Select the appropriate device (e.g., "Stereo Mix" or another system audio device)
    selected_device = None
    for device in devices:
        if 'Soundflower' in device['name']:  # Adjust this to match your system audio device's name
            print(f"Using device: {device['name']} with {device['max_input_channels']} channels")
            selected_device = device['index']
            break

            
    # Device override
    # selected_device = 9
    
    if selected_device is None:
        print("No suitable device found.")
    else:
        max_channels = sd.query_devices(selected_device)['max_input_channels']
        record_system_sound(sample_rate, output_file, device=selected_device, channels=max_channels)
