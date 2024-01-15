from metaflow import step, FlowSpec, current, card, pypi
from metaflow.cards import VegaChart
import random
import math
import time


class UpdatingAltairFlow(FlowSpec):
    def point(self, i):
        t = math.radians(i)
        return {
            "x": 0.05 * math.exp(0.05 * t) * math.cos(t),
            "y": 0.05 * math.exp(0.05 * t) * math.sin(t),
        }

    @pypi(packages={"altair": "5.2.0", "vega-datasets": "0.9.0"}, python="3.11.7")
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        import altair as alt

        data = []
        source = alt.Data({"values": data})
        alt_chart = (
            alt.Chart(source)
            .mark_circle(size=20)
            .encode(x="x:Q", y="y:Q")
            .interactive()
        )
        chart = VegaChart.from_altair_chart(alt_chart)
        current.card.append(chart)
        for i in range(30):
            data.extend(self.point(random.randint(0, 2000)) for i in range(50))
            chart.update(alt_chart.to_dict())
            current.card.refresh()
            time.sleep(0.5)

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    UpdatingAltairFlow()
