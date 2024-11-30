import numpy as np
from PIL import Image
import soundfile as sf

#Add gaussian noise to an image and returns Noisy PIL Image
def add_gaussian_noise(image_path, mean=0, stddev=25):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    
    # Generate Gaussian noise
    noise = np.random.normal(mean, stddev, image_array.shape).astype(np.float32)
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_image)




#Add noise to an audio file and save the noisy audio to a file
def add_noise_to_audio(input_audio_path, noise_level=50):
    
    # Load the audio file
    data, samplerate = sf.read(input_audio_path)

    # Ensure noise level is between 0 and 100
    noise_level = max(0, min(noise_level, 100))

    # Calculate the standard deviation of the noise based on the noise level
    noise_std = (noise_level / 100) * np.std(data)

    # Generate white noise
    noise = np.random.normal(0, noise_std, data.shape)

    # Add noise to the audio
    noisy_data = data + noise

    # Ensure the noisy audio stays in the valid range [-1, 1]
    noisy_data = np.clip(noisy_data, -1, 1)

    # Save the noisy audio to a file
    output_audio_path = "output/noisy_audio.wav"
    sf.write(output_audio_path, noisy_data, samplerate)

    return output_audio_path
