import re, datetime

def log_query(sql: str):
    with open("queries.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {sql}\n")

def is_suspicious(sql: str):
    patterns = [r"or\s+1=1", r"--", r"union", r"'.*'.*'.*'"]
    return [p for p in patterns if re.search(p, sql, re.IGNORECASE)]
