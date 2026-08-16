AVAILABLE = [3, 3, 2]
MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}


def calculate_need():
    return {p: [MAX_NEED[p][i] - ALLOCATION[p][i] for i in range(3)] for p in MAX_NEED}


def safety(available, allocation, need):
    work = available[:]
    finish = {p: False for p in allocation}
    sequence = []
    changed = True
    while changed:
        changed = False
        for p in allocation:
            if not finish[p] and all(need[p][i] <= work[i] for i in range(3)):
                work = [work[i] + allocation[p][i] for i in range(3)]
                finish[p] = True
                sequence.append(p)
                changed = True
    return all(finish.values()), sequence


def try_request(process, request):
    need = calculate_need()
    available = AVAILABLE[:]
    allocation = {p: v[:] for p, v in ALLOCATION.items()}

    if not all(request[i] <= need[process][i] for i in range(3)):
        return False, "Request exceeds process Need."
    if not all(request[i] <= available[i] for i in range(3)):
        return False, "Request exceeds Available resources."

    available = [available[i] - request[i] for i in range(3)]
    allocation[process] = [allocation[process][i] + request[i] for i in range(3)]
    need[process] = [need[process][i] - request[i] for i in range(3)]
    safe, sequence = safety(available, allocation, need)
    if safe:
        return True, f"Granted; resulting state is safe. Safe sequence: {sequence}"
    return False, "Denied: granting the request leaves the system unsafe, even though it fits Available and the process Need."


if __name__ == "__main__":
    need = calculate_need()
    print("Need matrix:", need)
    safe, seq = safety(AVAILABLE, ALLOCATION, need)
    print("Initial safe:", safe)
    print("Initial safe sequence:", seq)
    for p, req in (("P1", [1, 0, 2]), ("P0", [2, 0, 2])):
        granted, reason = try_request(p, req)
        print(f"{p} request {req}: {reason}")
