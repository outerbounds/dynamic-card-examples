from metaflow import step, FlowSpec, current, card, pypi, Parameter
from metaflow.cards import VegaChart
from datetime import datetime
import random
import time
import math

COLORS = ["#004f5f", "#f18a07", "#4dbd05", "#127cb1", "#9b45a3"]


class ScatterFlow(FlowSpec):
    num_points = Parameter("num_points", default=2000)
    num_classes = Parameter("num_classes", default=3)
    num_epochs = Parameter("num_epochs", default=20)

    @pypi(
        packages={"scikit-learn": "1.3.2"},
        python="3.11.7",
    )
    @card(type="scatter3d")
    # @card
    @step
    def start(self):
        from sklearn.datasets import make_classification

        np_data, np_labels = make_classification(
            n_samples=self.num_points,
            n_classes=self.num_classes,
            n_features=3,
            n_informative=3,
            n_redundant=0,
            n_repeated=0,
            n_clusters_per_class=1,
        )
        self.points = [list(arr) for arr in np_data]
        self.classes = list(map(int, np_labels))
        self.labels = [f"class-{i}" for i in range(self.num_classes)]
        self.colors = COLORS[: self.num_classes]

        batch = self.num_points // self.num_epochs
        for i in range(1, self.num_epochs + 1):
            current.card.refresh(
                {
                    "title": f"Epoch {i}/{self.num_epochs}",
                    "points": self.points[: i * batch],
                    "classes": self.classes[: i * batch],
                    "labels": self.labels,
                    "colors": self.colors,
                }
            )
            time.sleep(1)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    ScatterFlow()
