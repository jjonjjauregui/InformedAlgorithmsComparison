import heapq
import time
import tracemalloc
from typing import Dict, Tuple, List, Optional, Any
import math  

def measure(func):
    """Decorator to measure time, memory (peak), and collect metrics dict from search functions."""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = func(*args, **kwargs)  
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        path, cost, metrics = result
        metrics = dict(metrics) if metrics else {}
        metrics.update({
            "time_sec": t1 - t0,
            "peak_mem_kb": peak / 1024.0,
        })
        return path, cost, metrics
    return wrapper


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datagraph3 import graph, h_values, start, goal

# Import Greedy algorithm and create wrapper
from Greedy_B import greedy_best_first_search as original_greedy
def greedy_best_first_search(graph, start_node, goal_node, h_values):
    path_and_metrics = original_greedy(graph, start_node, goal_node, h_values)
    if path_and_metrics and path_and_metrics[0]:
        path, metrics = path_and_metrics
        cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        metrics["path_len"] = len(path)-1
        return path, cost, metrics
    return [], float('inf'), {"expansions": 0, "generated": 0, "max_frontier": 0}

# Import IDA algorithm and create wrapper
from IDA_B import ida_star as original_ida
def ida_star(graph, start_node, goal_node, h_values):
    path_and_metrics = original_ida(graph, start_node, goal_node, h_values)
    if path_and_metrics and path_and_metrics[0]:
        path, metrics = path_and_metrics
        cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        metrics["path_len"] = len(path)-1
        return path, cost, metrics
    return [], float('inf'), {"expansions": 0, "generated": 0, "max_frontier": 0}

# Import Weighted A* algorithm and create wrapper
from Weighted_A import weighted_a_star_search as original_weighted_a
def weighted_a_star_search(graph, start_node, goal_node, h_values, weight=1.5):
    path_and_metrics = original_weighted_a(graph, start_node, goal_node, h_values, weight)
    if path_and_metrics and path_and_metrics[0]:
        path, metrics = path_and_metrics
        cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        metrics["path_len"] = len(path)-1
        return path, cost, metrics
    return [], float('inf'), {"expansions": 0, "generated": 0, "max_frontier": 0}


def run_all(graph, h, start, goal):
    results = []

    algorithms = [
        ("A*", weighted_a_star_search, {"graph": graph, "start_node": start, "goal_node": goal, "h_values": h, "weight": 1.0}),
        ("Weighted A* w=1.5", weighted_a_star_search, {"graph": graph, "start_node": start, "goal_node": goal, "h_values": h, "weight": 1.5}),
        ("Weighted A* w=3", weighted_a_star_search, {"graph": graph, "start_node": start, "goal_node": goal, "h_values": h, "weight": 3.0}),
        ("Greedy Best-First", greedy_best_first_search, {"graph": graph, "start_node": start, "goal_node": goal, "h_values": h}),
        ("IDA*", ida_star, {"graph": graph, "start_node": start, "goal_node": goal, "h_values": h}),
    ]

    for name, func, kwargs in algorithms:
        print(f"→ Running {name} ...")
        try:
            decorated_func = measure(func)
            path, cost, metrics = decorated_func(**kwargs)
        except Exception as e:
            print(f"⚠️  {name} failed: {e}")
            path, cost, metrics = [], float("inf"), {}
        metrics.update({"algorithm": name})
        results.append((path, cost, metrics))

    return results


def print_report(results):
    header = (
        f"{'ALGORITHM':<20} {'COST':>8} {'LEN':>5} "
        f"{'EXP':>6} {'GEN':>6} {'MAX_OPEN':>9} "
        f"{'TIME(s)':>9} {'PEAK(KB)':>10}"
    )
    print(header)
    print("-" * len(header))

    for path, cost, m in results:
        algoname   = str(m.get("algorithm", "?"))
        path_len   = int(m.get("path_len", len(path) if path else 0))
        expansions = m.get("expansions", "?")
        generated  = m.get("generated", "?")
        max_open   = m.get("max_frontier", m.get("max_open", "?"))

        # Cost string
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) and math.isfinite(cost) else "inf"

        # Safe numeric defaults
        time_sec = float(m.get("time_sec", 0) or 0)
        peak_kb  = float(m.get("peak_mem_kb", 0) or 0)

        print(f"{algoname:<20} "
              f"{cost_str:>8} "
              f"{path_len:>5} "
              f"{expansions:>6} {generated:>6} {max_open:>9} "
              f"{time_sec:9.6f} {peak_kb:10.1f}")

    print("\nBest paths:")
    for path, cost, m in results:
        algoname = str(m.get("algorithm", "?"))
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) and math.isfinite(cost) else str(cost)
        print(f"- {algoname}: cost={cost_str}  path={path}")

if __name__ == "__main__":
    results = run_all(graph, h_values, start, goal)
    print_report(results)