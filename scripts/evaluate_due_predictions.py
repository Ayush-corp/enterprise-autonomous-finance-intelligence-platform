from services.prediction_evaluator import PredictionEvaluator


def main() -> None:
    outcomes = PredictionEvaluator().evaluate_due_predictions()
    for outcome in outcomes:
        print(outcome.model_dump_json())


if __name__ == "__main__":
    main()
