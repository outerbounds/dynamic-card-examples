import sys
import re
from multiprocessing import Pool, TimeoutError
from tempfile import NamedTemporaryFile

from metaflow import step, FlowSpec, current, card, pypi_base
from metaflow.cards import VegaChart, Markdown, Artifact

VEGA_SPEC = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"values": []},
    "mark": "line",
    "title": "Training loss",
    "encoding": {
        "x": {"field": "epoch", "type": "quantitative"},
        "y": {"field": "loss", "type": "quantitative", "scale": {"type": "log"}},
    },
}


@pypi_base(
    packages={"scikit-learn": "1.3.2"},
    python="3.11.7",
)
class MonitorSklearnFlow(FlowSpec):
    @card
    @step
    def start(self):
        from sklearn.datasets import make_classification

        print("Generating test data..")
        self.num_classes = 2
        self.train_data, self.train_labels = make_classification(
            n_samples=100000,
            n_classes=self.num_classes,
            n_features=400,
            n_informative=50,
        )
        self.next(self.train)

    @card(type="blank", refresh_interval=1)
    @step
    def train(self):
        data = []
        VEGA_SPEC["data"]["values"] = data
        chart = VegaChart(VEGA_SPEC)

        def update_charts(logfile):
            with open(logfile) as f:
                # parse model training logs
                vals = re.findall("Avg. loss: (.+)", f.read(), re.MULTILINE)
                data.clear()
                data.extend({"epoch": i, "loss": v} for i, v in enumerate(vals))
                chart.update(VEGA_SPEC)
                current.card.refresh()

        current.card.append(Markdown("# Training an SGDClassifier model"))
        current.card.append(chart)
        current.card.refresh()

        with NamedTemporaryFile() as tmp:
            with Pool(1) as pool:
                # start training in a subprocess
                proc = pool.apply_async(
                    train_process, (self.train_data, self.train_labels, tmp.name)
                )
                # wait until training is done
                while True:
                    try:
                        # wait for a second
                        self.model = proc.get(1)
                    except TimeoutError:
                        # update charts if we are not done
                        update_charts(tmp.name)
                    else:
                        # otherwise output the model and stop
                        current.card.append(Markdown("Training done!"))
                        current.card.append(Artifact(self.model))
                        break
            update_charts(tmp.name)
        self.next(self.end)

    @step
    def end(self):
        pass


def train_process(train_data, train_labels, output_file):
    # this function is run in a subprocess
    from sklearn.linear_model import SGDClassifier

    # redirect verbose output to a file
    # NOTE remember set buffering=1 or otherwise charts will update slowly
    sys.stdout = open(output_file, "w", buffering=1)
    model = SGDClassifier(verbose=1, max_iter=1000)
    model.fit(train_data, train_labels)
    return model


if __name__ == "__main__":
    MonitorSklearnFlow()
