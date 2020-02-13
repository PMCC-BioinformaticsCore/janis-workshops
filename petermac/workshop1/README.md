# Peter Mac - Workshop 1

_This README is a meta-commentary and not part of the workshop_

See [Part 1 - Introduction](1-intro.md) for the start of Workshop 1.

## About this workshop

This workshop was produced for training at Peter MacCallum Cancer Centre. Workshop 1 is designed to be a gentle introduction to Janis, specifically within a Peter Mac context.

The intended scope:

- What is Janis, 
    - How Janis is different from seqliner (the previous workflow system)
- How to load Janis (with modules),
- How to run a simple workflow,
- How to align some samples,
- How to debug if something goes wrong (check logs),
- How to override amount of resources,
- How to run the same pipeline on cohort of samples,


## History

Authors:

- Michael Franklin
- Richard Lupat


| Version 	|    Date    	|      Authors     	                | Description     	|
|:---------	|:----------	|:--------------------------------	|:-----------------	|
| v0.1.0  	| 2020-02-04 	| Michael Franklin, Richard Lupat 	| Initial version 	|
| v0.1.1  	| 2020-02-13 	| Michael Franklin, Richard Lupat 	| Based on feedback from workshop 1 	|
|         	|            	|                                 	|                 	|


### Presentations

| Date   	    |      Presenters     	            |  Feedback |
|:-----------	|:--------------------------------	| :---- |
| _2020-02-10_ 	| Michael Franklin, Richard Lupat 	| - The `hello` test should NOT run in the foreground, it breaks the cluster.<br />- In the template, set max_cores=1 + partition=debug (ensure unset in conclusion)<br />- Needs more details in the conclusion.|
| _2020-02-12_ 	| Michael Franklin, Richard Lupat 	| - The `hello` example became too complicated straight out by capturing the WID and overriding an input. - Not enough information about _running_ exemplar pipelines. This would demonstrate how Janis can already be used. - Some templates should support submitting to the cluster by default. |
|         	    |                  	                | |