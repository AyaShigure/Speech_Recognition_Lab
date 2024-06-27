import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import keyboard

def record_system_sound(sample_rate, output_file, device=None):
    # List to hold recorded audio data
    audio_data = []

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_data.append(indata.copy())

    # Start the recording
    print("Recording... Press 'q' to stop.")
    with sd.InputStream(samplerate=sample_rate, channels=2, callback=callback, device=device):
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

    # Select the appropriate device
    selected_device = None
    for device in devices:
        if device['max_input_channels'] >= 2:  # Ensure it supports at least 2 channels
            print(f"Using device: {device['name']}")
            selected_device = device['index']
            break

            
            
    if selected_device is None:
        print("No suitable device found.")
    else:
        record_system_sound(sample_rate, output_file, device=selected_device)
