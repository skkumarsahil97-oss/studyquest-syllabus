"""CSV (questions_src/*.csv) -> questions/<course>-<level>/<subject>__<chapter>.json + questions/index.json"""
import csv, hashlib, json, re
from pathlib import Path
def slug(s): return re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', s.lower()))
packs, errors, seen = {}, [], set()
for f in sorted(Path('questions_src').glob('*.csv')):
    for n, r in enumerate(csv.DictReader(f.open(encoding='utf-8')), 2):
        r = {k.strip(): (v or '').strip() for k, v in r.items() if k}
        if not r.get('question') or not r.get('answer'):
            errors.append(f'{f.name}:{n} missing question/answer'); continue
        norm = re.sub(r'\s+', ' ', r['question'].lower())
        if norm in seen: errors.append(f'{f.name}:{n} duplicate question'); continue
        seen.add(norm)
        key = f"{r['course']}/{r['level']}/{slug(r['subject'])}/{slug(r['chapter'])}"
        p = packs.setdefault(key, {'course': r['course'], 'level': r['level'], 'subject': r['subject'], 'chapter': r['chapter'], 'items': []})
        p['items'].append({
            'id': hashlib.sha1(norm.encode()).hexdigest()[:10],
            'type': (r.get('type') or 'mcq').lower(),
            'q': r['question'], 'a': r['answer'],
            'd': [x for x in [r.get('d1', ''), r.get('d2', ''), r.get('d3', '')] if x],
            'exp': r.get('explanation', ''), 'diff': (r.get('difficulty') or 'medium').lower(),
            'marks': float(r.get('marks') or 1),
        })
index = {'version': 1, 'chapters': {}, 'counts': {}}
for key, p in packs.items():
    c, l, s, ch = key.split('/')
    path = f'questions/{c}-{l}/{s}__{ch}.json'
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(p, ensure_ascii=False, indent=1))
    index['chapters'][key] = path; index['counts'][key] = len(p['items'])
Path('questions').mkdir(exist_ok=True)
Path('questions/index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1))
print(f'chapters: {len(packs)} | questions: {sum(len(p["items"]) for p in packs.values())} | problems: {len(errors)}')
for e in errors[:20]: print('  ', e)
