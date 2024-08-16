from mesa import Agent


class BoundedConfidenceAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print(f"Hi, I'm BoundedConfidenceAgent agent {self.unique_id}")
