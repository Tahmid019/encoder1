from scipy.ndimage.morphology import binary_dilation
from encoder1.hparams import *
from pathlib import Path
from typing import Optional, Union
import numpy as np
import webrtcvad
import librosa
import struct

int16_max = (2**15) - 1

def process_wav(fpath_or_wav: Union[str, Path, np.ndarray], source_sr: Optional[int]=None):
    """
    Resampling the Waveform to meet the hyperparameters.
    
    fpath_or_wav -> using typing ton specify the type of input and Union for or operation
    source_sr -> Optional is same as Union
    
    sampling rate shall automatically be detected eighterwise
    """
    
    #load wav
    if isinstance(fpath_or_wav, str) or isinstance(fpath_or_wav, Path):
        wav, source_sr = librosa.load(str(fpath_or_wav), sr=None)
    else:
        wav = fpath_or_wav
    
    #resample
    if source_sr is not None:
        wav = librosa.resample(wav, orig_sr=source_sr, target_sr=sampling_rate)
    
    #normalize volumes + shorten long silences
    wav = normalize_volume(wav, audio_norm_target_dBFS, increase_only=True)
    wav = trim_long_silences(wav)
    
    return wav

def wav_to_mel_spectrogram(wav):
    """
    produces a mel-spec (not log) for encoder
    """
    
    frames = librosa.feature.melspectrogram(
        y = wav,
        sr = sampling_rate,
        n_fft = int(sampling_rate * mel_window_length / 100),
        hop_length = int(sampling_rate * mel_window_step / 1000),
        n_mels = mel_n_channels      
    )
    
    return frames.astype(np.float32).T

def trim_long_silences(wav):
    """
    thrsh - VAD params in params.py
    
    """
    
    #voice detection window size
    samples_per_window = (vad_window_length * sampling_rate) // 1000
    
    #trim ends
    wav = wav[:len(wav) - (len(wav) % samples_per_window)]
    
    #float -> 16_bit mono pcm
    pcm_wav = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))
    
    #vad - voice activation detection
    voice_flags = []
    vad = webrtcvad.Wav(mode=3)
    for window_start in range(0, len(wav), samples_per_window):
        window_end = window_start + samples_per_window
        voice_flags.append(vad.is_speech(pcm_wav[window_start * 2: window_end * 2], sample_rate=sampling_rate))

    
    voice_flags = np.array(voice_flags)
    
    #msmoothing
    def moving_average(array, width):
        array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))
        ret = np.cumsum(array_padded, dtype=float) 
        ret[width:] = ret[width:] - ret[:-width]
        return ret[width - 1:] / width
    
    audio_mask = moving_average(voice_flags, vad_moving_average_width)
    audio_mask = np.round(audio_mask, samples_per_window)
    
    return wav(audio_mask == True)

def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    if increase_only and decrease_only:
        raise ValueError("Both increase oonly and decrease only are set")
    rms = np.sqrt(np.mean((wav * int16_max) ** 2))
    wave_dBFS = 20 * np.log10(rms / int16_max)
    dBFS_change = target_dBFS - wave_dBFS
    if dBFS_change < 0 and increase_only or dBFS_change > 0 and decrease_only:
        return wav
    return wav * (10 ** (dBFS_change / 20))
