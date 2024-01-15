from metaflow import step, FlowSpec, current, card, pypi, profile
from metaflow.cards import VegaChart, Markdown, Table

import time
from tempfile import NamedTemporaryFile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

URL = (
    "https://metaflow-demo-public.s3.us-west-2.amazonaws.com"
    "/taxi/sandbox/train_sample.parquet"
)


class DuckDBFlow(FlowSpec):
    def exec_duckdb(self, stats):
        # this function runs in a separate thread
        import duckdb
        import requests

        with NamedTemporaryFile(suffix=".parquet") as tmp:
            with profile("download", stats_dict=stats):
                tmp.write(requests.get(URL).content)
            tmp.flush()
            with profile("create_table", stats_dict=stats):
                duckdb.sql("CREATE TABLE taxi AS SELECT * FROM '%s'" % tmp.name)
                for i in range(100):
                    duckdb.sql("INSERT INTO taxi SELECT * FROM '%s'" % tmp.name)

        time.sleep(5)
        with profile("query", stats_dict=stats):
            return duckdb.sql(
                "select date_trunc('day', key), sum(fare_amount) from taxi group by 1"
            ).fetchall()

    def update_charts(self, proc, components, db_profile, mem_stats, cpu_stats):
        t = datetime.now().isoformat()
        cpu_stats.append({"time": t, "cpu": proc.cpu_percent()})
        mem_stats.append({"time": t, "memory": proc.memory_info().rss / 1024**2})
        for k, v in db_profile.items():
            if v:
                components[k].update(str(v))
        components["cpu_chart"].update(self.make_chart("cpu", cpu_stats).to_dict())
        components["mem_chart"].update(self.make_chart("memory", mem_stats).to_dict())
        current.card.refresh()

    def make_chart(self, label, data):
        import altair as alt

        source = alt.Data({"values": data})
        return (
            alt.Chart(source).mark_line().encode(x="time:T", y="%s:Q" % label)
        ).properties(title=label.capitalize(), width=300, height=200)

    @pypi(
        packages={"altair": "5.2.0", "duckdb": "0.9.2", "psutil": "5.9.7"},
        python="3.11.7",
    )
    @card(type="blank", refresh_interval=1)
    @step
    def start(self):
        import psutil

        proc = psutil.Process()
        db_profile = {"download": 0, "create_table": 0, "query": 0}
        mem_stats = []
        cpu_stats = []
        components = {}
        rows = []
        for label in db_profile:
            m = components[label] = Markdown("")
            rows.append([Markdown(label), m])

        [components["cpu_chart"], components["mem_chart"]] = chart_row = [
            VegaChart.from_altair_chart(self.make_chart("cpu", [])),
            VegaChart.from_altair_chart(self.make_chart("memory", [])),
        ]

        current.card.append(Markdown("# Execute a DuckDB query"))
        current.card.append(Table([chart_row]))
        current.card.append(Table(rows, headers=["Stage", "Milliseconds"]))
        current.card.refresh()

        with ThreadPoolExecutor(max_workers=1) as exe:
            res = exe.submit(self.exec_duckdb, db_profile)
            while True:
                try:
                    q = res.result(1)
                    break
                except TimeoutError:
                    self.update_charts(
                        proc, components, db_profile, mem_stats, cpu_stats
                    )

        # cool down in the end to record final stats
        for i in range(10):
            self.update_charts(proc, components, db_profile, mem_stats, cpu_stats)
            time.sleep(1)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    DuckDBFlow()
