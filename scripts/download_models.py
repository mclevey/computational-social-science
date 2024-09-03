import subprocess


def download_small_spacy_model():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])


# ADD OTHER LANGUAGE MODELS TOO

if __name__ == "__main__":
    download_small_spacy_model()
