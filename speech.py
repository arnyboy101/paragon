import boto3
import os

class TextToSpeechConverter:
    def __init__(self, text, output_dir='output', language='en-US', voice='Joanna'):
        self.text = text
        self.output_dir = output_dir
        self.language = language
        self.voice = voice

    def convert_to_audio(self, filename='output.mp3'):
        # Create a Polly client
        polly_client = boto3.client('polly')

        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Text=self.text,
            OutputFormat='mp3',
            VoiceId=self.voice,
            LanguageCode=self.language
        )

        # Save the audio to the specified directory
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, filename)

        with open(output_path, 'wb') as f:
            f.write(response['AudioStream'].read())

        return output_path
