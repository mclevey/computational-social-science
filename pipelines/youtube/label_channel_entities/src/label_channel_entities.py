import os

import pandas as pd
from span_marker import SpanMarkerModel

import icsspy
import icsspy.text as t

logger = icsspy.initialize_logger()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


df = pd.read_csv("../input/channels_processed.csv")

model = SpanMarkerModel.from_pretrained(
    "tomaarsen/span-marker-bert-base-fewnerd-fine-super"
)

device = icsspy.set_torch_device()
model.to(device)

all_ents_channels_dfs = []

for channel, group_df in df.groupby("channel"):
    ents_channels = t.label_entities(model, group_df, "video_id", "processed_text")
    ents_channels["channel"] = channel
    all_ents_channels_dfs.append(ents_channels)

final_ents_channels_df = pd.concat(all_ents_channels_dfs, ignore_index=True)
final_ents_channels_df.to_csv("../output/channels_entities.csv", index=False)
logger.info("Finished labelling entities\n")
print(final_ents_channels_df.sample(30))
