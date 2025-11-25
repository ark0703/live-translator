import speech_recognition as sr
import time
import inspect
import asyncio
import googletrans as gt
from gtts import gTTS
import pygame

output_file = "./output_audio.mp3"


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("I'm Listening... ")
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)  # type: ignore[attr-defined]
        print("You said: ", text)
        return text
    
    except sr.UnknownValueError:
        print("Can't understand, What you are saying...")
    except IOError as e:
        print(f"An IOError occurred: {e}")
    except KeyboardInterrupt:
        print("Listener Stopped.")
    except sr.RequestError as e:
        print(f"Could Not Request Results From Google Speech Recognition service; {e} ")


def voice_conversion(text, targeted_lang):
    if text is None:
        return
    translator = gt.Translator()
    # Use named parameter for clarity (dest). Some googletrans implementations
    # expose an async translate() which returns a coroutine. Handle both sync
    # and async return values.
    try:
        maybe_coro = translator.translate(text, dest=targeted_lang)
    except TypeError:
        # Fallback if the translator implementation expects positional args
        maybe_coro = translator.translate(text, targeted_lang)

    # If it's awaitable (a coroutine or Future), wrap it in a small
    # coroutine so we always pass a proper coroutine object to
    # asyncio.run / run_coroutine_threadsafe (this avoids type issues).
    if inspect.isawaitable(maybe_coro):
        async def _await_and_return(a):
            return await a

        try:
            translation = asyncio.run(_await_and_return(maybe_coro))
        except RuntimeError:
            # If an event loop is already running in this thread, try
            # run_coroutine_threadsafe on the running loop as a fallback.
            try:
                loop = asyncio.get_event_loop()
                future = asyncio.run_coroutine_threadsafe(_await_and_return(maybe_coro), loop)
                translation = future.result()
            except Exception as e:
                print(f"Could not run async translation: {e}")
                return None
    else:
        translation = maybe_coro

    # translation is expected to be an object with .text when successful
    try:
        print("Translation: ", translation.text)
        return translation.text
    except AttributeError:
        # If translation isn't the expected object, return its string form
        print("Translation (raw):", translation)
        return str(translation)


def text_to_voice(translated, targeted_lang):
    if translated is None:
        return
    tts = gTTS(text=translated, lang=targeted_lang, slow=False)
    tts.save(output_file) 


def play_sound(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        time.sleep(sound.get_length())  # Wait for the sound to finish playing
        
    except OSError as e:
        print(f"An IO Error Occurred: {e}")
    except pygame.error as e:
        print(f"Error playing sound: {e}")
    finally:
        pygame.mixer.quit()
