"""Adds every common board subject (re-runnable; skips subjects that already exist). All new chapters are marked 'verify'."""
import json, re
from pathlib import Path
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
SEC = lambda *xs: list(xs)
HINDI10 = SEC('Kshitij / Sparsh: Gadya Khand', 'Kshitij / Sparsh: Kavya Khand', 'Kritika / Sanchayan', 'Vyakaran', 'Lekhan (Patra, Anuchchhed, Vigyapan)')
HINDI12 = SEC('Aroh: Kavya Khand', 'Aroh: Gadya Khand', 'Vitan', 'Abhivyakti aur Madhyam', 'Lekhan (Nibandh, Patra, Feature)')
UP_HINDI12 = SEC('Gadya Khand', 'Kavya Khand', 'Sanskrit Digdarshika', 'Kavya Saundarya (Ras, Chhand, Alankar)', 'Nibandh evam Patra Lekhan', 'Vyakaran')
BR_HINDI = SEC('Godhuli / Digant: Gadya Khand', 'Godhuli / Digant: Kavya Khand', 'Varnika / Antral', 'Vyakaran', 'Nibandh evam Patra Lekhan')
SANSKRIT = SEC('Gadya Bhag', 'Padya Bhag', 'Vyakaran (Sandhi, Samas, Karak, Pratyay)', 'Anuvad', 'Rachana (Patra, Anuchchhed)')
MARATHI = SEC('Kumarbharati / Yuvakbharati: Gadya', 'Padya', 'Upayojit Lekhan', 'Vyakaran', 'Sthulvachan')
MH_HINDI = SEC('Lokbharati / Yuvakbharati: Gadya', 'Padya', 'Vyakaran', 'Rachana Vibhag')
CS12 = ['Python Revision Tour', 'Working with Functions', 'Exception Handling', 'File Handling', 'Data Structure: Stack', 'Computer Networks',
        'Database Concepts', 'Structured Query Language (SQL)', 'Interface Python with MySQL']
PE12 = ['Management of Sporting Events', 'Children and Women in Sports', 'Yoga as Preventive Measure for Lifestyle Disease', 'Physical Education and Sports for CWSN',
        'Sports and Nutrition', 'Test and Measurement in Sports', 'Physiology and Injuries in Sports', 'Biomechanics and Sports', 'Psychology and Sports', 'Training in Sports']
SOC12 = ['Introducing Indian Society', 'The Demographic Structure of Indian Society', 'Social Institutions: Continuity and Change', 'The Market as a Social Institution',
         'Patterns of Social Inequality and Exclusion', 'The Challenges of Cultural Diversity', 'Structural Change', 'Cultural Change', 'Change and Development in Rural Society',
         'Change and Development in Industrial Society', 'Globalisation and Social Change', 'Mass Media and Communications', 'Social Movements']
PSY12 = ['Variations in Psychological Attributes', 'Self and Personality', 'Meeting Life Challenges', 'Psychological Disorders', 'Therapeutic Approaches',
         'Attitude and Social Cognition', 'Social Influence and Group Processes']
PHIL12 = SEC('Indian Philosophy: Schools and Thinkers', 'Western Philosophy: Major Thinkers', 'Logic', 'Ethics', 'Philosophy of Religion')
HOMESCI12 = SEC('Human Development', 'Food and Nutrition', 'Resource Management', 'Fabric and Apparel', 'Communication and Extension')
IT12 = SEC('Advanced Web Designing', 'Introduction to SEO', 'Advanced JavaScript', 'Emerging Technologies', 'Server Side Scripting (PHP)', 'E-Commerce and E-Governance')
MH_HISPOL10 = ['History: Historiography – Development in the West', 'History: Historiography – Indian Tradition', 'History: Applied History', 'History: History of Indian Arts',
               'History: Mass Media and History', 'History: Entertainment and History', 'History: Sports and History', 'History: Tourism and History', 'History: Heritage Management',
               'Political Science: Working of the Constitution', 'Political Science: The Electoral Process', 'Political Science: Political Parties',
               'Political Science: Social and Political Movements', 'Political Science: Challenges faced by Indian Democracy']
MH_GEO10 = ['Field Visit', 'Location and Extent', 'Physiography and Drainage', 'Climate', 'Natural Vegetation and Wildlife', 'Population', 'Human Settlements',
            'Economy and Occupations', 'Tourism, Transport and Communication']
MH_ARTS12 = {'History': SEC('Europe and India', 'Colonialism and Imperialism', 'India: Freedom Struggle', 'Post-Independence India', 'World after 1945'),
             'Geography': SEC('Population', 'Human Settlements', 'Primary, Secondary and Tertiary Activities', 'Regional Development', 'Purpose and Practice of Geography'),
             'Political Science': SEC('World Politics after Cold War', 'Contemporary Issues', 'Indian Democracy', 'India and the World', 'Good Governance'),
             'Psychology': SEC('Psychological Attributes', 'Self and Personality', 'Stress and Health', 'Psychological Disorders and Therapy', 'Social Psychology'),
             'Sociology': SEC('Indian Society: Structure', 'Social Change in India', 'Rural and Urban Society', 'Social Problems', 'Social Movements')}

ADD = {  # board: {class: {stream or '': {subject: chapters}}}
 'cbse': {'10': {'': {'Hindi': HINDI10, 'Sanskrit': SANSKRIT}},
          '12': {s: {'Hindi Core': HINDI12, 'Physical Education': PE12, **({'Computer Science': CS12} if s != 'arts' else {}), **({'Sociology': SOC12, 'Psychology': PSY12} if s == 'arts' else {})}
                 for s in ('science', 'commerce', 'arts')}},
 'up': {'10': {'': {'Sanskrit': SANSKRIT}},
        '12': {s: {'Samanya Hindi': UP_HINDI12, 'Sanskrit': SANSKRIT, **({'Sociology': SOC12, 'Psychology': PSY12} if s == 'arts' else {})} for s in ('science', 'commerce', 'arts')}},
 'bihar': {'10': {'': {'Hindi': BR_HINDI, 'Sanskrit': SANSKRIT}},
           '12': {s: {'Hindi': BR_HINDI, **({'Computer Science': CS12} if s == 'science' else {}),
                      **({'Sociology': SOC12, 'Psychology': PSY12, 'Philosophy': PHIL12, 'Home Science': HOMESCI12} if s == 'arts' else {})} for s in ('science', 'commerce', 'arts')}},
 'maharashtra': {'10': {'': {'Marathi': MARATHI, 'Hindi': MH_HINDI, 'History & Political Science': MH_HISPOL10, 'Geography': MH_GEO10}},
                 '12': {s: {'Marathi / Hindi (2nd language)': MARATHI, **({'Information Technology': IT12} if s != 'arts' else {}), **(MH_ARTS12 if s == 'arts' else {})}
                        for s in ('science', 'commerce', 'arts')}},
}
ADD['others'] = ADD['cbse']

idx = json.loads(Path('index.json').read_text())
board = next(c for c in idx['courses'] if c.get('id') == 'board')
added = 0
for lv in board['levels']:
    parts = lv['id'].split('-'); b, cls = parts[0], parts[1]; st = parts[2] if len(parts) > 2 else ''
    extra = ADD.get(b, {}).get(cls, {}).get(st, {})
    p = Path(lv['pack']); pk = json.loads(p.read_text())
    have = {s['name'] for s in pk['subjects']}
    langs = [n for n in extra if any(k in n for k in ('Hindi', 'Sanskrit', 'Marathi'))]
    for name in list(langs) + [n for n in extra if n not in langs]:
        if name in have: continue
        subj = {'id': slug(name), 'name': name, 'modules': [{'id': slug(m), 'name': m, 'topics': [], 'status': 'verify'} for m in extra[name]]}
        if name in langs:  # languages right after English
            pos = 1 if pk['subjects'] and pk['subjects'][0]['name'] == 'English' else 0
            pk['subjects'].insert(pos + sum(1 for s in pk['subjects'] if s['name'] in langs), subj)
        else:
            pk['subjects'].append(subj)
        added += 1
    pk['version'] = int(pk.get('version', 1)) + 1
    p.write_text(json.dumps(pk, ensure_ascii=False, indent=1))
    lv['version'] = pk['version']; lv['subjects'] = len(pk['subjects']); lv['chapters'] = sum(len(s['modules']) for s in pk['subjects'])
Path('index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1))
print(f'subjects added: {added} across {len(board["levels"])} packs')
for lv in board['levels'][:20]:
    print(f"  {lv['id']:<24} {lv['subjects']:>2} subjects · {lv['chapters']:>3} chapters")
