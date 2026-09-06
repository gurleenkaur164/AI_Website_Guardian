import json
import sys
import time
from main import run_agent

def load_dataset(path="eval_dataset.json"):
    with open(path, "r") as f:
        return json.load(f)

def run_evaluation(dataset_path="eval_dataset.json"):
    dataset = load_dataset(dataset_path)
    results = []
    intent_stats = {}

    print(f"Running evaluation on {len(dataset)} test cases...\n")

    for i, case in enumerate(dataset):
        message = case["message"]
        expected = case["expected_intent"]
        print(f"[{i+1}/{len(dataset)}] Testing: {message[:60]}...")

        start = time.time()
        try:
            result = run_agent(message)
            elapsed = time.time() - start
            detected = result.get("analysis", {}).get("intent", "unknown")
            confidence = result.get("analysis", {}).get("confidence")

            # For injection cases, check if the trace shows injection was caught
            if expected == "injection":
                trace_tools = [t["tool"] for t in result.get("trace", [])]
                injection_caught = any(
                    "BLOCKED" in str(t.get("result", ""))
                    for t in result.get("trace", [])
                    if t["tool"] == "check_prompt_injection"
                )
                if injection_caught:
                    detected = "injection"

            correct = detected == expected
        except Exception as e:
            elapsed = time.time() - start
            detected = "error"
            confidence = None
            correct = False
            print(f"  ERROR: {e}")

        entry = {
            "message": message,
            "expected": expected,
            "detected": detected,
            "confidence": confidence,
            "correct": correct,
            "time_seconds": round(elapsed, 2),
        }
        results.append(entry)

        status = "PASS" if correct else "FAIL"
        conf_str = f"{confidence}%" if confidence is not None else "N/A"
        print(f"  {status} | expected={expected}, got={detected}, confidence={conf_str}, time={elapsed:.1f}s\n")

        if expected not in intent_stats:
            intent_stats[expected] = {"total": 0, "correct": 0}
        intent_stats[expected]["total"] += 1
        if correct:
            intent_stats[expected]["correct"] += 1

    # Summary
    total = len(results)
    total_correct = sum(1 for r in results if r["correct"])
    accuracy = (total_correct / total * 100) if total else 0
    avg_time = sum(r["time_seconds"] for r in results) / total if total else 0

    print("=" * 60)
    print(f"OVERALL ACCURACY: {total_correct}/{total} ({accuracy:.1f}%)")
    print(f"AVERAGE TIME PER MESSAGE: {avg_time:.1f}s")
    print("=" * 60)

    print("\nPer-intent breakdown:")
    print(f"{'Intent':<15} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
    print("-" * 45)
    for intent, stats in sorted(intent_stats.items()):
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] else 0
        print(f"{intent:<15} {stats['correct']:<10} {stats['total']:<10} {acc:.1f}%")

    # Failures
    failures = [r for r in results if not r["correct"]]
    if failures:
        print(f"\nFailed cases ({len(failures)}):")
        for f in failures:
            print(f"  - \"{f['message'][:60]}\" expected={f['expected']}, got={f['detected']}")

    # Save report
    report = {
        "total": total,
        "correct": total_correct,
        "accuracy_percent": round(accuracy, 1),
        "avg_time_seconds": round(avg_time, 1),
        "per_intent": {k: {"accuracy": round(v["correct"]/v["total"]*100, 1), **v} for k, v in intent_stats.items()},
        "failures": failures,
        "results": results,
    }
    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nFull report saved to eval_report.json")

    return report

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "eval_dataset.json"
    run_evaluation(path)
