import os

import pandas as pd
from span_marker import SpanMarkerModel

import icsspy
import icsspy.text as t
import icsspy.utils as u

logger = icsspy.initialize_logger()

device = u.set_torch_device()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


df = pd.read_csv("../input/comments_processed_english.csv")

model = SpanMarkerModel.from_pretrained(
    "tomaarsen/span-marker-bert-base-fewnerd-fine-super"
)

device = u.set_torch_device()
model.to(device)

all_ents_comments_dfs = []

for channel, group_df in df.groupby("channel"):
    ents_comments = t.label_entities(model, group_df, "comment_id", "processed_text")
    ents_comments["channel"] = channel
    all_ents_comments_dfs.append(ents_comments)

final_ents_comments_df = pd.concat(all_ents_comments_dfs, ignore_index=True)
final_ents_comments_df.to_csv("../output/comments_entities.csv", index=False)
print(final_ents_comments_df.sample(30))
logger.info("Finished labelling entities")
