#!/usr/bin/env python3
"""Check catalog links without changing their editorial review dates.

HTTP 403/429 and transient network errors are review warnings. Confirmed 404/410
responses fail the check. A reachable page is not proof of content quality.
"""
import concurrent.futures
import json
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def check(resource):
    result = {'id': resource['id'], 'url': resource['url']}
    try:
        request = Request(resource['url'].split('#')[0], headers={'User-Agent': 'BioinformaticsResources-LinkChecker/1.0'})
        with urlopen(request, timeout=25) as response:
            result.update(status=response.status, resolved=response.url)
    except HTTPError as error:
        result.update(status=error.code, error=str(error))
    except Exception as error:
        result.update(status=None, error=str(error))
    return result


if __name__ == '__main__':
    resources = json.loads((ROOT / 'content/catalog.json').read_text())['resources']
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, resources))
    print(json.dumps(results, indent=2))
    dead = [r for r in results if r['status'] in (404, 410)]
    warnings = [r for r in results if r['status'] is None or r['status'] >= 400]
    print(f'{len(results)} checked; {len(dead)} missing; {len(warnings)} require review.', file=sys.stderr)
    raise SystemExit(bool(dead))
