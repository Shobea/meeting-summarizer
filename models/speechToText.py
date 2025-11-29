import whisper
import torch
import warnings
from datetime import datetime
import os
warnings.filterwarnings("ignore")


class SpeechToText:
    def __init__(self, model_size="base"):
        #load whisper model for converting speech to text
        print(f"Loading Whisper {model_size} model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        #show gpu info if using cuda
        if self.device == "cuda":
            print(f"Using GPU: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB)")
        
        self.model = whisper.load_model(model_size, device=self.device)
        print(f"Model loaded on {self.device}")
    
    def transcribe(self, audio_path, language=None, task="transcribe"):
        #convert audio file to text
        #audio_path: path to audio file
        #language: language code like 'en' or 'es', leave as None to auto-detect
        #task: "transcribe" for original language, "translate" for English translation
        print(f"Transcribing {audio_path}...")
        
        #transcribe with whisper
        result = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            fp16=(self.device == "cuda")
        )
        
        return {
            "text": result["text"],
            "language": result["language"],
            "segments": result["segments"]
        }
    
    def transcribe_with_timestamps(self, audio_path, language=None):
        #get transcription with time stamps for each part
        #returns list of text segments with start and end times
        result = self.transcribe(audio_path, language)
        
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })
        
        return segments
    
    def save_transcription_to_file(self, audio_path, language=None, output_dir="transcriptions"):
        #transcribe audio and save results to a text file with timestamp
        #creates a file with date, time, detected language, and full transcription
        #if language is Tagalog, creates both original and English translation
        #
        #language: specify language for transcription (e.g., 'tl' for Tagalog), None for auto-detect
        
        #create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        #get transcription
        result = self.transcribe(audio_path, language)
        detected_language = result['language']
        
        #get current date and time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        filename_timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        #create filename based on audio file name and timestamp
        audio_basename = os.path.splitext(os.path.basename(audio_path))[0]
        
        #check if language is Tagalog
        needs_translation = detected_language == 'tl'
        
        #save original transcription
        output_filename = f"{audio_basename}_{filename_timestamp}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("SPEECH TO TEXT TRANSCRIPTION (ORIGINAL)\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {date_str}\n")
            f.write(f"Time: {time_str}\n")
            f.write(f"Audio File: {audio_path}\n")
            f.write(f"Detected Language: {detected_language}\n")
            f.write("\n" + "="*60 + "\n")
            f.write("TRANSCRIPTION\n")
            f.write("="*60 + "\n\n")
            f.write(result['text'])
        
        print(f"\nOriginal transcription saved to: {output_path}")
        
        #if Tagalog detected, create English translation
        if needs_translation:
            print(f"\nDetected Tagalog. Creating English translation...")
            translation_result = self.transcribe(audio_path, language='tl', task="translate")
            
            #save translation
            translation_filename = f"{audio_basename}_{filename_timestamp}_EN.txt"
            translation_path = os.path.join(output_dir, translation_filename)
            
            with open(translation_path, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("SPEECH TO TEXT TRANSCRIPTION (ENGLISH TRANSLATION)\n")
                f.write("="*60 + "\n\n")
                f.write(f"Date: {date_str}\n")
                f.write(f"Time: {time_str}\n")
                f.write(f"Audio File: {audio_path}\n")
                f.write(f"Original Language: {detected_language}\n")
                f.write(f"Translated to: English\n")
                f.write("\n" + "="*60 + "\n")
                f.write("ENGLISH TRANSLATION\n")
                f.write("="*60 + "\n\n")
                f.write(translation_result['text'])
            
            print(f"English translation saved to: {translation_path}")
            return {"original": output_path, "translation": translation_path}
        
        return {"original": output_path}


if __name__ == "__main__":

    #example usage
    # model_size options: tiny (fast), base (balanced), small, medium, large (best quality)
    stt = SpeechToText(model_size="base")
    
    #transcribe and save to file
    output_files = stt.save_transcription_to_file("test/testing.mp3")
    
    if "translation" in output_files:
        print(f"\n  Done! Created 2 files:")
        print(f"  - Original: {output_files['original']}")
        print(f"  - English Translation: {output_files['translation']}")
    else:
        print(f"\n Done! Check '{output_files['original']}' for results.")

