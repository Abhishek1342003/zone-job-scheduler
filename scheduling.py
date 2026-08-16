from jobs import JOBS


def _print_table(title, rows):
    print(f"\n{title}")
    print("Job       Waiting  Turnaround")
    print("--------- -------  ----------")
    for job_id, waiting, turnaround in rows:
        print(f"{job_id:<9} {waiting:>7}  {turnaround:>10}")
    avg_w = sum(r[1] for r in rows) / len(rows)
    avg_t = sum(r[2] for r in rows) / len(rows)
    print(f"Average   {avg_w:>7.3f}  {avg_t:>10.3f}")


def fcfs(jobs=JOBS):
    time = 0
    completion = {}
    remaining = {j["job_id"] for j in jobs}
    while remaining:
        ready = [j for j in jobs if j["job_id"] in remaining and j["arrival_time"] <= time]
        if not ready:
            time = min(j["arrival_time"] for j in jobs if j["job_id"] in remaining)
            continue
        job = min(ready, key=lambda j: (j["arrival_time"], j["job_id"]))
        time += job["burst_time"]
        completion[job["job_id"]] = time
        remaining.remove(job["job_id"])
    return metrics(jobs, completion)


def sjf(jobs=JOBS):
    time = 0
    completion = {}
    remaining = {j["job_id"] for j in jobs}
    while remaining:
        ready = [j for j in jobs if j["job_id"] in remaining and j["arrival_time"] <= time]
        if not ready:
            time = min(j["arrival_time"] for j in jobs if j["job_id"] in remaining)
            continue
        job = min(ready, key=lambda j: (j["burst_time"], j["arrival_time"], j["job_id"]))
        time += job["burst_time"]
        completion[job["job_id"]] = time
        remaining.remove(job["job_id"])
    return metrics(jobs, completion)


def srtf(jobs=JOBS):
    time = 0
    completion = {}
    remaining = {j["job_id"]: j["burst_time"] for j in jobs}
    while len(completion) < len(jobs):
        ready = [
            j for j in jobs
            if j["arrival_time"] <= time and j["job_id"] not in completion and remaining[j["job_id"]] > 0
        ]
        if not ready:
            time = min(j["arrival_time"] for j in jobs if j["job_id"] not in completion and remaining[j["job_id"]] > 0)
            continue
        job = min(ready, key=lambda j: (remaining[j["job_id"]], j["arrival_time"], j["job_id"]))
        jid = job["job_id"]
        future_arrivals = [j["arrival_time"] for j in jobs if j["arrival_time"] > time and j["job_id"] not in completion]
        next_arrival = min(future_arrivals) if future_arrivals else float("inf")
        run_for = min(remaining[jid], next_arrival - time)
        time += run_for
        remaining[jid] -= run_for
        if remaining[jid] == 0:
            completion[jid] = time
    return metrics(jobs, completion)


def metrics(jobs, completion):
    rows = []
    for job in jobs:
        turnaround = completion[job["job_id"]] - job["arrival_time"]
        waiting = turnaround - job["burst_time"]
        rows.append((job["job_id"], waiting, turnaround))
    return rows


if __name__ == "__main__":
    for name, fn in (("FCFS", fcfs), ("Non-preemptive SJF", sjf), ("SRTF", srtf)):
        _print_table(name, fn())
