from metaflow import step, FlowSpec, current, card
from metaflow.cards import VegaChart
from datetime import datetime
import random
import time
import math

vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 600,
    "height": 400,
    "data": {
        "url": "https://vega.github.io/vega-lite/examples/data/us-10m.json",
        "format": {"type": "topojson", "feature": "counties"},
    },
    "transform": [
        {
            "lookup": "id",
            "from": {
                "data": {
                    "url": "https://vega.github.io/vega-lite/examples/data/unemployment.tsv"
                },
                "key": "id",
                "fields": ["rate"],
            },
        }
    ],
    "projection": {"type": "albersUsa"},
    "mark": {"type": "geoshape", "tooltip": True},
    "encoding": {"color": {"field": "rate", "type": "quantitative"}},
}


class MapChartFlow(FlowSpec):
    @card(type="blank")
    @step
    def start(self):
        chart = VegaChart(vega_spec)
        current.card.append(chart)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    MapChartFlow()
