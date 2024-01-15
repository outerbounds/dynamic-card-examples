from metaflow import step, FlowSpec, current, card
from metaflow.cards import Markdown, ProgressBar, Table

import time


class ManyProgressFlow(FlowSpec):
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        ANIMALS = [("🐰", 3), ("🐖", 1.5), ("🐎", 5), ("🐢", 1)]
        import time

        rows = []
        for animal, speed in ANIMALS:
            rows.append([Markdown(f"# {animal}"), ProgressBar(max=19)])
        current.card.append(Markdown("# Ready, set, go! 🏁"))
        current.card.append(Table(rows))
        current.card.refresh()
        for i in range(20):
            time.sleep(1)
            for j, (_, speed) in enumerate(ANIMALS):
                rows[j][1].update(min(19, i * speed))
            current.card.refresh()
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    ManyProgressFlow()
