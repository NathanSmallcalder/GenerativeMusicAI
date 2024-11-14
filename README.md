# Generative Music AI 🎵

Welcome to the **Generative Music AI** project! This repository contains a deep learning model designed to generate new audio tracks by learning from a dataset of spectrograms and phase data. 

## Project Overview

The model takes in 40-second snippets of audio data, represented as spectrograms and phase information, and generates new audio outputs. It combines magnitude and phase data to reconstruct the final audio, producing tracks inspired by the training data.

### Key Features:
- Transforms raw audio into spectrogram and phase data for model training.
- Uses a neural network to learn and generate new music snippets.
-  Combines predicted spectrogram and phase data to produce playable audio.

## Dataset

The dataset consists of **1100 songs** processed into 40-second snippets. The data was collected via the Spotify API and downloaded from YouTube. Phase and magnitude data were extracted from these snippets.

| Name        | Artist                     | ID                       | Genre                    | Tempo   | Valence | Liveness | Acousticness | Danceability | Energy | Speechiness | Instrumentalness | Loudness | Key | Mode | Time Signature | File Path                                      | Phase File                                      | Spectrogram File                                |
|-------------|----------------------------|---------------------------|--------------------------|---------|---------|----------|--------------|--------------|--------|-------------|------------------|----------|-----|------|----------------|------------------------------------------------|------------------------------------------------|------------------------------------------------|
| Hourglass   | Catfish and the Bottlemen  | 4hEhOvEz9tulJQXZ7hiqkz    | modern alternative rock  | 129.902 | 0.398   | 0.153    | 0.389        | 0.652        | 0.302  | 0.0328      | 0.000251         | -9.949   | 6   | 1    | 4              | Youtube/Hourglass - Catfish and the Bottlemen.mp3  | Phase/Hourglass - Catfish and the Bottlemen_phase.npz | Spectogram/Hourglass - Catfish and the Bottlemen.npz |
| Purple      | Wunderhorse               | 01WnKRbZWhZaiF5YfOVJoz    | english indie rock       | 141.437 | 0.249   | 0.14     | 0.0502       | 0.27         | 0.683  | 0.0357      | 0.00206          | -5.523   | 11  | 1    | 4              | Youtube/Purple - Wunderhorse.mp3               | Phase/Purple - Wunderhorse_phase.npz           | Spectogram/Purple - Wunderhorse.npz            |
| Teal        | Wunderhorse               | 1jJvNlkbQmtRpG9uIUpiYA    | english indie rock       | 158.714 | 0.375   | 0.0949   | 0.438        | 0.439        | 0.883  | 0.36        | 0.0175           | -7.616   | 9   | 1    | 4              | Youtube/Teal - Wunderhorse.mp3                 | Phase/Teal - Wunderhorse_phase.npz             | Spectogram/Teal - Wunderhorse.npz              |
| Favourite   | Fontaines DC              | 7oG9qhZ0UaQEoUGJJVXh1U    | crank wave               | 76.003  | 0.424   | 0.361    | 0.000114     | 0.353        | 0.875  | 0.0343      | 1.13e-06         | -5.14    | 1   | 0    | 4              | Youtube/Favourite - Fontaines DC.mp3           | Phase/Favourite - Fontaines DC_phase.npz       | Spectogram/Favourite - Fontaines DC.npz        |
| I Love You  | Fontaines DC              | 4N8idxy0W2GDaEosAwPOMg    | crank wave               | 114.032 | 0.375   | 0.0679   | 0.089        | 0.633        | 0.771  | 0.0319      | 0.0              | -7.207   | 4   | 0    | 4              | Youtube/I Love You - Fontaines DC.mp3          | Phase/I Love You - Fontaines DC_phase.npz      | Spectogram/I Love You - Fontaines DC.npz       |


### Note:

This dataset includes copyrighted material and is used strictly for **personal, non-commercial purposes**.

## Project Structure

-------

## Getting Started

## Prerequisites
- Python 3.8+
- TensorFlow
- NumPy
- Matplotlib
- Librosa

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/generative-music-ai.git
   cd generative-music-ai


### Future Improvements
 - Experiment with larger datasets.

### Disclaimer

This project is for educational and personal use only. Generated content may resemble copyrighted material. Ensure you comply with all relevant copyright laws.

### Contact

For questions or collaboration, feel free to reach out:

Name: Nathan Smallcalder
Email: nsmallcalder5@gmail.com
Linkedin: https://www.linkedin.com/in/nathan-smallcalder-b83673209/
