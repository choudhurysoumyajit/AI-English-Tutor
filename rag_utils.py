import os
import json
import tempfile
from langchain_groq import ChatGroq
#from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import shutil
from groq import Groq
from pathlib import Path
#from elevenlabs.client import ElevenLabs
#from elevenlabs.play import play
#from elevenlabs import save
from gtts import gTTS

os.environ["CHROMA_TELEMETRY"] = "false"

load_dotenv()

def ask_question(query, k=3, file_flag=False):

        llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
        )

        prompt_template = """
        As a highly knowledgeable chat assistant and a proficient english tutor, your role is to accurately interpret queries and 
        provide appropriate responses.

        Listen the statement provided, understand the context. Find out the grammatical mistakes and help user to rectify that 
        or provide ideas on how to improve the same sentence . Be creative and Continue the discussion by proactively asking more engaging questions untill user is not willing to continue.  

        Make the conversation interesting and humanlike.   

        Provide conscise answers within 100 word limit. 
        Question: {question}
        """
        custom_prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

        prompt_text = custom_prompt.format(
            question=query
        )
        
        # Invoke the chain with input data and include the callback
        result = llm.invoke(prompt_text)
        print(result.content)
        print(file_flag)
        response_text = result.content

        return response_text

def audio_transcript(audio_file):
    # Initialize the Groq client
    client = Groq() 
    if audio_file:
    # Display audio player
        transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo", 
        file=Path(audio_file), 
        #response_format="text",
        prompt="provide an accurate transcription of the audio file using ponctuations and capitalization as well."
        )
        return transcription.text
        
def text_to_speech(input_text):
    client = ElevenLabs(
    api_key=os.getenv('ELELABS_API_KEY') 
)
    audio = client.text_to_speech.convert(
    text=input_text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)
    #play(audio)
    #save(audio, "output.mp3")

def text_to_speech2(input_text):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=input_text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("t2s.mp3")
