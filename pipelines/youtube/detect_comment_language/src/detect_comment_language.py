import pandas as pd
from tqdm import tqdm
from transformers import pipeline

import icsspy
from icsspy.text import truncate_text_to_transformer_limit

logger = icsspy.initialize_logger()

device = icsspy.set_torch_device()
model = "papluca/xlm-roberta-base-language-detection"
classifier = pipeline("text-classification", model=model, device=device)

df = pd.read_csv("../input/comments_processed.csv")

# remove invalid text
df = df.dropna(subset=["processed_text"])
df = df[df["processed_text"].apply(lambda x: isinstance(x, str) and len(x) > 0)]

ids = df["comment_id"].tolist()
text = df["processed_text"].tolist()

# Do I want to wrap this up in a function like the others?
vids, preds, scores = [], [], []
for vid, text in tqdm(
    zip(ids, text), total=len(ids), desc="Detecting comment language"
):
    try:
        truncated_text = truncate_text_to_transformer_limit(text)
        predicted_language = classifier(truncated_text)

        if predicted_language:
            vids.append(vid)
            preds.append(predicted_language[0]["label"])
            scores.append(predicted_language[0]["score"])
    except Exception as e:
        logger.error(f"Error processing comment_id {vid}: {e}")

langdf = pd.DataFrame(
    {"comment_id": vids, "predicted_language": preds, "confidence_score": scores}
)

langdf.to_csv("../output/comments_predicted_language.csv", index=False)
logger.info("Finished predicting comment languages\n")
print(langdf.head())
