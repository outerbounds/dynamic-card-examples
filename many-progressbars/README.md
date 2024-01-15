
A Metaflow Dynamic Card Example
# Show Many Progress Bars

![](../images/rtcard-manyprogress.gif)

This example shows how to manage multiple concurrent progress bars.

See [Visualizing results](https://docs.metaflow.org/metaflow/visualizing-results) in Metaflow docs for more information.

## Usage

Start a local card server in a terminal (or use your existing Metaflow UI):
```
python manyprogress.py card server --poll-interval 1
```
Execute the flow in another terminal:
```
python manyprogress.py run
```
