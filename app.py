import gradio as gr
from gtts import gTTS
from pdfplumber import open as pp_open
import os

def convert_pdf_to_speech(pdf, language):
    """
    This function takes in a PDF file and converts it to speech.
    
    Parameters:
    pdf (str): The path to the PDF file.
    language (str): The language of the text.

    Returns:
    A message stating that the PDF has been converted to speech.
    """
    
    # Extract text from our pdf
    pdf_content = ""
    
    with pp_open(pdf) as pdf_file:
        for page in pdf_file.pages:
            pdf_content += page.extract_text()
            
    # Convert pdf to speech and make AudioBook!
    tts = gTTS(text=pdf_content, lang=language)
    filename = os.path.basename(pdf)
    filename = f"{filename.split('.')[0]}.mp3"
    tts.save(filename)
    
    return f"Your PDF has been converted to speech. The MP3 file is saved as {os.path.abspath(filename)}"

demo = gr.Blocks(theme='gradio/soft')

with demo:
    # App description
    with gr.Column():
        gr.Markdown("<b>PDF Text-to-Speech Converter</b>")
        gr.Markdown("Convert your PDF files to audio books")

    # Input for the PDF
    pdf_input = gr.File(label="Select a PDF", type="filepath")  

    # Language selector
    language_selector = gr.Dropdown(
        label="Language",
        value="en",
        choices=["en", "es", "de", "it", "fr"],
        interactive=True,
    )

    # Button to start the conversion process
    button = gr.Button("Convert PDF to Speech")
    
    # Output message
    output = gr.Textbox(label="Output")

    with gr.Column():
        # Footer with links to LinkedIn, GitHub and Live demo of PhD defense
        footer_html = """
<div style="text-align: center; margin-top: 20px;">
    <a href="https://www.linkedin.com/in/pejman-ebrahimi-4a60151a7/" target="_blank">LinkedIn</a> |
    <a href="https://github.com/arad1367" target="_blank">GitHub</a> |
    <a href="https://arad1367.pythonanywhere.com/" target="_blank">Live demo of my PhD defense</a> 
    <br>
    Made with 💖 by Pejman Ebrahimi
</div>
"""
        gr.HTML(footer_html)

    # Layout the components
    button.click(convert_pdf_to_speech, inputs=[pdf_input, language_selector], outputs=output)
    
demo.launch()
