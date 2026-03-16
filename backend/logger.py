import time

def log(msg: str, level: str = "INFO"):
    tag = {
        "INFO": "\033[36mINFO\033[0m",
        "OK":   "\033[32m OK \033[0m",
        "WARN": "\033[33mWARN\033[0m",
        "ERR":  "\033[31m ERR\033[0m",
    }.get(level, level)
    ts = time.strftime("%H:%M:%S")
    print(f"  [{ts}] [{tag}] {msg}", flush=True)
