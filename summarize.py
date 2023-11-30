from summarizer import Summarizer

class TextSummarizer:
    def __init__(self):
        pass

    def summarize(self, sample_text, min_length=60):
        model = Summarizer()
        summary = ''.join(model(sample_text, min_length=min_length))
        return summary