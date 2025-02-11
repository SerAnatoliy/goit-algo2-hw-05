import json
import time
import unittest

import requests

from task2 import HyperLogLog


class TestHyperLogLogComparison(unittest.TestCase):
    def test_benchmark_comparison(self):
        log_url = "https://drive.google.com/file/d/13NUCSG7l_z2B7gYuQubYIpIjJTnwOAOb/view?usp=sharing"
        results = benchmark_comparison(log_url)

        print()
        print(f"Set execution time: {results['exact_time']:.5f} s")
        print(f"HLL execution time: {results['approximate_time']:.5f} s")

        self.assertGreater(results["exact_count"], 0)
        self.assertGreater(results["approximate_count"], 0)
        self.assertEqual(results["exact_count"], 28)
        self.assertLess(results["exact_time"], results["approximate_time"])
        self.assertAlmostEqual(results["exact_count"], results["approximate_count"],
                               delta=0.05 * results["exact_count"])


def load_data_from_drive(url):
    file_id = url.split('/d/')[1].split('/')[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    response.raise_for_status()
    return response.text


def extract_ips(log_data):
    ips = []
    for line in log_data.splitlines():
        try:
            log_entry = json.loads(line)
            ips.append(log_entry.get("remote_addr"))
        except json.JSONDecodeError:
            continue
    return ips


def count_unique_with_set(ip_addresses):
    unique_ips = set(ip_addresses)
    return len(unique_ips)


def count_unique_with_hll(ip_addresses):
    hll = HyperLogLog(p=14)
    for ip in ip_addresses:
        hll.add(ip)
    return hll.count()


def benchmark_comparison(log_url):
    log_data = load_data_from_drive(log_url)
    ip_addresses = extract_ips(log_data)

    start_time = time.time()
    exact_count = count_unique_with_set(ip_addresses)
    exact_time = time.time() - start_time

    start_time = time.time()
    approx_count = count_unique_with_hll(ip_addresses)
    approx_time = time.time() - start_time

    return {
        "exact_count": exact_count,
        "approximate_count": approx_count,
        "exact_time": exact_time,
        "approximate_time": approx_time,
    }


if __name__ == "__main__":
    unittest.main()