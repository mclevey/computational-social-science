import pandas as pd

df = pd.read_csv("../input/channels_merged_labelled_text.csv")
df.to_csv("../output/channels_merged_labelled_text.csv", index=False)
