from gtts import gTTS

def generate_audio(text, lang, output_file):
    # Create a TTS object with the specified language
    tts = gTTS(text=text, lang=lang)
    
    # Save the generated audio to a file
    tts.save(output_file)
    print(f"Audio saved as {output_file}")

# Example usage for each language
# generate_audio("Hello, how are you? hope this finds you well", lang='ha', output_file='hausa.mp3')
# generate_audio("Hello, how are you? hope this finds you well", lang='ak', output_file='twi.mp3')
# generate_audio("Hello, how are you? hope this finds you well", lang='ee', output_file='ewe.mp3')
generate_audio("Hello, how are you? hope this finds you well", lang='sw', output_file='swahili.mp3')
generate_audio("Hello, how are you? hope this finds you well", lang='yo', output_file='yoruba.mp3')
generate_audio("Hello, how are you? hope this finds you well", lang='ig', output_file='igbo.mp3')
