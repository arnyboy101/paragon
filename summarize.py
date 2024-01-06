from transformers import PegasusTokenizer, PegasusForConditionalGeneration, pipeline
class TextSummarizer:
    def __init__(self):
        pass

    def model_init(self):
        model_name = 'Joemgu/pegasus-x-sumstew'
        tokenizer = PegasusTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
        return summarizer
        
    def summarize(self, sample_text, min_length=60):
        model = self.model_init()
        summary = ''.join(model(sample_text, min_length=min_length,do_sample=False,max_length=150)[0]['summary_text'])
        print(summary)
        return summary