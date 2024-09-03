import logging
import os
from itertools import chain
from typing import Any, List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import spacy
from bertopic import BERTopic
from bertopic.representation import (
    KeyBERTInspired,
    MaximalMarginalRelevance,
    PartOfSpeech,
)
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from hdbscan import HDBSCAN
from scipy.special import softmax
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelBinarizer
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from umap import UMAP

import icsspy.utils as u

logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def make_text_df(filenames: List[str], texts: List[List[str]]) -> pd.DataFrame:
    """
    Create a DataFrame from filenames and corresponding texts.

    Args:
        filenames (List[str]): List of filenames.
        texts (List[List[str]]): List of lists of texts corresponding to each filename.

    Returns:
        pd.DataFrame: DataFrame containing filename, text, and position in text.
    """
    data = {"filename": [], "text": [], "position in text": []}

    for fn, paragraphs in zip(filenames, texts):
        for position, paragraph in enumerate(paragraphs):
            data["filename"].append(fn)
            data["text"].append(paragraph)
            data["position in text"].append(position)

    data = pd.DataFrame(data)
    return data


def truncate_text_to_transformer_limit(text: str, limit: int = 512) -> str:
    """
    Truncate text to the specified transformer limit.

    Args:
        text (str): Text to be truncated.
        limit (int): Maximum length of the text. Defaults to 512.

    Returns:
        str: Truncated text.
    """
    return text[:limit]


def label_topics(
    df: pd.DataFrame,
    textcol: str,
    model: str = "all-MiniLM-L6-v2",
    umap_n_neighbors: int = 15,
    umap_n_components: int = 5,
    hdbscan_min_cluster_size: int = 15,
    hdbscan_min_samples: int = 5,
    mmr_model_diversity: float = 0.3,
    vectorizer_min_df: int = 2,
    vectorizer_max_df: float = 0.9,
    ngram_upper_limit: int = 2,
    top_n_words: int = 10,
    spacy_model: str = "en_core_web_sm",
) -> Tuple[pd.DataFrame, pd.DataFrame, BERTopic]:
    """
    Label topics in the DataFrame using BERTopic.

    Args:
        df (pd.DataFrame): DataFrame containing text data.
        textcol (str): Column name containing text data.
        model (str): Sentence transformer model name. Defaults to "all-MiniLM-L6-v2".
        umap_n_neighbors (int): Number of neighbors for UMAP. Defaults to 15.
        umap_n_components (int): Number of components for UMAP. Defaults to 5.
        hdbscan_min_cluster_size (int): Minimum cluster size for HDBSCAN.
            Defaults to 15.
        hdbscan_min_samples (int): Minimum samples for HDBSCAN. Defaults to 5.
        mmr_model_diversity (float): Diversity parameter for Maximal Marginal Relevance.
            Defaults to 0.3.
        vectorizer_min_df (int): Minimum document frequency for CountVectorizer.
            Defaults to 2.
        vectorizer_max_df (float): Maximum document frequency for CountVectorizer.
            Defaults to 0.9.
        ngram_upper_limit (int): Upper limit for ngram range. Defaults to 2.
        top_n_words (int): Number of top words for topic representation. Defaults to 10.
        spacy_model (str): SpaCy model name. Defaults to "en_core_web_sm".

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, BERTopic]: DataFrame with topics, topic
            information, and BERTopic model.
    """
    df = df.reset_index(drop=True)
    sent_embeddings = SentenceTransformer(model)
    embeddings = sent_embeddings.encode(df[textcol], show_progress_bar=True)
    umap_model = UMAP(
        n_neighbors=umap_n_neighbors,
        n_components=umap_n_components,
        min_dist=0.0,
        metric="cosine",
        random_state=30,
    )
    hdbscan_model = HDBSCAN(
        min_cluster_size=hdbscan_min_cluster_size,
        min_samples=hdbscan_min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    vectorizer_model = CountVectorizer(
        stop_words="english",
        max_df=vectorizer_max_df,
        min_df=vectorizer_min_df,
        ngram_range=(1, ngram_upper_limit),
    )
    keybert_model = KeyBERTInspired()
    pos_model = PartOfSpeech(spacy_model)
    mmr_model = MaximalMarginalRelevance(diversity=mmr_model_diversity)
    representation_model = {
        "KeyBERT": keybert_model,
        "MMR": mmr_model,
        "POS": pos_model,
    }
    topic_model = BERTopic(
        embedding_model=sent_embeddings,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        top_n_words=top_n_words,
        verbose=True,
    )
    topics, probabilities = topic_model.fit_transform(df[textcol], embeddings)
    df["topic"] = topics
    df["topic_probability"] = probabilities
    topic_info = topic_model.get_topic_info()
    return df, topic_info, topic_model


def label_entities(
    model: Any,
    df: pd.DataFrame,
    idcol: str,
    textcol: str,
    drop_invalid_text: bool = True,
) -> Optional[pd.DataFrame]:
    """
    Label entities in the DataFrame using the provided model.

    Args:
        model (Any): Entity recognition model.
        df (pd.DataFrame): DataFrame containing text data.
        idcol (str): Column name for IDs.
        textcol (str): Column name for text data.
        drop_invalid_text (bool): Whether to drop rows with invalid text.
            Defaults to True.

    Returns:
        Optional[pd.DataFrame]: DataFrame with labeled entities, or None if no valid
            entities are found.
    """
    if drop_invalid_text:
        df = df.dropna(subset=[textcol])
        df = df[df[textcol].apply(lambda x: isinstance(x, str) and len(x) > 0)]

    ids = df[idcol]
    text = df[textcol]

    ents: List[pd.DataFrame] = []
    for i, td in tqdm(zip(ids, text), total=len(ids), desc="Labelling entities"):
        try:
            entities = model.predict(td)
            if entities:
                entdf = pd.DataFrame(entities)
                entdf[textcol] = td
                entdf[idcol] = i
                ents.append(entdf)
        except RuntimeWarning as rw:
            if "All-NaN slice encountered" in str(rw):
                logging.warning(f"Skipping NaN slice at ID {i}")
            else:
                logging.error(f"Runtime warning for ID {i}: {rw}")
        except Exception as e:
            logging.error(f"Exception for ID {i}: {e}")

    if ents:
        entdf_concat = pd.concat(ents)
        return entdf_concat
    else:
        logging.info("No valid entities found")
        return None


def label_sentiment(
    model: str,
    df: pd.DataFrame,
    textcol: str,
    idcol: str,
    set_torch_device: bool = True,
    drop_invalid_text: bool = True,
) -> pd.DataFrame:
    """
    Label sentiment in the DataFrame using the specified model.

    Args:
        model (str): Model name for sentiment analysis.
        df (pd.DataFrame): DataFrame containing text data.
        textcol (str): Column name for text data.
        idcol (str): Column name for IDs.
        set_torch_device (bool): Whether to set the torch device. Defaults to True.
        drop_invalid_text (bool): Whether to drop rows with invalid text.
            Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with sentiment labels.
    """
    import torch

    tokenizer = AutoTokenizer.from_pretrained(model, max_len=512)
    model = AutoModelForSequenceClassification.from_pretrained(model)

    if set_torch_device:
        device = u.set_torch_device()
        model.to(device)
    else:
        device = torch.device("cpu")
        model.to(device)

    if drop_invalid_text:
        df = df.dropna(subset=[textcol])
        df = df[df[textcol].apply(lambda x: isinstance(x, str) and len(x) > 0)]

    ids, text = df[idcol], df[textcol]
    scores: List[Any] = []
    sentids: List[Any] = []
    processed_text: List[str] = []

    for i, td in tqdm(zip(ids, text), total=len(ids), desc="Labelling Sentiment"):
        try:
            truncated_text = truncate_text_to_transformer_limit(td)
            encoded = tokenizer.encode(truncated_text, return_tensors="pt").to(device)
            sentsent = model(encoded)
            sentsent = sentsent[0][0].detach().cpu().numpy()
            sentsent = softmax(sentsent)
            scores.append(sentsent)
            processed_text.append(truncated_text)
            sentids.append(i)
        except RuntimeWarning as rw:
            if "All-NaN slice encountered" in str(rw):
                logging.warning(f"Skipping NaN slice at ID {i} in {textcol}")
            else:
                logging.error(f"Runtime warning for ID {i} in {textcol}: {rw}")
        except Exception as e:
            logging.error(f"Exception for ID {i} with text '{td}' in {textcol}: {e}")

    if scores:
        df_sentiment = pd.DataFrame(
            scores,
            columns=["sentiment_negative", "sentiment_neutral", "sentiment_positive"],
        )
        df_sentiment[idcol] = sentids
        df_sentiment[textcol] = processed_text
        logging.info(f"Finished processing {textcol}")
        return df_sentiment
    else:
        logging.info(f"No valid sentiments found for {textcol}")
        return pd.DataFrame(
            columns=[
                "sentiment_negative",
                "sentiment_neutral",
                "sentiment_positive",
                idcol,
            ]
        )


def label_emotion_concepts(
    model: str,
    df: pd.DataFrame,
    textcol: str,
    idcol: str,
    multilabel: bool = True,
    set_torch_device: bool = True,
    drop_invalid_text: bool = True,
) -> pd.DataFrame:
    """
    Label emotion concepts in the DataFrame using the specified model.

    Args:
        model (str): Model name for emotion concept classification.
        df (pd.DataFrame): DataFrame containing text data.
        textcol (str): Column name for text data.
        idcol (str): Column name for IDs.
        multilabel (bool): Whether to use multilabel classification. Defaults to True.
        set_torch_device (bool): Whether to set the torch device. Defaults to True.
        drop_invalid_text (bool): Whether to drop rows with invalid text.
            Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with emotion concept labels.
    """
    import torch

    if set_torch_device:
        device = u.set_torch_device()
    else:
        device = torch.device("cpu")

    pipe = pipeline(
        "text-classification",
        model=model,
        device=device.index if device.type != "cpu" else -1,
        top_k=None if multilabel else 1,
    )

    if drop_invalid_text:
        df = df.dropna(subset=[textcol])
        df = df[df[textcol].apply(lambda x: isinstance(x, str) and len(x) > 0)]

    texts = df[textcol].tolist()
    ids = df[idcol].tolist()

    emodfs: List[pd.DataFrame] = []
    for i, td in tqdm(
        zip(ids, texts), total=len(ids), desc="Labelling Emotion Concepts"
    ):
        truncated_text = truncate_text_to_transformer_limit(td)
        try:
            emo = pipe(truncated_text)
            if isinstance(emo, list):
                if isinstance(emo[0], list):
                    emo_dict = {
                        item["label"]: item["score"]
                        for sublist in emo
                        for item in sublist
                    }
                else:
                    emo_dict = {item["label"]: item["score"] for item in emo}
            else:
                raise ValueError("Unexpected output format from the pipeline.")

            emodf = pd.DataFrame([emo_dict])
            emodf.columns = [f"ec_{c}" for c in emodf.columns]
            emodf[idcol] = i
            emodf[textcol] = truncated_text

            emodfs.append(emodf)
        except Exception as e:
            print(f"Error processing ID {i} with text: {td}")
            print(f"Error: {e}")

    master_emo = pd.concat(emodfs, ignore_index=True)
    return master_emo


def preview_topics(text_topic_df: pd.DataFrame, topic_info: pd.DataFrame) -> None:
    """
    Preview a random sample of the text topic DataFrame and the topic information.

    Args:
        text_topic_df (pd.DataFrame): DataFrame containing text topics.
        topic_info (pd.DataFrame): DataFrame containing topic information.
    """
    print("\nRANDOM SAMPLE (N=30) PREVIEW OF TEXT TOPIC DF")
    print(text_topic_df.sample(30), "\n\n")

    print("\nTOPICS")
    for t, c, r in zip(
        topic_info["Topic"].tolist(),
        topic_info["Count"].tolist(),
        topic_info["Representation"].tolist(),
    ):
        print(t, c, r)


def filter_entities(
    df: pd.DataFrame,
    entity_col: str,
    entity_types: List[str],
    score_col: str,
    score_threshold: float,
) -> pd.DataFrame:
    """
    Filter entities in the DataFrame based on type and score threshold.

    Args:
        df (pd.DataFrame): DataFrame containing entity data.
        entity_col (str): Column name for entity types.
        entity_types (List[str]): List of entity types to filter.
        score_col (str): Column name for entity scores.
        score_threshold (float): Minimum score threshold for filtering.

    Returns:
        pd.DataFrame: Filtered DataFrame with entities.
    """
    if not isinstance(entity_types, list):
        raise ValueError("entity_types should be a list")
    filtered_df = df[
        (df[entity_col].isin(entity_types)) & (df[score_col] >= score_threshold)
    ]
    return filtered_df


def group_entities(
    df: pd.DataFrame, id_col: str, span_col: str, score_col: str
) -> pd.DataFrame:
    """
    Group entities by ID and aggregate spans and scores.

    Args:
        df (pd.DataFrame): DataFrame containing entity data.
        id_col (str): Column name for IDs.
        span_col (str): Column name for entity spans.
        score_col (str): Column name for entity scores.

    Returns:
        pd.DataFrame: Grouped DataFrame with aggregated spans and scores.
    """
    grouped_df = (
        df.groupby(id_col)
        .agg(
            spans_list=(span_col, lambda x: list(x)),
            scores_list=(score_col, lambda x: list(x)),
        )
        .reset_index()
    )
    return grouped_df


def construct_entity_topic_edgelist(
    df: pd.DataFrame, topic_col: str = "topic", entities_col: str = "entities_list"
) -> pd.DataFrame:
    """
    Construct an edge list from topics and entities.

    Args:
        df (pd.DataFrame): DataFrame containing topic and entity data.
        topic_col (str): Column name for topics. Defaults to "topic".
        entities_col (str): Column name for entities. Defaults to "entities_list".

    Returns:
        pd.DataFrame: DataFrame containing the edge list with counts.
    """
    edge_list: List[Tuple[Any, Any]] = []
    for topic, entities in zip(df[topic_col], df[entities_col]):
        if entities is not None and not pd.isna(topic):
            if topic != -1:  # -1 is the BERTopic junk topic; who cares...
                if isinstance(entities, list):
                    for ent in entities:
                        if ent is not None:
                            edge_list.append((topic, ent))
    edge_df = pd.DataFrame(edge_list, columns=["topic", "entity"])
    edge_df = edge_df.groupby(["topic", "entity"]).size().reset_index(name="count")
    return edge_df


# REFACTORING FROM DCSS


def get_topic_word_scores(df, n_words, topic_column, all_topics=False, as_tuples=True):
    df = df.sort_values(by=[topic_column], ascending=False)
    if all_topics is True:
        result = pd.concat([df.head(n_words), df.tail(n_words)]).round(4)
    else:
        result = pd.concat([df.head(n_words), df.tail(n_words)]).round(4)
        result = result[topic_column]
        if as_tuples is True:
            result = list(zip(result.index, result))
    return result


def sparse_groupby(groups, sparse_m, vocabulary):
    grouper = LabelBinarizer(sparse_output=True)
    grouped_m = grouper.fit_transform(groups).T.dot(sparse_m)

    df = pd.DataFrame.sparse.from_spmatrix(grouped_m)
    df.columns = vocabulary
    df.index = grouper.classes_

    return df


def bigram_process(
    texts, nlp=None, threshold=0.75, scoring="npmi", detokenize=True, n_process=1
):
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    sentences = []
    docs = []

    # sentence segmentation doesn't need POS tagging or lemmas.
    for doc in tqdm(
        nlp.pipe(texts, disable=["tagger", "lemmatizer", "ner"], n_process=n_process),
        total=len(texts),
        desc="Processing sentences",
    ):
        doc_sents = [
            [
                token.text.lower()
                for token in sent
                if token.text != "\n" and token.is_alpha
            ]
            for sent in doc.sents
        ]
        sentences.extend(doc_sents)
        docs.append(doc_sents)

    model = Phrases(sentences, min_count=1, threshold=threshold, scoring=scoring)
    bigrammer = Phraser(model)
    bigrammed_list = [
        [bigrammer[sent] for sent in doc] for doc in tqdm(docs, desc="Applying bigrams")
    ]

    if detokenize:
        bigrammed_list = [[" ".join(sent) for sent in doc] for doc in bigrammed_list]
        bigrammed_list = [" ".join(doc) for doc in bigrammed_list]
    elif detokenize == "sentences":
        bigrammed_list = [[" ".join(sent) for sent in doc] for doc in bigrammed_list]
    else:
        bigrammed_list = list(chain(*bigrammed_list))

    return model, bigrammed_list


def preprocess(
    texts, nlp=None, bigrams=False, detokenize=True, n_process=1, custom_stops=[]
):
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    processed_list = []
    allowed_postags = [92, 96, 84]  # 'NOUN', 'PROPN', 'ADJ'

    if bigrams:
        model, texts = bigram_process(texts, detokenize=True, n_process=n_process)

    for doc in tqdm(
        nlp.pipe(texts, disable=["ner", "parser"], n_process=n_process),
        total=len(texts),
        desc="Preprocessing documents",
    ):
        processed = [
            token.lemma_
            for token in doc
            if not token.is_stop and len(token) > 1 and token.pos in allowed_postags
        ]

        if detokenize:
            processed = " ".join(processed)
            processed_list.append(processed)
        else:
            processed_list.append(processed)

    if bigrams:
        return model, processed_list
    else:
        return processed_list


def plot_topic_distribution(topic_distr, topic_model, doc_index, filename=None):
    """
    Plots the topic probability distribution for a single document.

    Parameters:
    - topic_distr: The matrix of topic distributions for all documents.
    - topic_model: The BERTopic model (or similar) used to generate the topics.
    - doc_index: The index of the document in the topic_distr matrix to plot.

    Returns:
    - A horizontal bar chart of the topic probabilities for the specified document.
    """

    # Get the topic distribution for the specified document
    doc_topics = topic_distr[doc_index]

    # Filter out topics with zero probability
    non_zero_topics = doc_topics > 0
    doc_topics = doc_topics[non_zero_topics]

    # Retrieve topic names or numbers
    topic_names = [
        f"Topic {i}: {topic_model.get_topic(i)[0][0]}"
        for i in range(len(non_zero_topics))
        if non_zero_topics[i]
    ]

    # Plot the horizontal bar chart
    plt.figure(
        figsize=(10, 8 + 0.2 * len(topic_names))
    )  # Dynamic figure height based on number of topics
    plt.barh(topic_names, doc_topics, color="C0")

    # Set labels and title
    plt.xlabel("\nTopic Probability")
    plt.ylabel("")
    plt.title(f"Topic Probability Distribution for Document {doc_index}\n", loc="left")

    # Dynamically adjust the y-axis limits to avoid bars touching the plot edges
    plt.ylim(-0.5, len(topic_names) - 0.5)

    # Remove the top and bottom grid lines while keeping the x-axis grid lines
    plt.grid(True, which="major", axis="x", linestyle="--", alpha=0.7)

    # Dynamically adjust layout to avoid grid line issues at the top and bottom
    plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.1)

    # Display the plot
    if filename is not None:
        plt.savefig(filename, dpi=300)
