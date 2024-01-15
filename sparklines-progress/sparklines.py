import time
import copy
import random

from metaflow import FlowSpec, step, card, current
from metaflow.cards import Markdown, Table, VegaChart


class SparklinesFlow(FlowSpec):
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        sparks = []
        rows = []
        for i in range(1, 7):
            spark = RandomSpark(index=i)
            sparks.append(spark)
            rows.append([spark.label, spark.chart])
        current.card.append(Table(rows))
        current.card.refresh()

        for i in range(MAX):
            time.sleep(1)
            for spark in sparks:
                spark.advance()
            current.card.refresh()
        self.next(self.end)

    @step
    def end(self):
        print("done")


# Sparkline as a Vega Lite spec
MAX = 30
SPARKSPEC = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"values": []},
    "height": 20,
    "width": 400,
    "mark": {"type": "area"},
    "encoding": {
        "x": {
            "field": "x",
            "type": "quantitative",
            "scale": {"domain": [0, MAX - 1]},
            "axis": {
                "title": None,
                "orient": "top",
                "domain": False,
                "ticks": False,
                "labels": False,
                "grid": False,
            },
        },
        "y": {
            "field": "y",
            "aggregate": "sum",
            "type": "quantitative",
            "axis": {
                "title": None,
                "domain": False,
                "labels": False,
                "ticks": False,
                "grid": False,
            },
        },
    },
}


class RandomSpark:
    def __init__(self, max_len=MAX, index=0):
        self.max_len = max_len
        self.spec = copy.deepcopy(SPARKSPEC)
        self.speed = random.randint(3, MAX // 6)
        self.data = [{"x": 0, "y": 0}]
        self.index = index
        self.label = Markdown(f"### Updating {self.index}")
        self.spec["data"]["values"] = self.data
        self.chart = VegaChart(self.spec)

    def advance(self):
        import random

        for i in range(self.speed):
            if len(self.data) < self.max_len:
                new_val = max(0, self.data[-1]["y"] + random.randint(-1, 3))
                self.data.append({"x": len(self.data), "y": new_val})
        if len(self.data) == self.max_len:
            self.spec["mark"]["color"] = "green"
            self.label.update(f"### Done updating {self.index}")
        self.chart.update(self.spec)


if __name__ == "__main__":
    SparklinesFlow()
