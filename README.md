# DDF Load Test

A simple load testing tool taking advantage of locust.io.

![](http://ddf.slackexception.com/weight.png)

## Setup

#### This requires python 3.5+ to run.

1. Ensure python 3.5+ is installed on your system.
2. Install requirements by running `pip install -r requirements.txt`
    1. `pip` may be aliased to `pip3` on macOS


## Running
1. Run `python DDFLoadTest.py --host=https://localhost:8993` to start the application
    - `python` may be aliased to `python3` on macOS
    - replace `localhost:8993` with running server address
2. Navigate to [http://localhost:8089](http://localhost:8089) to open the Load Test UI.


# DDF Ingest Performance Test

A simple performance testing tool

## Setup

#### This requires python 3.5+ to run.
1. Ensure python 3.5+ is installed on your system.
2. Install requirements by running `pip install -r requirements.txt`
    1. `pip` may be aliased to `pip3` on macOS

## Running

1. Start DDF
2. Run `python DDFIngestTest.py <csw | rest> <path-to-xml-file> <metadata-format>` to start the application
    - `python` may be aliased to `python3` on macOS