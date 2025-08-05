import streamlit as st
import re
from streamlit_chat import message
import helper
import uuid
import requests

# UI Design
st.sidebar.title('hAIck')
st.sidebar.image('pictures/logo.png',width=100)
st.sidebar.markdown('---')
url=st.sidebar.text_input("Enter Video URL")

col=st.columns([1,1,1])
col[1].image('pictures/avatar.png')
col[1].markdown('### Let\'s Dive Deep')
st.markdown('---')
st.sidebar.markdown('###### *Reload on Crash')
st.sidebar.markdown('---')

# Checking entry condition

if 'Past_Session' not in st.session_state:
    st.session_state['Past_Session']=''

# Extracting video ID from Youtube URL
try:

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    vid=match.group(1)
    
    # Extracting transcript and checking if video ID is changed or not
    if ('Transcript' not in st.session_state) or (st.session_state['VID']!=vid):

        st.session_state['VID']=vid
        st.session_state['Chats']=[]
        st.session_state['Chat_Index']=0
        with st.spinner('Analyzing Video...'):
            print("hello 3 here")
            transcript=helper.transcription(vid)
            transcript=helper.embeddor(transcript)  
            st.session_state['Transcript']=transcript 
        
    # File uploader for uploading previous interactions
    upload=st.sidebar.file_uploader('Import Chat History')

    if ((upload is not None) and ('Imported' not in st.session_state)):
        st.session_state['Imported']=upload
        st.session_state['Transcript'],text=helper.importer(upload,st.session_state['Transcript'])
        st.session_state['Past_Session']=helper.past_session_summarize(text)
        st.sidebar.download_button("Export Chat History",helper.exporter(st.session_state['Chats']))
   
        for i,msg in enumerate(st.session_state['Chats']):
            if msg['role']=='user':
                message(msg['content'],is_user=True,key=uuid.uuid4().hex) # Generating unique IDs for each conversation text
            else:
                message(msg['content'],key=uuid.uuid4().hex)

    query=st.chat_input('Ask anything')

    if query!=None:
        st.session_state['Chats'].append({'role':'user','content':query})

        for i,msg in enumerate(st.session_state['Chats']):
            if msg['role']=='user':
                message(msg['content'],is_user=True,key=uuid.uuid4().hex)
            else:
                message(msg['content'],key=uuid.uuid4().hex)

        st.session_state['Chat_Index']+=1

    with st.spinner('Generating...'):
        emb_query=helper.query_embeddor(query)
        context=helper.similarity(emb_query,st.session_state['Transcript'])
        context=helper.refine_context(context)

        history=st.session_state['Chats'][-20:]
        history='\n'.join([f"{message['role']}:{message['content']}" for message in st.session_state['Chats']])
        print(history)
        answer=helper.answer(context,query,history,st.session_state['Past_Session'])
    
    st.session_state['Chats'].append({'role':'assistant','content':answer})
    st.session_state['Transcript']=helper.real_time_embedder(query,answer,st.session_state['Transcript'])
    
    message(st.session_state['Chats'][st.session_state['Chat_Index']]['content'])
           
    st.session_state['Chat_Index']+=1

    st.sidebar.download_button("Export Chat History",helper.exporter(st.session_state['Chats']))  # Downloading Chat History for future reference

# Exception Handling
except AttributeError as e:
    pass
except TypeError as e:
    pass
except requests.exceptions.SSLError:
    col=st.columns([1,2,1])
    col[1].markdown('##### Please use VPN to proceed...!!!')
except UnboundLocalError as e:
    col[1].markdown('##### Quota exceeded.Try again later...!!!')