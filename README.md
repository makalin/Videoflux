# Videoflux

![Videoflux Logo](videoflux_logo.png)

**Videoflux** is a simple, command-line video editing tool powered by AI. It leverages text-to-speech generation and audio analysis to automate tasks like adding voiceovers and removing silent sections from videos. Built with Python, it’s lightweight, practical, and easy to extend.

## Features
- **Text-to-Speech (TTS)**: Convert text into speech and overlay it onto your video using Google TTS.
- **Silence Removal**: Automatically detect and cut out silent portions of the video.
- **Audio Mixing**: Optionally mix TTS with the original audio instead of replacing it.
- **Progress Feedback**: Visual progress bar for long operations like silence removal.

## Installation

### Prerequisites
- Python 3.x
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system PATH

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/makalin/videoflux.git
   cd videoflux
   ```
2. Install dependencies:
   ```bash
   pip install moviepy librosa numpy gtts tqdm
   ```
3. Ensure FFmpeg is installed:
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt-get install ffmpeg`
   - Windows: Download from [FFmpeg’s site](https://ffmpeg.org/download.html) and add to PATH.

## Usage

Run the tool via the command line with `videoflux.py`. Here are some examples:

### Basic Save
Save a video without changes:
```bash
python videoflux.py input_video.mp4 -o output.mp4
```

### Add Text-to-Speech
Add an AI-generated voiceover:
```bash
python videoflux.py input_video.mp4 --tts "Welcome to Videoflux" -o output.mp4
```

### Remove Silence
Cut out silent sections:
```bash
python videoflux.py input_video.mp4 --remove-silence -o output.mp4
```

### Combine Features
Mix TTS with original audio and remove silence:
```bash
python videoflux.py input_video.mp4 --tts "Overlay this" --mix-audio --remove-silence -o output.mp4
```

### Options
- `-o, --output`: Specify output file (default: `output.mp4`).
- `--tts`: Text to convert to speech.
- `--remove-silence`: Remove silent sections.
- `--mix-audio`: Mix TTS with original audio instead of replacing it.

## How It Works
- **TTS**: Uses `gTTS` to generate speech, saved as a temporary audio file and added to the video.
- **Silence Removal**: Analyzes audio with `librosa` to detect non-silent segments, then stitches them together using `moviepy`.
- **Video Processing**: Relies on `moviepy` and `ffmpeg` for editing and rendering.

## Contributing
Contributions are welcome! Here’s how to get started:
1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to your fork: `git push origin feature/your-feature`.
5. Open a pull request.

Feel free to suggest new features like cropping, speed adjustment, or advanced audio filters!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [moviepy](https://zulko.github.io/moviepy/), [librosa](https://librosa.org/), [gTTS](https://github.com/pndurette/gTTS), and [tqdm](https://github.com/tqdm/tqdm).
