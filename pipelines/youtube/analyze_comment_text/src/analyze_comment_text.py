import pandas as pd

df = pd.read_csv("../input/comments_merged_labelled_text.csv")
df.to_csv("../output/comments_merged_labelled_text.csv", index=False)
