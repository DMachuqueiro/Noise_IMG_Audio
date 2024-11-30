from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import pesq
import soundfile as sf

import scipy.signal

#Calculates PSNR and SSIM between the original and noisy images.
def calculate_metrics(original_path, noisy_path):

    original = np.array(Image.open(original_path).convert("RGB"))
    noisy = np.array(Image.open(noisy_path).convert("RGB"))
    
    # PSNR
    psnr_value = psnr(original, noisy)
    
    # SSIM (usar channel_axis=-1 para imagens RGB)
    ssim_value = ssim(original, noisy, channel_axis=-1, win_size=None)
    
    return psnr_value, ssim_value




#Calculate the PESQ score for a reference and degraded audio.
def calculate_pesq_score(reference_audio_path, degraded_audio_path, sample_rate=16000):
    # Load the reference and degraded audio files
    ref_data, ref_samplerate = sf.read(reference_audio_path)
    deg_data, deg_samplerate = sf.read(degraded_audio_path)

    # Ensure both audios have the same sample rate
    if ref_samplerate != sample_rate or deg_samplerate != sample_rate:
        raise ValueError(f"Both audio files must have a sample rate of {sample_rate} Hz.")

    # Calculate the PESQ score
    score = pesq.pesq(sample_rate, ref_data, deg_data, 'wb')
    return score



#Puts both audio in Mono and 16000 hz sample rate for the PESQ method
def resample_audio(input_path, output_path, target_samplerate=16000):
    try:
        # Load the audio file
        data, samplerate = sf.read(input_path)
        
        # Convert to mono if necessary
        if len(data.shape) > 1:  # Check if the audio is stereo or multi-channel
            data = np.mean(data, axis=1)  # Average channels to create mono audio

        # Resample if the sample rate differs from the target
        if samplerate != target_samplerate:
            # Calculate the resampling ratio
            resample_ratio = target_samplerate / samplerate
            
            # Resample the audio
            resampled_data = scipy.signal.resample(data, int(len(data) * resample_ratio))
            
            # Write the resampled audio to the output file
            sf.write(output_path, resampled_data, target_samplerate)
        else:
            # If the sample rate is already the target, just save as mono
            sf.write(output_path, data, samplerate)
    except Exception as e:
        raise RuntimeError(f"Error resampling audio: {e}")