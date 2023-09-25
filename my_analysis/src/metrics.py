import data

TIME = 0
GPUS = 1


def get_total_gpus():
    machines = data.load_table("pai_machine_spec")
    return machines[machines['gpu_type'] != 'CPU']['cap_gpu'].sum()


def split_tasks(tasks):
    tasks = tasks[~(tasks['end_time'].isnull())]
    task_starts = tasks.sort_values(
        'start_time')[['start_time', 'gpus']].values.tolist()
    task_ends = tasks.sort_values(
        'end_time')[['end_time', 'gpus']].values.tolist()
    return task_starts, task_ends


def get_availability(tasks):
    curr_available_gpus = get_total_gpus()
    task_starts, task_ends = split_tasks(tasks)
    print(f"number of tasks: {len(task_starts)}")
    i = 0
    j = 0
    availability = list()
    while i < len(task_starts) and j < len(task_ends):
        if task_starts[i][TIME] == task_ends[j][TIME]: 
            curr_available_gpus -= task_starts[i][GPUS]
            curr_available_gpus += task_ends[j][GPUS]
            availability_timestamp = task_starts[i][TIME]
            i += 1
            j += 1
        elif task_starts[i][TIME] < task_ends[j][TIME]:
            curr_available_gpus -= task_starts[i][GPUS]
            availability_timestamp = task_starts[i][TIME]
            i += 1
        else:
            curr_available_gpus += task_ends[j][GPUS]
            availability_timestamp = task_ends[j][TIME]
            j += 1
        availability.append([availability_timestamp, curr_available_gpus])
    while i < len(task_starts):
        curr_available_gpus -= task_starts[i][GPUS]
        i += 1
    while j < len(task_ends):
        curr_available_gpus += task_ends[j][GPUS]
        j += 1
    return availability
