from summarizer import Summarizer,TransformerSummarizer


bert_model = Summarizer()
bert_summary = ''.join(bert_model(sample_text, min_length=60))