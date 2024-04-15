import streamlit as st
from pipeline import Deid_audio
import time
import json

st.title("錄音檔去識別化 demo Website")
# st.session_state.masked_file = None

if 'masked_file' not in st.session_state:
    st.session_state['masked_file'] = None
    st.session_state.new_file = False
    st.session_state.res_json = None

def upf():
    print(f"file uploaded {time.time()}")
    if st.session_state['file_upload'] is not None:
        # save the file
        with open(f'./.output/{st.session_state["file_upload"].name}', 'wb') as f:
            f.write(st.session_state['file_upload'].getvalue())
        st.session_state.new_file = True

st.file_uploader("Choose a .mp3 file" , type="mp3" , on_change=upf , key="file_upload")

if st.session_state['file_upload'] is not None:
    st.write('original file')
    st.audio(st.session_state['file_upload'])

if st.session_state['file_upload'] is None:
    st.session_state['masked_file'] = None
if st.session_state.new_file:
    # print wait message
    pw = st.empty()
    pw.text('Please wait for a while...')
    st.session_state.new_file = False

    # add press bar
    my_bar = st.progress(5)
    status_text = st.empty()
    deid = Deid_audio(f'./.output/{st.session_state["file_upload"].name}')

    status_text.text('wisperx...')
    deid.wisperx()
    my_bar.progress(30)
    
    status_text.text('pythia model...')
    deid.model()
    my_bar.progress(80)
    
    status_text.text('mask audio...')
    deid.mask_audio()
    my_bar.progress(100)
    # print(deid.get_masked_file_path())


    status_text.text('Done!')
    pw.empty()
    st.session_state.masked_file = deid.get_masked_file_path()
    


    with open(f'./.output/{st.session_state["file_upload"].name.replace(".mp3" , "_mask.json")}') as f:
        st.session_state['res_json'] =  json.load(f)

# if success generate masked file then show the audio player and download button
if st.session_state['masked_file'] is not None:
    st.write('Masked file')
    st.audio(st.session_state.masked_file)
    with open(st.session_state.masked_file, 'rb') as f:
        audio_bytes = f.read()
    st.download_button( label="Download Masked Audio", 
                        data=audio_bytes , 
                        file_name=f"{st.session_state['masked_file'].split('/')[-1]}"
                        )

    st.write(st.session_state.res_json)










