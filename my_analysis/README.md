# My Analysis of GPU Cluster

## Obtaining Data

On Windows (i.e. without `curl`): 

1. Go to `cluster-trace-gpu-v2020\data\download_data.sh`.
2. Click on each link to trigger download.
3. "Extract here" each downloaded `tar.gz` with WinRAR to get CSVs.

On Linux, just run (from `src`): 

```bash
bash prep_data.sh
```

## Existing Work

Existing work from NSDI paper: 
* Low task GPU utilization (0.042). 
* Peak job request is 1000 GPUs.
* High tasks repetition (65% repeated 5 times) -- don't explain how they identify duplicate tasks.
* 60% of most jobs have queueing delay of max 10s.
* 10% of jobs requesting > 1 GPU can wait hours.
* < 4K GPUs allocated at any given time

## Ideas 

1. Given a particular job, track it's available GPUs over time.
* Can obtain the total number of GPUs from the cluster with `metrics::get_total_gpus()`.
* To look at GPU availability, we want to look at what Alibaba deems as tasks. Tasks which are subcomponents of jobs (e.g. workers in a parameter server) and they are the ones that make GPU requests. 
* First, we drop all waiting tasks. They haven't started in the timespan of the Alibaba trace and aren't useful for analysis.
* Next, we scale down their GPU measure from percentage to GPU fraction. We leave fractional amounts as the Alibaba and most schedulers do GPU sharing.
* We drop all NaN GPU counts. There isn't anything we can really obtain from this. Not sure what the authors were thinking to get out of this.
* We drop all NaN end times. NaN end times occur for tasks that have failed, terminated, and are still running. For running tasks that makes sense. However, we can't really do anything about terminated and failed ones. We assume the scheduler gets GPUs back for failed and terminated tasks, but we don't know when they did.
* Now, to compute availability we sort tasks by start and end time. We get two lists and then loop and every task that starts, we take its requested GPU count away from the total. Then for every ending task we give the GPU count back. At times where a task starts and ends then we give and take at the same time.
* The result is that a lot of GPUs appear free. in fact, a large portion of GPUs remain available. This would indicate that we really aren't getting the full picture from the trace and our truncations of the trace.
* They do not give their source code for figure 8 which is closest to what we are interested in (which shows GPU usage over a 24 HR time period). However, it seems that even in that plot, with GPU sharing, there is high GPU availability.
