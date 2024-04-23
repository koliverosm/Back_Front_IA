import whisper



try:
    model = whisper.load_model("small")
    result = model.transcribe(audio="./kevin.mp3", fp16=False)
    print(result["text"])

    
except Exception as e:
    print(e)