import speech_recognition as sr
      
def file_to_text(recognizer, language, file_path):
    with sr.AudioFile(file_path) as source:
        audio = recognizer.listen(source, timeout=10)
        try:
            print("processing...wait")
            text = recognizer.recognize_google(audio, language=language)
            print("Text: " + text)
            
            with open("audio_file_to_text","w") as file:
                file.write(text)
        
        except sr.UnknownValueError:
            print("google does not understand the input audio")
        except sr.RequestError as e:
            print(f"request failed to google service {e}")
        except Exception as e:
            print(f"Error Ocurred {e}")
def main():
    recognizer = sr.Recognizer()
    file_name = "english_car.wav"
    file_to_text(recognizer=recognizer, language="en_EN", file_path=file_name) ## audio to text

if __name__=="__main__":
    main()