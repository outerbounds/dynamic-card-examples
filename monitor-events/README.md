
A Metaflow Dynamic Card Example
# Monitor Results Produced by a Generator

![](../images/rtcard-wikievents.gif)

This example shows how to structure your flow in two parts: A generator (co-routine) that
executes your main workload while another function monitors progress.

Here, our generator is `event_stream` which subscribes to a real-time event stream of
edits made to Wikipedia. It collects statistics and yields them periodically to the
step function for visualization. The chart is interactive: Point at a bar to
see what edits people have made just seconds ago!

You can use this pattern to structure your own applications. Just `yield` statistics
periodically for visualization.

See [Visualizing results](https://docs.metaflow.org/metaflow/visualizing-results) in Metaflow docs for more information.

## Usage

Start a local card server in a terminal (or use your existing Metaflow UI):
```
python wikievents.py --environment=pypi card server --poll-interval 1
```
Execute the flow in another terminal:
```
python wikievents.py --environment=pypi run
```
