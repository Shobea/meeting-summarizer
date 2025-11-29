#text summarization using pretrained models like bart or t5

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import warnings
import os
from datetime import datetime
warnings.filterwarnings("ignore")


class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        #load summarization model
        #model_name options: facebook/bart-large-cnn (good for news), google/pegasus-xsum (extreme summarization), t5-base (versatile)
        print(f"Loading summarization model: {model_name}...")
        self.device = 0 if torch.cuda.is_available() else -1
        
        #load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        if self.device == 0:
            self.model = self.model.to("cuda")
            print("Model loaded on GPU")
        else:
            print("Model loaded on CPU")
        
        #create pipeline
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )
    
    def summarize(self, text, max_length=150, min_length=30, 
                  do_sample=False, num_beams=4):
        #summarize the given text
        #max_length: max words in summary
        #min_length: min words in summary
        #do_sample: use sampling for more creative summaries
        #num_beams: higher number = better quality but slower
        if not text or len(text.strip()) == 0:
            return ""
        
        #split long texts into chunks if needed
        max_input_length = 1024
        token_count = len(self.tokenizer.encode(text))
        
        if token_count > max_input_length:
            print(f"Text is long ({token_count} tokens). Processing in chunks...")
            return self._summarize_long_text(text, max_length, min_length, 
                                            do_sample, num_beams)
        
        #summarize
        result = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=do_sample,
            num_beams=num_beams,
            early_stopping=True
        )
        
        return result[0]["summary_text"]
    
    def _summarize_long_text(self, text, max_length, min_length, 
                            do_sample, num_beams):
        #summarize long texts by breaking them into smaller chunks
        
        #split by sentences or paragraphs
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            test_chunk = current_chunk + sentence + ". "
            if len(self.tokenizer.encode(test_chunk)) > 900:  #leave buffer
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + ". "
            else:
                current_chunk = test_chunk
        
        if current_chunk:
            chunks.append(current_chunk)
        
        #summarize each chunk
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}...")
            summary = self.summarizer(
                chunk,
                max_length=max_length // len(chunks) + 50,
                min_length=min_length // len(chunks),
                do_sample=do_sample,
                num_beams=num_beams
            )
            summaries.append(summary[0]["summary_text"])
        
        #combine summaries
        combined = " ".join(summaries)
        
        #if combined is still too long, summarize again
        if len(self.tokenizer.encode(combined)) > 900:
            final = self.summarizer(
                combined,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
                num_beams=num_beams
            )
            return final[0]["summary_text"]
        
        return combined
    
    def batch_summarize(self, texts, max_length=150, min_length=30):
        #summarize multiple texts at once
        #texts: list of text strings to summarize
        #returns: list of summaries
        results = self.summarizer(
            texts,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            num_beams=4
        )
        
        return [r["summary_text"] for r in results]
    
    def read_transcription_file(self, file_path):
        #read a transcription file and extract the actual transcription text
        #skips the metadata headers and returns just the transcribed content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        #find the transcription section (after the last "=====" line)
        lines = content.split('\n')
        transcription_lines = []
        found_transcription = False
        
        for i, line in enumerate(lines):
            if "TRANSCRIPTION" in line or "ENGLISH TRANSLATION" in line:
                found_transcription = True
                continue
            if found_transcription and line.strip() == "=" * 60:
                #skip the separator line after TRANSCRIPTION header
                continue
            if found_transcription and line.strip():
                transcription_lines.append(line)
        
        transcription_text = '\n'.join(transcription_lines).strip()
        return transcription_text
    
    def summarize_transcription_file(self, file_path, max_length=150, min_length=30, 
                                     save_summary=True, output_dir="summaries"):
        #read a transcription file, summarize it, and optionally save the summary
        #file_path: path to the transcription file
        #save_summary: if True, saves the summary to a file
        #output_dir: directory to save summary files
        
        print(f"\nReading transcription from: {file_path}")
        transcription_text = self.read_transcription_file(file_path)
        
        if not transcription_text or len(transcription_text.strip()) < 10:
            print("Transcription is too short to summarize.")
            return ""
        
        print(f"Transcription length: {len(transcription_text.split())} words")
        print("Generating summary...")
        
        summary = self.summarize(transcription_text, max_length, min_length)
        
        if save_summary:
            #create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            #create summary filename based on original file
            basename = os.path.basename(file_path)
            summary_filename = basename.replace('.txt', '_SUMMARY.txt')
            summary_path = os.path.join(output_dir, summary_filename)
            
            #get metadata from original file
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            
            #write summary to file
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("TEXT SUMMARY\n")
                f.write("="*60 + "\n\n")
                f.write(f"Summary Generated: {date_str} {time_str}\n")
                f.write(f"Source File: {file_path}\n")
                f.write(f"Original Length: {len(transcription_text.split())} words\n")
                f.write(f"Summary Length: {len(summary.split())} words\n")
                f.write("\n" + "="*60 + "\n")
                f.write("SUMMARY\n")
                f.write("="*60 + "\n\n")
                f.write(summary)
            
            print(f"Summary saved to: {summary_path}")
        
        return summary
    
    def summarize_all_combined(self, transcription_dir="transcriptions", 
                              output_dir="summaries", max_length=200, min_length=50):
        #combine all transcription files and create ONE master summary
        #transcription_dir: directory containing transcription files
        #output_dir: directory to save the combined summary
        
        if not os.path.exists(transcription_dir):
            print(f"Error: Directory '{transcription_dir}' not found.")
            return ""
        
        #get all .txt files (excluding _EN files to avoid duplicates)
        txt_files = [f for f in os.listdir(transcription_dir) 
                    if f.endswith('.txt') and not f.endswith('_EN.txt')]
        
        if not txt_files:
            print(f"No transcription files found in '{transcription_dir}'")
            return ""
        
        print(f"\nFound {len(txt_files)} transcription file(s).")
        print("Combining all transcriptions into one master summary...\n")
        
        #read and combine all transcriptions
        all_transcriptions = []
        file_list = []
        
        for txt_file in sorted(txt_files):
            file_path = os.path.join(transcription_dir, txt_file)
            try:
                transcription_text = self.read_transcription_file(file_path)
                if transcription_text and len(transcription_text.strip()) > 10:
                    all_transcriptions.append(transcription_text)
                    file_list.append(txt_file)
                    print(f"✓ Added: {txt_file} ({len(transcription_text.split())} words)")
            except Exception as e:
                print(f"✗ Error reading {txt_file}: {e}")
        
        if not all_transcriptions:
            print("No valid transcriptions found to summarize.")
            return ""
        
        #combine all texts
        combined_text = "\n\n".join(all_transcriptions)
        total_words = len(combined_text.split())
        
        print(f"\n{'='*60}")
        print(f"Combined {len(all_transcriptions)} transcription(s)")
        print(f"Total length: {total_words} words")
        print("Generating master summary...")
        print(f"{'='*60}\n")
        
        #generate summary
        summary = self.summarize(combined_text, max_length, min_length)
        
        #save master summary
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        summary_filename = f"MASTER_SUMMARY_{timestamp}.txt"
        summary_path = os.path.join(output_dir, summary_filename)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("MASTER SUMMARY - ALL TRANSCRIPTIONS COMBINED\n")
            f.write("="*60 + "\n\n")
            f.write(f"Summary Generated: {date_str} {time_str}\n")
            f.write(f"Source Directory: {transcription_dir}\n")
            f.write(f"Number of Files Combined: {len(all_transcriptions)}\n")
            f.write(f"Total Original Length: {total_words} words\n")
            f.write(f"Summary Length: {len(summary.split())} words\n")
            f.write("\n" + "="*60 + "\n")
            f.write("FILES INCLUDED\n")
            f.write("="*60 + "\n")
            for i, filename in enumerate(file_list, 1):
                f.write(f"{i}. {filename}\n")
            f.write("\n" + "="*60 + "\n")
            f.write("MASTER SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(summary)
        
        print(f"\n✓ Master summary saved to: {summary_path}")
        print(f"  Combined {len(all_transcriptions)} files into 1 summary\n")
        
        return summary
    
    def summarize_all_in_directory(self, transcription_dir="transcriptions", 
                                   output_dir="summaries", max_length=150, min_length=30):
        #summarize each transcription file individually (separate summaries)
        #transcription_dir: directory containing transcription files
        #output_dir: directory to save summaries
        
        if not os.path.exists(transcription_dir):
            print(f"Error: Directory '{transcription_dir}' not found.")
            return []
        
        #get all .txt files (excluding _EN files to avoid summarizing translations separately)
        txt_files = [f for f in os.listdir(transcription_dir) 
                    if f.endswith('.txt') and not f.endswith('_EN.txt')]
        
        if not txt_files:
            print(f"No transcription files found in '{transcription_dir}'")
            return []
        
        print(f"\nFound {len(txt_files)} transcription file(s) to summarize.")
        
        summaries = []
        for txt_file in txt_files:
            file_path = os.path.join(transcription_dir, txt_file)
            try:
                summary = self.summarize_transcription_file(
                    file_path, 
                    max_length=max_length, 
                    min_length=min_length,
                    save_summary=True,
                    output_dir=output_dir
                )
                summaries.append({
                    "file": txt_file,
                    "summary": summary
                })
                print(f"✓ Completed: {txt_file}\n")
            except Exception as e:
                print(f"✗ Error processing {txt_file}: {e}\n")
        
        print(f"\n{'='*60}")
        print(f"Summarization complete! {len(summaries)}/{len(txt_files)} files processed.")
        print(f"{'='*60}")
        
        return summaries


def display_menu():
    #display the main menu options
    print("\n" + "="*60)
    print("TEXT SUMMARIZER - MAIN MENU")
    print("="*60)
    print("\n1. Combine all transcriptions into ONE master summary (RECOMMENDED)")
    print("2. Create INDIVIDUAL summaries for each transcription file")
    print("3. Summarize ONE specific transcription file")
    print("4. Summarize plain text directly (manual input)")
    print("5. Exit")
    print("\n" + "="*60)


def get_user_input(prompt, default=None):
    #get user input with optional default value
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def get_int_input(prompt, default):
    #get integer input with default value
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("Please enter a valid number.")


def list_transcription_files(directory="transcriptions"):
    #list available transcription files
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return []
    
    txt_files = [f for f in os.listdir(directory) 
                if f.endswith('.txt') and not f.endswith('_EN.txt')]
    return txt_files


if __name__ == "__main__":
    print("\n" + "="*60)
    print("WELCOME TO TEXT SUMMARIZER")
    print("="*60)
    print("\nInitializing model... This may take a moment.")
    
    summarizer = TextSummarizer()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            #option 1: combine all transcriptions into ONE master summary
            print("\n" + "="*60)
            print("OPTION 1: Create Master Summary (Combined)")
            print("="*60)
            
            transcription_dir = get_user_input("Transcription directory", "transcriptions")
            output_dir = get_user_input("Output directory", "summaries")
            max_length = get_int_input("Maximum summary length (words)", 200)
            min_length = get_int_input("Minimum summary length (words)", 50)
            
            print("\nProcessing...")
            master_summary = summarizer.summarize_all_combined(
                transcription_dir=transcription_dir,
                output_dir=output_dir,
                max_length=max_length,
                min_length=min_length
            )
            
            if master_summary:
                print(f"\nMaster Summary:\n{'-'*60}\n{master_summary}\n{'-'*60}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            #option 2: create INDIVIDUAL summaries for each file
            print("\n" + "="*60)
            print("OPTION 2: Create Individual Summaries")
            print("="*60)
            
            transcription_dir = get_user_input("Transcription directory", "transcriptions")
            output_dir = get_user_input("Output directory", "summaries")
            max_length = get_int_input("Maximum summary length (words)", 150)
            min_length = get_int_input("Minimum summary length (words)", 30)
            
            print("\nProcessing...")
            summaries = summarizer.summarize_all_in_directory(
                transcription_dir=transcription_dir,
                output_dir=output_dir,
                max_length=max_length,
                min_length=min_length
            )
            
            if summaries:
                print(f"\n✓ Successfully created {len(summaries)} summaries!")
            
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            #option 3: summarize ONE specific transcription file
            print("\n" + "="*60)
            print("OPTION 3: Summarize Specific File")
            print("="*60)
            
            transcription_dir = "transcriptions"
            
            #list available files from transcriptions folder
            txt_files = list_transcription_files(transcription_dir)
            
            if not txt_files:
                print(f"\nNo transcription files found in '{transcription_dir}' folder.")
                print("Please make sure you have .txt files in the transcriptions directory.")
                input("\nPress Enter to continue...")
                continue
            
            print(f"\nFound {len(txt_files)} file(s) in '{transcription_dir}' folder:")
            print("-" * 60)
            for i, file in enumerate(txt_files, 1):
                print(f"  {i}. {file}")
            print("-" * 60)
            
            file_choice = input("\nEnter file number (1-{}): ".format(len(txt_files))).strip()
            
            #check if user entered a valid number
            try:
                file_idx = int(file_choice) - 1
                if 0 <= file_idx < len(txt_files):
                    file_path = os.path.join(transcription_dir, txt_files[file_idx])
                    print(f"\nSelected: {txt_files[file_idx]}")
                else:
                    print(f"\n✗ Invalid file number. Please enter a number between 1 and {len(txt_files)}.")
                    input("\nPress Enter to continue...")
                    continue
            except ValueError:
                print("\n✗ Invalid input. Please enter a number.")
                input("\nPress Enter to continue...")
                continue
            
            print("\nGenerating summary...")
            try:
                summary = summarizer.summarize_transcription_file(
                    file_path,
                    max_length=150,
                    min_length=30,
                    save_summary=True,
                    output_dir="summaries"
                )
                
                if summary:
                    print(f"\nSummary:\n{'-'*60}\n{summary}\n{'-'*60}")
            except Exception as e:
                print(f"\n✗ Error: {e}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            #option 4: summarize plain text directly
            print("\n" + "="*60)
            print("OPTION 4: Summarize Plain Text")
            print("="*60)
            print("\nEnter or paste your text below.")
            print("When done, type 'END' on a new line and press Enter.\n")
            
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            
            text = "\n".join(lines)
            
            if not text.strip():
                print("\nNo text entered.")
                input("\nPress Enter to continue...")
                continue
            
            max_length = get_int_input("Maximum summary length (words)", 150)
            min_length = get_int_input("Minimum summary length (words)", 30)
            
            save_option = input("Save summary to file? (y/n) [n]: ").strip().lower()
            
            print("\nProcessing...")
            summary = summarizer.summarize(text, max_length=max_length, min_length=min_length)
            
            print(f"\nSummary:\n{'-'*60}\n{summary}\n{'-'*60}")
            
            if save_option == 'y':
                output_dir = get_user_input("Output directory", "summaries")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"text_summary_{timestamp}.txt"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("TEXT SUMMARY\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Original Length: {len(text.split())} words\n")
                    f.write(f"Summary Length: {len(summary.split())} words\n")
                    f.write("\n" + "="*60 + "\n")
                    f.write("SUMMARY\n")
                    f.write("="*60 + "\n\n")
                    f.write(summary)
                
                print(f"\n✓ Summary saved to: {filepath}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            #exit
            print("\n" + "="*60)
            print("Thank you for using Text Summarizer!")
            print("="*60 + "\n")
            break
        
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 5.")
            input("\nPress Enter to continue...")

