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


## demo web img
![螢幕擷取畫面 2024-05-25 215646](https://github.com/ISLAB-rui/deidaudioconsultation/assets/56379887/b7cc08a3-ad3a-4de3-b580-963460596ae2)

![螢幕擷取畫面 2024-05-25 215532](https://github.com/ISLAB-rui/deidaudioconsultation/assets/56379887/b1ecbd5d-cd9f-4102-a71d-4589940b1b99)




