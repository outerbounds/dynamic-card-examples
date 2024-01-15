
A Metaflow Dynamic Card Example
# Basic Chart using Altair

![](../images/rtcard-altairflow.gif)

This example shows how to create a basic interactive chart
using Altair. For more details, see [Altair's documentation](https://altair-viz.github.io/).
This chart doesn't update while the task is executing.

See [Visualizing results](https://docs.metaflow.org/metaflow/visualizing-results) in Metaflow docs for more information.

## Usage

Start a local card server in a terminal (or use your existing Metaflow UI):
```
python altairflow.py --environment=pypi card server --poll-interval 1
```
Execute the flow in another terminal:
```
python altairflow.py --environment=pypi run
```
