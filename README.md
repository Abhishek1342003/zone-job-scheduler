# Zone Job-Scheduler & Cloud/IoT Deployment

This repository contains the complete answer for **Q2 Part 1 (60 marks) and Part 2 (40 marks)**. Part 2 explicitly deploys the fixed compute core implemented in Part 1.

## Requirements

- Python 3.9+
- No third-party Python packages are required.

## Repository structure

```text
.
├── jobs.py
├── scheduling.py
├── round_robin.py
├── priority.py
├── race_peterson.py
├── bankers.py
├── memory_translation.py
├── run_all.py
├── docs/
│   └── architecture_blueprint.md
└── README.md
```

## Part 1 — fixed input

`jobs.py` contains the exact 8-job list from the question and is imported by the scheduling scripts. `job_id` and `priority` are the two PCB fields. `zone`, `arrival_time`, and `burst_time` are simulation-only metadata.

## Run the programs

```bash
python scheduling.py
python round_robin.py
python priority.py
python race_peterson.py
python bankers.py
python memory_translation.py
python run_all.py
```

## Measured Part 1 results

### FCFS, SJF and SRTF

| Algorithm | Average waiting | Average turnaround |
|---|---:|---:|
| FCFS | 17.125 | 22.625 |
| Non-preemptive SJF | 13.000 | 18.500 |
| SRTF | 11.500 | 17.000 |

For this fixed workload, SRTF has the lowest average waiting time, followed by SJF and FCFS.

### Round Robin

| Quantum | Average waiting | Average turnaround | Dispatch slices | Context switches |
|---:|---:|---:|---:|---:|
| 3 | 22.625 | 28.125 | 17 | 16 |
| 6 | 20.375 | 25.875 | 11 | 10 |

The boundary convention counts a context switch as a **job change between adjacent dispatch slices**, so 17 slices produce 16 switches and 11 slices produce 10 switches. In a real OS, the quantum-3 run would have more switching overhead because it causes 16 observed job changes versus 10 for quantum 6; switching is not free in a real OS.

### Priority scheduling

No aging:

| Job | Waiting | Turnaround |
|---|---:|---:|
| Z1-J01 | 0 | 8 |
| Z1-J02 | 7 | 11 |
| Z2-J01 | 27 | 36 |
| Z2-J02 | 11 | 16 |
| Z3-J01 | 8 | 10 |
| Z3-J02 | 33 | 39 |
| Z1-J03 | 13 | 16 |
| Z2-J03 | 14 | 21 |

Longest wait: **Z3-J02 = 33 ticks**.

With aging, effective priority is `max(1, priority - (ticks waited since becoming ready // 3))` at each dispatch decision:

| Job | Waiting | Turnaround |
|---|---:|---:|
| Z1-J01 | 0 | 8 |
| Z1-J02 | 7 | 11 |
| Z2-J01 | 10 | 19 |
| Z2-J02 | 18 | 23 |
| Z3-J01 | 22 | 24 |
| Z3-J02 | 23 | 29 |
| Z1-J03 | 28 | 31 |
| Z2-J03 | 29 | 36 |

Longest wait: **Z2-J03 = 29 ticks**. Z3-J02's wait decreases from 33 to 23 ticks.

### Peterson's Algorithm

The unsynchronized counter starts at 100. One thread subtracts 40 and the other adds 25, so the correct serialized result is 85. The race demonstration forces a read/sleep/write interleaving and runs it five times; at least one run should differ from 85. The Peterson version protects the read-modify-write section and is expected to return exactly 85 on all five runs.

### Banker's Algorithm

Initial Need matrix:

```text
P0: [7, 4, 3]
P1: [1, 2, 2]
P2: [6, 0, 0]
P3: [0, 1, 1]
```

Initial state: **safe**.

One valid safe sequence: **P1 → P3 → P0 → P2**.

- `P1` request `[1, 0, 2]`: **granted**; resulting state is safe.
- `P0` request `[2, 0, 2]`: **denied** because the resulting state is unsafe, even though the request is within both Available and P0's Need.

### Paging and segmentation

Paged logical addresses:

- `260` → physical `5380`
- `1500` → physical `2524`
- `3000` → physical `10168`
- `5000` → **page fault** because page 4 is absent from the page table.

Segmented logical addresses:

- `(0, 150)` → physical `1150`
- `(1, 350)` → **segmentation fault** because `350 >= 300`
- `(2, 100)` → physical `600`

## Task 8 — production choice

**Production choice: SRTF / SJF family, specifically SRTF where preemption is operationally acceptable.**

For this exact workload, SRTF measured **11.500 average waiting ticks**, compared with **13.000 for SJF** and **17.125 for FCFS**. It therefore minimizes waiting among the measured FCFS/SJF-family alternatives.

Why the other three families are less suitable for this workload:

1. **FCFS:** 17.125 average waiting ticks, which is 5.625 ticks higher than SRTF.
2. **Round Robin:** even its better measured quantum-6 run has 20.375 average waiting ticks and 10 context switches, while quantum 3 has 22.625 waiting and 16 switches.
3. **Priority scheduling:** no-aging priority has a 33-tick maximum wait for Z3-J02; aging reduces that job's wait to 23 but still gives a 29-tick maximum wait for Z2-J03.

This choice is specifically justified by the measured results for the supplied 8-job workload; a production system with strict response-time or starvation constraints could require a different policy after operational requirements are measured.

## Part 2

The complete Cloud, Security & IoT Deployment Blueprint is in:

`docs/architecture_blueprint.md`

It covers Tasks 9–14: Hybrid architecture, communication protocols, VPC isolation, six network-security objectives, IAM and data protection, IoT connectivity/layers, and concrete threats with mitigations.

## One-repository submission

Submit the URL of this single public GitHub repository. Do not create separate repositories for Part 1 and Part 2.
