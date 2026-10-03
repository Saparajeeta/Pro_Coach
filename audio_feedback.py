import queue
import sys
import threading

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

_AUDIO_QUEUE = queue.Queue(maxsize=3)


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
    if pyttsx3 is None:
        return
    try:
        _AUDIO_QUEUE.put_nowait(text)
    except queue.Full:
        pass
