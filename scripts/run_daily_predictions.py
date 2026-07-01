from services.prediction_scheduler import PredictionScheduler


def main() -> None:
    run = PredictionScheduler().run_daily_prediction_job()
    print(run.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
