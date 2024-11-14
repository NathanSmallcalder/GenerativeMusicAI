import os
import yt_dlp
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydub import AudioSegment
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import random

def search_youtube(query, max_results=1):
    """
    Search for YouTube videos based on a query.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'noplaylist': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
        return results.get('entries', [])

def download_audio(video_url, download_path, song_name, song_artist):
    """
    Download the audio from a YouTube video and save it as an MP3.
    """
    safe_song_name = "".join([c for c in song_name if c.isalnum() or c in (' ', '-', '_')])
    safe_song_artist = "".join([c for c in song_artist if c.isalnum() or c in (' ', '-', '_')])
    filename = f"{safe_song_name} - {safe_song_artist}"
    output_path = os.path.join(download_path, filename)
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'ffmpeg_location': '/usr/bin/ffmpeg', 
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            print(f"Downloaded: {output_path}")
        except Exception as e:
            print(f"Error downloading {video_url}: {e}")

def load_downloaded_titles(download_path):
    """
    Load previously downloaded titles to avoid duplicates.
    """
    titles = set()
    for file in os.listdir(download_path):
        if file.endswith('.mp3'):
            title = os.path.splitext(file)[0]
            titles.add(title)
    return titles

def process_song(song, download_path, downloaded_titles, lock):
    """
    Process each song by searching and downloading the top search result.
    """
    song_name = song['name']
    song_artist = song['artist']
    search_query = f"{song_name} {song_artist}"
    print(f"Searching for: {search_query}")
    
    # Get search results
    videos = search_youtube(search_query)
    
    if not videos:
        print(f"No results found for: {search_query}")
        return
    
    video_url = videos[0]['url']
    print(f"Processing video URL: {video_url}")
    
    # Thread-safe check and download
    with lock:
        if f"{song_name} - {song_artist}" not in downloaded_titles:
            downloaded_titles.add(f"{song_name} - {song_artist}")
            download_audio(video_url, download_path, song_name, song_artist)

def install_playlist(playlist):
    """
    Install a playlist by processing each song using threading.
    """
    download_path = 'Youtube'
    os.makedirs(download_path, exist_ok=True)
    
    downloaded_titles = load_downloaded_titles(download_path)
    lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = []
        for song in playlist:
            futures.append(executor.submit(process_song, song, download_path, downloaded_titles, lock))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")
    
    print("All songs processed.")

def convert_mp3_to_wav(mp3_path, wav_path):
    """
    Converts mp3 to wav file format
    """
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format='wav')
        print(f"Converted {mp3_path} to {wav_path}")
    except Exception as e:
        print(f"Error converting {mp3_path}: {e}")

def generate_spectrogram_npz(wav_file, npz_file):
    """
    Generates a spectrogram from a WAV file and saves it as an NPZ file.
    
    Parameters:
        wav_file (str): Path to the input WAV file.
        npz_file (str): Path where the NPZ file will be saved.
    """
    y, sr = librosa.load(wav_file, sr=None)
    D = librosa.stft(y)
    magnitude = np.abs(D)
    phase = np.angle(D)
    S_db = librosa.amplitude_to_db(magnitude, ref=np.max)
    
    # Save magnitude, phase, and spectrogram data
    np.savez(npz_file, magnitude=magnitude, phase=phase, S_db=S_db, sr=sr)
    print(f"Spectrogram data saved to {npz_file}")

def generate_phase_spectrogram_npz(wav_file, npz_file):
    """
    Generates phase spectrogram data from a WAV file and saves it as an NPZ file.
    
    Parameters:
        wav_file (str): Path to the input WAV file.
        npz_file (str): Path where the NPZ file will be saved.
    """
    y, sr = librosa.load(wav_file, sr=None)
    D = librosa.stft(y)
    phase = np.angle(D)
    
    # Save phase data
    np.savez(npz_file, phase=phase, sr=sr)
    print(f"Phase data saved to {npz_file}")

def trim_audio(input_file, output_file, duration=40):
    """
    Trims the audio to a random 40 seconds within the audio file.
    """
    try:
        audio = AudioSegment.from_mp3(input_file)
        audio_length = len(audio)
        print(f"Processing '{input_file}': length is {audio_length / 1000:.2f} seconds.")
        max_start_time = audio_length - (duration * 1000)

        if max_start_time < 0:
            raise ValueError("Audio is shorter than the specified duration.")

        random_start_time = random.randint(0, max_start_time)
        end_time = random_start_time + duration * 1000
        trimmed_audio = audio[random_start_time:end_time]
        trimmed_audio.export(output_file, format="wav")
        print(f"Trimmed audio saved to '{output_file}', starting at {random_start_time // 1000} seconds.")
    
    except Exception as e:
        print(f"Error processing '{input_file}': {e}")

def reconstruct_audio(spectrogram, phase, sr, output_wav_file):
    """
    Reconstructs audio from magnitude spectrogram and phase data.
    
    Parameters:
        spectrogram (np.ndarray): The magnitude spectrogram.
        phase (np.ndarray): The phase data.
        sr (int): Sample rate of the audio.
        output_wav_file (str): Path to save the reconstructed audio.
    """
    # Ensure shapes match
    if spectrogram.shape != phase.shape:
        raise ValueError("Spectrogram and phase shapes do not match.")

    # Reconstruct the complex spectrogram
    complex_spectrogram = spectrogram * np.exp(1j * phase)

    # Perform ISTFT to get the time-domain signal
    reconstructed_audio = librosa.istft(complex_spectrogram)

    # Save the reconstructed audio as a WAV file
    sf.write(output_wav_file, reconstructed_audio, sr)
    print(f"Audio reconstructed and saved to {output_wav_file}")
