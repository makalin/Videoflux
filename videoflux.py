#!/usr/bin/env python3
import argparse
import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import librosa
import numpy as np
from gtts import gTTS
from tqdm import tqdm  # For progress bar

class Videoflux:
    def __init__(self, input_file):
        self.input_file = input_file
        self.video = VideoFileClip(input_file)
        self.audio = self.video.audio

    def text_to_speech(self, text, output_audio="tts_output.mp3"):
        """Generate speech from text and save as audio file."""
        print("Generating text-to-speech...")
        tts = gTTS(text=text, lang='en')
        tts.save(output_audio)
        return output_audio

    def remove_silence(self, threshold=0.03, min_silence_len=0.5):
        """Remove silent sections from the video with progress feedback."""
        print("Analyzing audio for silence removal...")
        audio_data, sr = librosa.load(self.input_file, sr=self.audio.fps)
        
        # Detect non-silent intervals
        non_silent = librosa.effects.split(audio_data, top_db=threshold * 100)
        
        # Convert intervals to video clips with progress bar
        clips = []
        for start, end in tqdm(non_silent, desc="Processing non-silent segments"):
            t_start = start / sr
            t_end = end / sr
            if (t_end - t_start) >= min_silence_len:  # Ensure minimum length
                clip = self.video.subclip(t_start, t_end)
                clips.append(clip)
        
        # Combine non-silent clips
        final_clip = concatenate_videoclips(clips) if clips else self.video
        return final_clip

    def add_audio(self, audio_file, mix=False, output_file="output_with_audio.mp4"):
        """Add an audio track to the video, optionally mixing with original audio."""
        print("Adding audio to video...")
        new_audio = AudioFileClip(audio_file)
        if mix and self.audio:
            final_audio = CompositeAudioClip([self.audio, new_audio])
        else:
            final_audio = new_audio
        final_video = self.video.set_audio(final_audio)
        final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
        return output_file

    def save(self, output_file="output.mp4"):
        """Save the edited video with progress feedback."""
        print(f"Saving video to {output_file}...")
        self.video.write_videofile(output_file, codec="libx264", audio_codec="aac", verbose=False)

def main():
    parser = argparse.ArgumentParser(description="Videoflux: AI-Powered Video Editing Tool")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-o", "--output", default="output.mp4", help="Output video file")
    parser.add_argument("--tts", help="Text to convert to speech and add to video")
    parser.add_argument("--remove-silence", action="store_true", help="Remove silent sections")
    parser.add_argument("--mix-audio", action="store_true", help="Mix TTS with original audio instead of replacing it")
    
    args = parser.parse_args()

    # Initialize Videoflux
    editor = Videoflux(args.input)

    # Process text-to-speech if provided
    if args.tts:
        tts_file = editor.text_to_speech(args.tts)
        editor.add_audio(tts_file, mix=args.mix_audio)
        os.remove(tts_file)  # Clean up temporary file

    # Remove silence if requested
    if args.remove_silence:
        editor.video = editor.remove_silence()

    # Save the final video
    editor.save(args.output)
    print("Editing complete!")

if __name__ == "__main__":
    main()