import json
import random
import mmh3
import math
import time


data_url = "./lms-stage-access.log"

with open(data_url) as f:
    data = f.readlines()
    json_data = [json.loads(line) for line in data]

    print("Line 1:  ", json_data[0])
    print("IP line 1: ", json_data[0]["remote_addr"])


def cardinality_exact_count(data_array):
    start_time = time.time()
    ips = set()
    for line in data_array:
        ips.add(line["remote_addr"])

    unique_ips_count = len(ips)

    end_time = time.time()
    execution_time = end_time - start_time
    return [unique_ips_count, execution_time]


class HyperLogLog:
    def __init__(self, p=5):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2  # threshold for small values

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0**-r for r in self.registers)
        E = self.alpha * self.m * self.m / Z

        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        return E


def cardinality_hyper_log_log(data_array):
    start_time = time.time()
    hll = HyperLogLog(p=16)
    for line in data_array:
        hll.add(line["remote_addr"])

    unique_ips_count = hll.count()

    end_time = time.time()
    execution_time = end_time - start_time
    return [unique_ips_count, execution_time]


if __name__ == "__main__":
    exact_count_results = cardinality_exact_count(json_data)
    hll_results = cardinality_hyper_log_log(json_data)
    print("-" * 100)
    print(f"Total number of records: {len(json_data)}")
    print("Results of comparison:")
    print(f"{'':<20} {'Cardinality':<20} {'Execution time':<20}")
    print(
        f"{"Exact count:":<20} {exact_count_results[0]:<20} {exact_count_results[1]:<20.5f}"
    )
    print(f"{"HyperLogLog:":<20} {hll_results[0]:<20.5f} {hll_results[1]:<20.5f}")
    print("-" * 100)
