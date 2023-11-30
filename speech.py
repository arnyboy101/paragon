from gtts import gTTS
import os

class TextToSpeechConverter:
    def __init__(self, text, output_dir='output', language='en'):
        self.text = text
        self.output_dir = output_dir
        self.language = language

    def convert_to_audio(self, filename='output.mp3'):
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, filename)

        myobj = gTTS(text=self.text, lang=self.language, slow=False)
        myobj.save(output_path)

        return output_path