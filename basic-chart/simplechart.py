from metaflow import step, FlowSpec, current, card
from metaflow.cards import VegaChart
from datetime import datetime
import random
import time
import math

vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"values": []},
    "mark": "line",
    "encoding": {
        "x": {"field": "time", "type": "temporal"},
        "y": {"field": "value", "type": "quantitative"},
    },
}


class SimpleChartFlow(FlowSpec):
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        data = vega_spec["data"]["values"]
        chart = VegaChart(vega_spec)
        current.card.append(chart)
        for i in range(30):
            val = math.sin(i * 0.1) + random.random() * 0.1 - 0.05
            data.append({"time": datetime.now().isoformat(), "value": val})
            chart.update(vega_spec)
            current.card.refresh()
            time.sleep(1)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    SimpleChartFlow()
