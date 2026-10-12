#!/usr/bin/env python3
"""Summarize the user's local, redacted seven-day observations. No uploads, no dependencies.

Usage: python3 tools/slo_report.py templates/七天测量表.csv

Only rows whose success fields are explicitly 0/1 enter denominators.
A result from 42 tests does not imply annual or country-wide performance.
"""
from __future__ import annotations
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    a = sorted(values)
    k = (len(a) - 1) * p / 100
    low, high = math.floor(k), math.ceil(k)
    return a[low] if low == high else a[low] * (high-k) + a[high] * (k-low)

def format_group(name: str, rows: list[dict[str,str]]) -> str:
    measured = [r for r in rows if r.get('核心任务成功(1/0)', '').strip() in ('0','1')]
    attempted = [r for r in rows if r.get('连接成功(1/0)', '').strip() in ('0','1')]
    success = sum(r['核心任务成功(1/0)'].strip() == '1' for r in measured)
    connected = sum(r['连接成功(1/0)'].strip() == '1' for r in attempted)
    latencies = []
    for r in measured:
        if r['核心任务成功(1/0)'].strip() != '1':
            continue
        try:
            x = float(r['核心任务耗时秒'])
            if math.isfinite(x) and x >= 0:
                latencies.append(x)
        except (ValueError, TypeError):
            pass
    denominator = len(measured)
    conn_denominator = len(attempted)
    pct = f'{success/denominator:.1%}' if denominator else '无法计算（未填）'
    conn = f'{connected/conn_denominator:.1%}' if conn_denominator else '无法计算（未填）'
    p95 = percentile(latencies,95)
    return (f'[{name}]\n'
            f'  采样点: 计划 {len(rows)}，实填核心任务 {denominator}（未填 {len(rows)-denominator}）\n'
            f'  连接成功: {connected}/{conn_denominator} = {conn}\n'
            f'  核心任务成功: {success}/{denominator} = {pct}\n'
            f'  成功任务耗时 p95: {p95:.2f}s (n={len(latencies)})' if p95 is not None else
            f'[{name}]\n  采样点: 计划 {len(rows)}，实填核心任务 {denominator}（未填 {len(rows)-denominator}）\n'
            f'  连接成功: {connected}/{conn_denominator} = {conn}\n'
            f'  核心任务成功: {success}/{denominator} = {pct}\n'
            f'  成功任务耗时 p95: 无有效耗时样本')

def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'templates'/'七天测量表.csv'
    try:
        with src.open('r',encoding='utf-8-sig',newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except (OSError, UnicodeError) as e:
        print('无法读取 CSV:',e,file=sys.stderr);return 1
    required={'接入网络','连接成功(1/0)','核心任务成功(1/0)','核心任务耗时秒'}
    if not required.issubset(set(reader.fieldnames or [])):
        print('缺少必要列：'+ ', '.join(sorted(required-set(reader.fieldnames or []))),file=sys.stderr);return 1
    print('七天 SLO 报告｜仅本地数据，不上传，不代表全年或全国可用性')
    print(format_group('总计',rows))
    groups=defaultdict(list)
    for r in rows:groups[r.get('接入网络','未知')].append(r)
    for name,rr in sorted(groups.items()):print(format_group(name or '未填写接入网络',rr))
    return 0
if __name__=='__main__':
    sys.exit(main())
