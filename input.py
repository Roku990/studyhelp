import PyPDF2

PDF_PATH =  r"C:\Users\asus\Desktop\Bonn uni D\SoSe 25\MCI\MCI Buch 2025.pdf"

#for PDF
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

#Using spaCy for smart splitting
import spacy
nlp = spacy.load("en_core_web_sm")

def split_into_paragraph(text):
    doc = nlp(text)
    paragraphs = [sent.text for sent in doc.sents]
    return paragraphs


from transformers import pipeline
summarizer = pipeline("summarization", model= "facebook/bart-large-cnn")

def summarize_with_bart(text):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']


#using gTTs
from gtts import gTTS
import os

def text_to_speech(text, output_file="summary.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    os.system(f"start {output_file}")


#import gradio as gr

#def process_file(file):
#    text = extract_text_from_pdf(file.name) #adjust for file type
#    paragraphs = split_into_paragraph(text)
#    summaries = [summarize_with_bart(p) for p in paragraphs[:5]]
#    combined_summary = "\n".join(summaries)
#    text_to_speech(combined_summary)
#    return combined_summary

#gr.Interface(fn=process_file, inputs="file", outputs="text").launch()

if __name__ == "__main__":
    print("Processing PDF..")
    text = extract_text_from_pdf(PDF_PATH)
    paragraphs = split_into_paragraph(text)

    #Summarize first 5 paragraphs (adjust as needed)
    summaries = [summarize_with_bart(p) for p in paragraphs[:5]]
    combined_summary = "\n".join(summaries)

    print("\nSummary:\n", combined_summary)
    text_to_speech(combined_summary)