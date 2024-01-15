
A Metaflow Dynamic Card Example
# Basic Chart using Altair

![](../images/rtcard-clockflow.gif)

This example shows how to create a basic progress bar that
updating while a task is executing.

See [Visualizing results](https://docs.metaflow.org/metaflow/visualizing-results) in Metaflow docs for more information.

## Usage

Start a local card server in a terminal (or use your existing Metaflow UI):
```
python clockflow.py card server --poll-interval 1
```
Execute the flow in another terminal:
```
python clockflow.py run
```
