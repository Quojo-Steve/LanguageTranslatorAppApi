import speech_recognition as sr

def mic_to_text(recognizer, language):
    with sr.Microphone() as source:
        print("adjusting for ambient noise for mic")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("listening...Speak into the mic")
        try:
            audio = recognizer.listen(source, timeout=10)
            print("processing...wait")
            text = recognizer.recognize_google(audio, language=language)
            print("Text: " + text)
            
            with open("mic_to_text","w") as file:
                file.write(text)
        except sr.WaitTimeoutError:
            print("No audio coming from mic")
        except sr.UnknownValueError:
            print("google does not understand the input audio")
        except sr.RequestError as e:
            print(f"request failed to google service {e}")
        except Exception as e:
            print(f"Error Ocurred {e}")

def main():
    recognizer = sr.Recognizer()
    mic_to_text(recognizer=recognizer, language="en-EN") ## voice to text

if __name__=="__main__":
    main()