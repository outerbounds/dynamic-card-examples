from metaflow import step, FlowSpec, current, card, pypi
from metaflow.cards import VegaChart

# An interactive Altair example from
# https://altair-viz.github.io/gallery/selection_histogram.html
class AltairFlow(FlowSpec):
    @pypi(packages={"altair": "5.2.0", "vega-datasets": "0.9.0"}, python="3.11.7")
    @card(type="blank")
    @step
    def start(self):
        import altair as alt
        from vega_datasets import data

        source = data.cars()
        brush = alt.selection_interval()
        points = (
            alt.Chart(source, width=500, height=400)
            .mark_point()
            .encode(
                x="Horsepower:Q",
                y="Miles_per_Gallon:Q",
                color=alt.condition(brush, "Origin:N", alt.value("lightgray")),
            )
            .add_params(brush)
        )

        bars = (
            alt.Chart(source)
            .mark_bar()
            .encode(y="Origin:N", color="Origin:N", x="count(Origin):Q")
            .transform_filter(brush)
        )

        chart = VegaChart.from_altair_chart(points & bars)
        current.card.append(chart)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    AltairFlow()
