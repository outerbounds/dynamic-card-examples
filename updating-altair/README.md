
A Metaflow Dynamic Card Example
# Updating Altair Chart

![](../images/rtcard-updatingaltair.gif)

This example shows how to update data in an Altair chart on the fly.
For more details, see [Altair's documentation](https://altair-viz.github.io/).

See [Visualizing results](https://docs.metaflow.org/metaflow/visualizing-results) in Metaflow docs for more information.

## Usage

Start a local card server in a terminal (or use your existing Metaflow UI):
```
python updating_altair.py --environment=pypi card server --poll-interval 1
```
Execute the flow in another terminal:
```
python updating_altair.py --environment=pypi run
```
