# DeidAudioConsultation

## venv 
```
python -m venv .venv
.\.venv\Scripts\activate
```

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers peft datasets 
pip install git+https://github.com/m-bain/whisperx.git
pip install streamlit pydub
```

```
pip freeze > requirements.txt
pip install -r requirements.txt

```



## How to run the web
```
streamlit run .\web.py
```


## demo video

https://github.com/ISLAB-rui/deidaudioconsultation/assets/56379887/896333fa-4e41-429b-b6a1-9d44514bd1af




