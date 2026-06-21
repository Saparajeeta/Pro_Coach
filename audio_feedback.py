import pyttsx3
import threading

def init_engine():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        return engine
    except Exception as e:
        print(f"Audio init failed: {e}")
        return None

def _speak(text):
    engine = init_engine()
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Audio play failed: {e}")

def play_audio(text):
    """
    Play audio in a separate thread so it doesn't block video processing.
    """
    t = threading.Thread(target=_speak, args=(text,))
    t.start()
