from collections import deque
from jobs import JOBS


def round_robin(quantum, jobs=JOBS):
    ordered = sorted(jobs, key=lambda j: (j["arrival_time"], j["job_id"]))
    remaining = {j["job_id"]: j["burst_time"] for j in jobs}
    completion = {}
    ready = deque()
    timeline = []
    time = 0
    index = 0

    while len(completion) < len(jobs):
        while index < len(ordered) and ordered[index]["arrival_time"] <= time:
            ready.append(ordered[index])
            index += 1
        if not ready:
            time = ordered[index]["arrival_time"]
            continue

        job = ready.popleft()
        jid = job["job_id"]
        start = time
        run = min(quantum, remaining[jid])
        time += run
        remaining[jid] -= run
        timeline.append((jid, start, time))

        # Boundary convention: newly arrived jobs enter the ready queue before
        # a quantum-expired job is re-added to the back.
        while index < len(ordered) and ordered[index]["arrival_time"] <= time:
            ready.append(ordered[index])
            index += 1

        if remaining[jid] > 0:
            ready.append(job)
        else:
            completion[jid] = time

    rows = []
    for job in jobs:
        turnaround = completion[job["job_id"]] - job["arrival_time"]
        waiting = turnaround - job["burst_time"]
        rows.append((job["job_id"], waiting, turnaround))

    switches = sum(a[0] != b[0] for a, b in zip(timeline, timeline[1:]))
    return rows, timeline, switches


def print_run(quantum):
    rows, timeline, switches = round_robin(quantum)
    avg_w = sum(r[1] for r in rows) / len(rows)
    avg_t = sum(r[2] for r in rows) / len(rows)
    print(f"\nRound Robin quantum={quantum}")
    print("Job       Waiting  Turnaround")
    for row in rows:
        print(f"{row[0]:<9} {row[1]:>7}  {row[2]:>10}")
    print(f"Average waiting: {avg_w:.3f}")
    print(f"Average turnaround: {avg_t:.3f}")
    print(f"Dispatch slices: {len(timeline)}")
    print(f"Context switches/job changes: {switches}")


if __name__ == "__main__":
    print_run(3)
    print_run(6)
