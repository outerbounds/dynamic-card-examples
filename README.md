
# Gallery of Metaflow Dynamic Cards

![](images/rtcard-all.gif)

Imagine a long-running task, like training of an ML/AI model, a data processing task,
or a task communicating with an external service. In all these cases, it is useful to
know how the task is performing, how fast it is making progress, and get a sneak peek
to its results *while the task is running*.

Metaflow allows you to [orchestrate even large compute tasks](https://docs.metaflow.org/scaling/introduction)
easily, which you can then [monitor live using dynamic cards](https://docs.metaflow.org/metaflow/visualizing-results).
This repository contains a gallery of dynamic cards, showing how you can apply them in various use cases.

## Starter Examples

Take a look at these simple examples to get started:

 - [Basic Progress Bar](basic-progressbar) - a simple progress bar.
 - [Basic Chart](basic-chart) - A simple updating line chart.
 - [Basic Altair](basic-altair) - An interactive chart made with the Altair library.
 - [Updating Altair](updating-altair) - An Altair chart with updating data.
 - [Map Visualization](map-chart) - Visualize geographical information.
 - [Changing Layout](change-layout) - Adding more elements on the fly.
 - [Many Progress Bars](many-progressbars) - Manage multiple elements in a table.

## Monitoring Work

Dynamic cards are well suited for monitoring work that happens *concurrently* with visualization.
Depending on the type of work you want to monitor (and libraries you use), a few different patterns come in handy:

 - [Monitor with callbacks](monitor-callback) - Using callbacks to monitor progress. In this case, XGBoost training.
 - [Monitoring a thread](monitor-thread) - Monitor work happening in a separate thread. In this case, DuckDB.
 - [Monitoring a subprocess](monitor-subprocess) - Monitor work happening in a subprocess. In this case, training with SciKit Learn.
 - [Monitoring a generator](monitor-events) - Monitor work happening in a separate generator or a co-routine.

## Advanced Examples

Simple things should be simple and complex things should be possible. Here are a few examples of more complex and advanced use cases:

 - [Custom Vega Chart](sparklines-progress) - An example of a custom Vega Lite chart, acting as a progress bar.
 - [Custom Card](custom-card) - A fully custom card using an external JS library. In this case, showing an interactive 3D scatter plot.


