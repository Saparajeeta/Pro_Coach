import csv
import os
import sys


def compute_accuracy(csv_path):
    if not csv_path or not os.path.exists(csv_path):
        return {"message": f"File not found: {csv_path}"}

    if os.path.getsize(csv_path) == 0:
        return {"message": f"File is empty: {csv_path}"}

    required_columns = [
        "trial_id",
        "exercise",
        "true_reps_correct",
        "true_reps_incorrect",
        "system_reps_correct",
        "system_reps_incorrect",
        "true_mistake",
        "system_mistake",
    ]

    exercise_stats = {}
    with open(csv_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            return {"message": f"CSV file is empty: {csv_path}"}

        missing = [col for col in required_columns if col not in reader.fieldnames]
        if missing:
            return {"message": f"Missing required CSV columns: {', '.join(missing)}"}

        for row in reader:
            exercise = (row.get("exercise") or "").strip()
            if not exercise:
                continue

            stats = exercise_stats.setdefault(
                exercise,
                {"total": 0, "rep_matches": 0, "mistake_matches": 0},
            )
            stats["total"] += 1

            true_reps_correct = int(row.get("true_reps_correct", 0) or 0)
            true_reps_incorrect = int(row.get("true_reps_incorrect", 0) or 0)
            system_reps_correct = int(row.get("system_reps_correct", 0) or 0)
            system_reps_incorrect = int(row.get("system_reps_incorrect", 0) or 0)
            true_mistake = (row.get("true_mistake") or "").strip()
            system_mistake = (row.get("system_mistake") or "").strip()

            rep_match = (
                system_reps_correct == true_reps_correct
                and system_reps_incorrect == true_reps_incorrect
            )
            if rep_match:
                stats["rep_matches"] += 1

            if system_mistake == true_mistake:
                stats["mistake_matches"] += 1

    if not exercise_stats:
        return {"message": f"No exercise rows found in {csv_path}"}

    exercise_results = []
    rep_accuracies = []
    mistake_accuracies = []

    for exercise, stats in sorted(exercise_stats.items()):
        total = max(stats["total"], 1)
        rep_accuracy = (stats["rep_matches"] / total) * 100
        mistake_accuracy = (stats["mistake_matches"] / total) * 100
        exercise_results.append(
            {
                "exercise": exercise,
                "repetition_accuracy_percent": rep_accuracy,
                "mistake_accuracy_percent": mistake_accuracy,
                "total_trials": total,
            }
        )
        rep_accuracies.append(rep_accuracy)
        mistake_accuracies.append(mistake_accuracy)

    overall_rep = sum(rep_accuracies) / len(rep_accuracies)
    overall_mist = sum(mistake_accuracies) / len(mistake_accuracies)

    return {
        "exercise_results": exercise_results,
        "overall_repetition_accuracy_percent": overall_rep,
        "overall_mistake_accuracy_percent": overall_mist,
    }


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "evaluation/trials.csv"
    result = compute_accuracy(csv_path)
    print(result)
