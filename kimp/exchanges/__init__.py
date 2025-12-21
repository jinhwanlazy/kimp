import importlib

__all__ = ["Upbit", "Binance", "BinanceFutures", "BinanceFuturesTestnet"]


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name == "Upbit":
        module = importlib.import_module(f"{__name__}.upbit")
    elif name == "Binance":
        module = importlib.import_module(f"{__name__}.binance")
    elif name == "BinanceFutures":
        module = importlib.import_module(f"{__name__}.binance_futures")
    elif name == "BinanceFuturesTestnet":
        module = importlib.import_module(f"{__name__}.binance_futures_testnet")
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    obj = getattr(module, name)
    globals()[name] = obj
    return obj


def __dir__():
    return sorted(list(globals().keys()) + __all__)


def create_exchange(name: str, *args, **kwargs):
    exchange_class = __getattr__(name)
    print(args, kwargs)
    return exchange_class(*args, **kwargs)
