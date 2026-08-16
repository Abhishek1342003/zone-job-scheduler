import threading
import time


def unsynchronized_once():
    counter = [100]
    start = threading.Barrier(2)

    def subtract():
        start.wait()
        old = counter[0]
        time.sleep(0.001)
        counter[0] = old - 40

    def add():
        start.wait()
        old = counter[0]
        time.sleep(0.001)
        counter[0] = old + 25

    t1 = threading.Thread(target=subtract)
    t2 = threading.Thread(target=add)
    t1.start(); t2.start(); t1.join(); t2.join()
    return counter[0]


def unsynchronized_demo(runs=5):
    values = [unsynchronized_once() for _ in range(runs)]
    print("Unsynchronized runs:", values)
    print("At least one differs from 85:", any(v != 85 for v in values))
    return values


def peterson_demo(runs=5):
    results = []
    for _ in range(runs):
        counter = [100]
        flag = [False, False]
        turn = [0]
        start = threading.Barrier(2)

        def critical_section(me, other, delta):
            start.wait()
            flag[me] = True
            turn[0] = other
            while flag[other] and turn[0] == other:
                time.sleep(0)
            old = counter[0]
            time.sleep(0.001)
            counter[0] = old + delta
            flag[me] = False

        t1 = threading.Thread(target=critical_section, args=(0, 1, -40))
        t2 = threading.Thread(target=critical_section, args=(1, 0, 25))
        t1.start(); t2.start(); t1.join(); t2.join()
        results.append(counter[0])

    print("Peterson-protected runs:", results)
    print("All equal 85:", all(v == 85 for v in results))
    return results


if __name__ == "__main__":
    unsynchronized_demo(5)
    peterson_demo(5)
