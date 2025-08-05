import numpy as np
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import asyncio
import sys


if sys.version_info >= (3, 10):  # Important if you're using Python 3.10+
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

# loading the API Key
load_dotenv()
api_key=os.getenv('API_KEY')

model=GoogleGenerativeAIEmbeddings(model='models/text-embedding-004',google_api_key=api_key,task_type="retrieval_document") #embedding model
llm=ChatGoogleGenerativeAI(model='models/gemini-2.5-flash-lite-preview-06-17',google_api_key=api_key) #LLM model

def transcription(vid):  #Generates the transcription
    c=0
    text=''
    chunks=[]
    i=0
    l=['en','hi', 'bn', 'gu', 'as', 'kn', 'ml', 'mr', 'ne', 'or', 'pa', 'sa', 'ta', 'te', 'ur'] #different languages for the extraction order is given
    yt=YouTubeTranscriptApi()

    try:
        transcript=yt.fetch(vid,languages=l)
    except:
        st.write(f'Failed to fetch Transcript')
    
    
    while i<len(transcript):
        text=text+transcript[i].text+' '
        c=c+1
        i=i+1
        if c==4 or c==6:
            text=text+'\t'
        if c==10:
            c=0
            i=i-4
            chunks.append(text+'\n')
            text=''

    df=pd.DataFrame({
        'Chunk':chunks
    })
    return df

def embeddor(transcript):  #embeds the chunks
    i=0
    embeddings=[]
    while i<transcript.shape[0]:
        embeddings.extend(model.embed_documents(transcript.iloc[i:i+250]['Chunk'].tolist()))
        i=i+250
        
    transcript['Embedding']=embeddings
    return transcript

def query_embeddor(query):    #embeds the query
    embedding=model.embed_query(query)
    return embedding

def similarity(emb_query,df):   #does the semantic search between the query and the chunks to find related chunks
    #transcript=pd.DataFrame()
    transcript=df.copy()
    score=cosine_similarity([emb_query],transcript['Embedding'].tolist())
    transcript['Score']=score[0]
    relevent=transcript.sort_values('Score').head(50)
    relevent.sort_index(inplace=True)
    return relevent['Chunk']

def refine_context(context):   #refines the chunks into one fine text for the query context
    text=context.iloc[0].replace('\t',' ')
    for i in range(1,len(context)):
        present_chunk=context.iloc[i].split('\t')
        past_chunk=context.iloc[i-1].split('\t')
        try:
            if past_chunk[2][:-1]==present_chunk[0]:
                text=text[:-1]+present_chunk[1]+present_chunk[2]
            else:
                text=text+present_chunk[0]+present_chunk[1]+present_chunk[2]
        except:
            text=text+context.iloc[i]+'\n'

    return text

def answer(context,query,history,past_session):      #invokes the LLM

    prompt=f"""
You are an intelligent assistant helping a user understand and analyze a YouTube video.

You are given the Video Transcript Context,User Question,Chat History and a summary of the past session between you and the user

Video Transcript Context (retrieved relevant chunks):  
{context}

User Question:  
{query}

Chat History:
{history}

Summary of Past Session Interactions:
{past_session}

Instructions:
- If the answer is clearly present in the transcript, answer based on that.
- If the topic is not explicitly mentioned in the transcript but seems related, you may answer using your own general knowledge.
- If the question is completely unrelated to the transcript, clearly state that it's out of context, and optionally provide a helpful general answer.
- If the user greets respond with an appropriate greeting
- Make use of the chat history and past session summary to make the conversation smooth
- If the past session summary is blank,explicitly mention not remembering past sessions.However if it is present make appropriate use of it in the conversation.

Keep answers clear, polite, and avoid overwhelming details.
"""
    response=llm.invoke(prompt)
    return response.content

def real_time_embedder(query,ans,transcript):       #embeds the live conversation 
    text = f"User query: {query}\nAI answer: {ans}"
    embedding=model.embed_query(text)
    qna_df=pd.DataFrame({'Chunk':text,'Embedding':[embedding]})
    
    return pd.concat([transcript,qna_df],ignore_index=True).drop_duplicates(['Chunk'])

def exporter(chats):        #exports the chat history
    chat_history='\n\n~'.join([f"{i['role']}:{i['content']}" for i in chats])
    return chat_history

def importer(file,transcript):      #processes previous conversation and adds them to the database
    
    text=file.read().decode("utf-8")
    content=text.split('\n\n~')

    for i in range(0,len(content)-1,2):
        query=content[i].split(':')[1]
        answer=content[i+1].split(':')[1]
        transcript=real_time_embedder(query,answer,transcript)
        
    return transcript,text

def past_session_summarize(text):       #summarizes the past session
    prompt = f"""
You are a helpful assistant. Summarize the following interaction thoroughly without missing any key details. Ensure that all important points, discussions, and decisions made are captured clearly and in detail. The summary should preserve the original meaning and technical relevance, while being easy to understand.

Text to summarize:
\"\"\"{text}\"\"\"
"""

    response=llm.invoke(prompt)
    return response.content
    