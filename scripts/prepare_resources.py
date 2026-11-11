"""Validate a complete BTEC snapshot; dispatch replaces resources.json atomically."""
import json
import os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def validate(rows):
    if not isinstance(rows, list):
        raise ValueError('resources must be a JSON array')
    units = {u['id'] for u in json.loads((ROOT / 'units.json').read_text())}
    result, seen = [], set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'Row {i}: expected object')
        if row.get('course', 'BTEC Sport') != 'BTEC Sport':
            raise ValueError(f'Row {i}: wrong course; refusing cross-hub content')
        if 'published' in row and row['published'] is not True:
            raise ValueError(f'Row {i}: unpublished item in publication payload')
        unit = row.get('unit')
        if type(unit) is not int or unit not in units:
            raise ValueError(f'Row {i}: unit must be an integer in units.json')
        out = {'unit': unit}
        for key in ['title', 'url', 'description', 'type']:
            value = row.get(key, '' if key == 'description' else None)
            if not isinstance(value, str) or (key != 'description' and not value.strip()):
                raise ValueError(f'Row {i}: invalid {key}')
            out[key] = value.strip()
        url = urlparse(out['url'])
        if url.scheme not in ('http', 'https') or not url.netloc or url.username or url.password:
            raise ValueError(f'Row {i}: URL must be an HTTP(S) link without embedded credentials')
        for key in ['learningAims', 'tags']:
            values = row.get(key, [])
            if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
                raise ValueError(f'Row {i}: {key} must be an array of non-empty strings')
            out[key] = list(dict.fromkeys(v.strip() for v in values))
        identity = (unit, out['title'], out['url'])
        if identity in seen:
            raise ValueError(f'Row {i}: duplicate resource')
        seen.add(identity)
        result.append(out)
    return result

if __name__ == '__main__':
    event = json.loads(Path(os.environ.get('GITHUB_EVENT_PATH', '/dev/null')).read_text() or '{}') if os.environ.get('GITHUB_EVENT_PATH') else {}
    dispatch = os.environ.get('GITHUB_EVENT_NAME') == 'repository_dispatch'
    payload = event.get('client_payload', {})
    if dispatch and 'resources' not in payload:
        raise ValueError('Dispatch missing resources; existing snapshot preserved')
    rows = payload['resources'] if dispatch else json.loads((ROOT / 'resources.json').read_text())
    validated = validate(rows)
    if dispatch and not validated and payload.get('allowEmpty') is not True:
        raise ValueError('Empty replacement requires client_payload.allowEmpty=true')
    tmp = ROOT / 'resources.json.tmp'
    tmp.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(ROOT / 'resources.json')
    print(f'Validated {len(validated)} BTEC resources')
