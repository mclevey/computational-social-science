import networkx as nx

from .model import ThresholdModel

G = nx.connected_watts_strogatz_graph(n=30, k=3, p=0.5, seed=42, tries=100)


def model_test_run():
    model = ThresholdModel(num_initial_AGREE=5, network=G)
    for i in range(10):
        model.step()


if __name__ == "__main__":
    model_test_run()
