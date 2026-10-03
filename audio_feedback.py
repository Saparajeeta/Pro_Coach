import queue
import sys
import threading
import time

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

VOICE_ENABLED = True
_AUDIO_QUEUE = queue.Queue(maxsize=3)
_LAST_SPEAK = {}
_SPEAK_LOCK = threading.Lock()


def set_voice_enabled(flag):
    global VOICE_ENABLED
    VOICE_ENABLED = bool(flag)


def _audio_worker():
    if sys.platform.startswith("win"):
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass

    if pyttsx3 is None:
        return

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
    except Exception as e:
        print(f"Audio failed: {e}")
        engine = None

    while True:
        try:
            text = _AUDIO_QUEUE.get()
            if text is None:
                continue
            if engine is None:
                continue
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Audio failed: {e}")
        except Exception as e:
            print(f"Audio failed: {e}")
        finally:
            try:
                _AUDIO_QUEUE.task_done()
            except Exception:
                pass


if pyttsx3 is not None:
    _WORKER = threading.Thread(target=_audio_worker, daemon=True)
    _WORKER.start()


def play_audio(text):
    if not VOICE_ENABLED or pyttsx3 is None or text is None:
        return
    try:
        _AUDIO_QUEUE.put_nowait(text)
    except queue.Full:
        pass


def speak_feedback(key, text, cooldown=4.0):
    if not VOICE_ENABLED or text is None:
        return
    now = time.monotonic()
    with _SPEAK_LOCK:
        last = _LAST_SPEAK.get(key, 0.0)
        if now - last < cooldown:
            return
        _LAST_SPEAK[key] = now
    play_audio(text)
