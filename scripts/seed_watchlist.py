from services.watchlist_service import WatchlistService


def main() -> None:
    symbols = WatchlistService().seed_default_watchlist()
    for symbol in symbols:
        print(f"{symbol.symbol} {symbol.country} active={symbol.is_active}")


if __name__ == "__main__":
    main()
