from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import os

def summarize_text(model_dir, input_text, checkpoint_num=None, max_input_length=512, max_output_length=128):
    # If checkpoint_num is provided, create the path to the specific checkpoint directory
    checkpoint_path = f"{model_dir}/checkpoint-{checkpoint_num}" if checkpoint_num is not None else model_dir

    # Check if config.json is present in the checkpoint directory
    config_path = f"{checkpoint_path}/config.json"
    if checkpoint_num is not None and not os.path.exists(config_path):
        raise FileNotFoundError(f"config.json not found in {checkpoint_path}")

    # Load the trained model and tokenizer
    model = BartForConditionalGeneration.from_pretrained(checkpoint_path)
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    # Tokenize and convert the input text to input_ids
    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=max_input_length,
        truncation=True,
    )

    # Generate the summary
    summary_ids = model.generate(
        input_ids,
        max_length=max_output_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=False,
    )

    # Decode the summary_ids to text
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

# Example usage
output_dir = "./output"  # Adjust the path to your output directory
checkpoint_number = 3003  # Specify the desired checkpoint number
sample_text = """
In a quiet corner of the city, an unassuming shop turned into a battlefield when a seemingly ordinary customer, John, stumbled upon an ancient artifact. Little did he know that his discovery would lead to a series of events that would culminate in an unexpected hero emerging from the shadows.

The scene unfolded at Harikumar Merchant's Antiquities Emporium, a shop known for its collection of rare and ancient artifacts. John, an enthusiast of historical curiosities, entered the establishment and was immediately drawn to a particularly intriguing item – a weathered piece of papyrus dating back to 1000 BCE.

Curiosity piqued, John inquired about the origins of the artifact from Harikumar, the shopkeeper. As Harikumar began to explain the historical significance of the ancient papyrus, a tangible air of mystery surrounded the conversation. It was at this moment that the situation took an unforeseen turn.

In an unexpected move, John, seemingly inspired by the historical weaponries of ancient cultures, produced a set of ninja stars. The atmosphere in the shop shifted from one of scholarly curiosity to one of tension as the police were promptly summoned.

The arrival of the police, anticipating a routine disturbance, escalated into a full-blown spectacle as a battalion of around a hundred ninjas descended upon the scene. The ninjas, armed with an array of lethal ninja stars, engaged in a confrontational standoff with the police officers. The situation rapidly spiraled out of control, prompting the police to call for urgent backup.

Responding to the escalating chaos, three helicopters, fifteen cop cars, and four firetrucks raced to the scene, creating an unusual tableau of law enforcement and emergency services converging on a seemingly tranquil antique shop. As the ninjas intensified their assault, targeting both police officers and emergency vehicles, the situation reached a critical juncture.

It was at this crucial moment that an unexpected figure entered the fray – Jiro, a revered figure known as the Japan king in local circles. Dressed in traditional attire and exuding an air of authority, Jiro approached the chaotic scene. To the surprise of onlookers, the ninjas, as if acknowledging a higher authority, ceased their attack on the police and turned their attention to Jiro.

Taking advantage of the momentary diversion, the police regrouped and assessed the situation. Jiro, displaying a remarkable ability to communicate with the ninjas, managed to pacify the situation and defuse the tension. The once-aggressive ninjas, now under the influence of Jiro's authoritative presence, stood down.

Grateful for Jiro's intervention, the police, in a gesture of appreciation, bestowed upon him the keys to the city. Jiro, the Japan king, became an unlikely hero, not only for quelling the ninja invasion but also for averting a potential catastrophe involving law enforcement and emergency services.

The events at Harikumar Merchant's Antiquities Emporium transformed a routine day into a riveting tale of unexpected turns. The ancient papyrus, once a source of intrigue, became the catalyst for an extraordinary sequence of events. Jiro's intervention not only saved the day but also highlighted the unpredictable nature of everyday life in a bustling city. As the city returned to its usual rhythm, the mysterious papyrus remained as an enduring artifact, silently witnessing the peculiar chapter it had inspired in the city's history.


"""
result = summarize_text(output_dir, sample_text, checkpoint_num=checkpoint_number, max_output_length=128)
print("Original Text:\n", sample_text)
print("\nSummary:\n", result)