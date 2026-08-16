from scheduling import fcfs, sjf, srtf
from round_robin import round_robin
from priority import priority_schedule
from bankers import calculate_need, safety, try_request, AVAILABLE, ALLOCATION
from memory_translation import translate_paged, translate_segmented
from race_peterson import unsynchronized_demo, peterson_demo


def print_sched(name, rows):
    print(f"\n{name}")
    for row in rows:
        print(row)
    print("Average waiting:", sum(r[1] for r in rows) / len(rows))
    print("Average turnaround:", sum(r[2] for r in rows) / len(rows))


if __name__ == "__main__":
    print_sched("FCFS", fcfs())
    print_sched("SJF", sjf())
    print_sched("SRTF", srtf())
    for q in (3, 6):
        rows, timeline, switches = round_robin(q)
        print_sched(f"RR q={q}", rows)
        print("Dispatch slices:", len(timeline), "Context switches:", switches)
    for aging in (False, True):
        rows, dispatches = priority_schedule(aging)
        print_sched("Priority aging=" + str(aging), rows)
        print("Dispatch order:", [x[0] for x in dispatches])
    print("\nBanker's Need:", calculate_need())
    print("Banker's initial safety:", safety(AVAILABLE, ALLOCATION, calculate_need()))
    print("P1:", try_request("P1", [1, 0, 2]))
    print("P0:", try_request("P0", [2, 0, 2]))
    print("\nPaging:")
    for x in (260, 1500, 3000, 5000): print(translate_paged(x))
    print("Segmentation:")
    for x in ((0, 150), (1, 350), (2, 100)): print(translate_segmented(*x))
    print("\nRace condition:")
    unsynchronized_demo(5)
    peterson_demo(5)
