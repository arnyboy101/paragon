# train.py
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split


class BBCNewsDataset(Dataset):
    def __init__(self, articles, summaries, tokenizer, max_source_length=1024, max_target_length=128, truncation=True):
        self.tokenizer = tokenizer
        self.max_source_length = max_source_length
        self.max_target_length = max_target_length
        self.articles = articles
        self.summaries = summaries
        self.truncation = truncation

    def __len__(self):
        return len(self.articles)

    def __getitem__(self, idx):
        article = self.articles[idx]
        summary = self.summaries[idx]

        inputs = self.tokenizer(
            article,
            max_length=self.max_source_length,
            return_tensors="pt",
            truncation=True,
            padding="max_length",  # Add padding to ensure consistent length
        )
        labels = self.tokenizer(
            summary,
            max_length=self.max_target_length,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
        )

        return {
            "input_ids": inputs["input_ids"].flatten(),
            "attention_mask": inputs["attention_mask"].flatten(),
            "labels": labels["input_ids"].flatten(),
        }

# Function to train the model
def train_model():
    # Load the dataset
    dataset = load_dataset("gopalkalpande/bbc-news-summary")

    # Split the 'train' dataset into training and evaluation sets
    train_articles, eval_articles, train_summaries, eval_summaries = train_test_split(
        dataset["train"]["Articles"],
        dataset["train"]["Summaries"],
        test_size=0.1,
        random_state=42,
    )

    # Initialize the model and tokenizer
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Prepare the training dataset
    train_dataset = BBCNewsDataset(
        articles=train_articles,
        summaries=train_summaries,
        tokenizer=tokenizer,
        max_source_length=1024,
        max_target_length=128,
    )

    # Prepare the evaluation dataset
    eval_dataset = BBCNewsDataset(
        articles=eval_articles,
        summaries=eval_summaries,
        tokenizer=tokenizer,
        max_source_length=1024,
        max_target_length=128,
    )

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./output",
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        evaluation_strategy="epoch",
        save_total_limit=3,
        save_strategy="epoch",
        num_train_epochs=3,
        learning_rate=5e-5,
        overwrite_output_dir=True,
        load_best_model_at_end=True,
        resume_from_checkpoint="./output",
    )

    # Initialize Trainer with both training and evaluation datasets
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    # Fine-tune the model
    trainer.train()

