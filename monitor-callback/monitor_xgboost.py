from metaflow import step, FlowSpec, current, card, pypi_base, Parameter
from metaflow.cards import VegaChart, Markdown, ProgressBar


@pypi_base(
    packages={"altair": "5.2.0", "scikit-learn": "1.3.2", "xgboost": "2.0.3"},
    python="3.11.7",
)
class MonitorXgboostFlow(FlowSpec):
    num_epochs = Parameter("num_epochs", default=200)

    def fit_xgb(self, num_rounds, update_progress):
        import xgboost as xgb

        class ProgressCallback(xgb.callback.TrainingCallback):
            def after_iteration(self, model, epoch, evals_log):
                data = []
                for label in ("train", "valid"):
                    data.extend(
                        {"logloss": e, "label": label, "epoch": i}
                        for i, e in enumerate(evals_log[label]["mlogloss"])
                    )
                update_progress(epoch, data)

        m_train = xgb.DMatrix(self.train_data, self.train_labels)
        m_valid = xgb.DMatrix(self.valid_data, self.valid_labels)
        return xgb.train(
            {"objective": "multi:softmax", "num_class": self.num_classes},
            m_train,
            evals=[(m_train, "train"), (m_valid, "valid")],
            num_boost_round=num_rounds,
            callbacks=[ProgressCallback()],
        )

    def make_chart(self, data):
        import altair as alt

        source = alt.Data({"values": data})
        nearest = alt.selection_point(
            nearest=True, on="mouseover", fields=["epoch"], empty=False
        )
        line = (
            alt.Chart(source)
            .mark_line()
            .encode(x="epoch:Q", y="logloss:Q", color="label:N")
        )

        # the code below makes an interactive selector bar
        # see https://altair-viz.github.io/gallery/multiline_tooltip.html
        selectors = (
            alt.Chart(source)
            .mark_point()
            .encode(
                x="epoch:Q",
                opacity=alt.value(0),
            )
            .add_params(nearest)
        )
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        text = line.mark_text(align="left", dx=5, dy=-5).encode(
            text=alt.condition(nearest, "logloss:Q", alt.value(" "))
        )
        rules = (
            alt.Chart(source)
            .mark_rule(color="gray")
            .encode(
                x="epoch:Q",
            )
            .transform_filter(nearest)
        )
        return alt.layer(line, selectors, points, rules, text)

    @card
    @step
    def start(self):
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split

        print("Generating test data..")
        self.num_classes = 4
        data, labels = make_classification(
            n_samples=100000,
            n_classes=self.num_classes,
            n_features=200,
            n_informative=5,
        )
        (
            self.train_data,
            self.valid_data,
            self.train_labels,
            self.valid_labels,
        ) = train_test_split(data, labels)
        self.next(self.train)

    @card(type="blank", refresh_interval=1)
    @step
    def train(self):
        def update_progress(epoch, data):
            progress.update(epoch + 1)
            chart.update(self.make_chart(data).to_dict())
            current.card.refresh()

        chart = VegaChart.from_altair_chart(self.make_chart([]))
        progress = ProgressBar(max=self.num_epochs, label="epochs")
        current.card.append(Markdown("# XGBoost training"))
        current.card.append(progress)
        current.card.append(chart)
        current.card.refresh()
        self.fit_xgb(self.num_epochs, update_progress)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    MonitorXgboostFlow()
