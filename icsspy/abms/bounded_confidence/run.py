from .model import BoundedConfidenceModel


def run_model():
    model = BoundedConfidenceModel(10)  # Initialize with 10 agents
    for i in range(100):  # Run for 100 steps
        model.step()


if __name__ == "__main__":
    run_model()
