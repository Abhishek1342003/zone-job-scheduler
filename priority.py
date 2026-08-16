from jobs import JOBS


def priority_schedule(aging=False, jobs=JOBS):
    time = 0
    done = set()
    completion = {}
    dispatches = []

    while len(done) < len(jobs):
        ready = [j for j in jobs if j["job_id"] not in done and j["arrival_time"] <= time]
        if not ready:
            time = min(j["arrival_time"] for j in jobs if j["job_id"] not in done)
            continue

        def effective_priority(job):
            if not aging:
                return job["priority"]
            waited = time - job["arrival_time"]
            return max(1, job["priority"] - (waited // 3))

        job = min(ready, key=lambda j: (effective_priority(j), j["arrival_time"], j["job_id"]))
        dispatches.append((job["job_id"], time, effective_priority(job)))
        time += job["burst_time"]
        completion[job["job_id"]] = time
        done.add(job["job_id"])

    rows = []
    for job in jobs:
        turnaround = completion[job["job_id"]] - job["arrival_time"]
        waiting = turnaround - job["burst_time"]
        rows.append((job["job_id"], waiting, turnaround))
    return rows, dispatches


def show(label, aging):
    rows, dispatches = priority_schedule(aging)
    print(f"\n{label}")
    print("Dispatch order:", " -> ".join(x[0] for x in dispatches))
    print("Job       Waiting  Turnaround")
    for row in rows:
        print(f"{row[0]:<9} {row[1]:>7}  {row[2]:>10}")
    longest = max(rows, key=lambda x: x[1])
    print(f"Longest wait: {longest[0]} ({longest[1]})")


if __name__ == "__main__":
    show("Priority scheduling - no aging", False)
    show("Priority scheduling - with aging", True)
