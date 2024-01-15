from metaflow import step, FlowSpec, current, card, pypi
from metaflow.cards import VegaChart, Markdown, Artifact

import time
import json
from collections import Counter, defaultdict
from datetime import datetime


class WikiEventsFlow(FlowSpec):
    def event_stream(self):
        import requests
        import sseclient

        # retrieve real-time page edit events from Wikipedia
        URL = "https://stream.wikimedia.org/v2/stream/recentchange"
        resp = requests.get(URL, stream=True)
        client = sseclient.SSEClient(resp)
        counts = Counter()
        log = defaultdict(list)
        last_update = 0
        for event in client.events():
            try:
                body = json.loads(event.data)
                if (
                    body["meta"]["domain"] == "en.wikipedia.org"
                    and ":" not in body["title"]
                ):
                    # bucket events in 5-second bins
                    key = (body["timestamp"] // 5) * 5
                    counts[key] += 1
                    log[key].append(body["title"][:20])
                    if time.time() - last_update > 5:
                        # update the chart every 5 seconds
                        yield counts, log
                        last_update = time.time()
            except:
                continue

    @pypi(packages={"altair": "5.2.0", "sseclient-py": "1.8.0"}, python="3.11.7")
    @card(type="blank")
    @step
    def start(self):
        import altair as alt

        FOLLOW_SECONDS = 45
        data = []
        source = alt.Data({"values": data})
        chart = alt_chart = None
        begin = time.time()
        current.card.append(Markdown("# Listening to Wikipedia events.."))
        countbox = Markdown("0 events observed")
        current.card.append(countbox)
        current.card.refresh()
        for counts, log in self.event_stream():
            # format data
            data.clear()
            data.extend(
                {
                    "time": datetime.fromtimestamp(t).isoformat(),
                    "event_count": c,
                    "log": ", ".join(log[t]),
                }
                for t, c in sorted(counts.items())
            )
            if chart is None:
                # format data
                first_event = min(counts)
                min_t = datetime.fromtimestamp(first_event - 10).isoformat()
                max_t = datetime.fromtimestamp(
                    first_event + FOLLOW_SECONDS + 10
                ).isoformat()
                alt_chart = (
                    alt.Chart(source)
                    .mark_bar(width={"band": 10.0})
                    .encode(
                        x=alt.X("time:T", scale=alt.Scale(domain=(min_t, max_t))),
                        y="event_count:Q",
                        tooltip=["log:N"],
                    )
                )
                chart = VegaChart.from_altair_chart(alt_chart)
                current.card.append(chart)
                current.card.append(Markdown("Point at a bar to see pages edited"))
            else:
                chart.update(alt_chart.to_dict())
            countbox.update(f"{sum(counts.values())} events observed")
            current.card.refresh()
            if time.time() - begin > 45:
                break
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    WikiEventsFlow()
