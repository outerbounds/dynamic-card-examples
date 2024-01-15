from metaflow import step, FlowSpec, current, card
from metaflow.cards import Markdown, ProgressBar


class ClockFlow(FlowSpec):
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        from datetime import datetime
        import time

        m = Markdown("# Clock is starting 🕒")
        p = ProgressBar(max=30, label="Seconds passed")
        current.card.append(m)
        current.card.append(p)
        current.card.refresh()
        for i in range(31):
            t = datetime.now().strftime("%H:%M:%S")
            m.update(f"# Time is {t}")
            p.update(i)
            current.card.refresh()
            print(t)
            time.sleep(1)
        m.update("# ⏰ ring ring!")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    ClockFlow()
