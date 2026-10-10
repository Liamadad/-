import sys, re, json
sys.path.insert(0, '.')
from load import ngsl_rank, ecdict
from awl import SUBLISTS
import subjects

POS_MAP = {'a.': 'adj.', 'ad.': 'adv.', 'vt.': 'v.', 'vi.': 'v.', 's.': 'adj.'}
POS_RE = re.compile(r'^(n|v|vt|vi|a|adj|ad|adv|prep|conj|pron|num|int|art|aux|abbr|s)\.\s*')
SKIP_PREFIX = ('[', '【')

def short_meaning(tr, max_len=26):
    lines = [l.strip() for l in tr.replace('\\n', '\n').split('\n') if l.strip()]
    kept = []
    for l in lines:
        if l.startswith(SKIP_PREFIX):
            continue
        m = POS_RE.match(l)
        pos = ''
        body = l
        if m:
            pos = m.group(0).strip()
            pos = POS_MAP.get(pos, pos)
            body = l[m.end():]
        body = re.sub(r'\[[^\]]*\]', '', body)          # remove [domain] tags
        body = re.sub(r'（[^）]*）|\([^)]*\)', '', body)  # remove parenthetical notes
        senses = [s.strip(' ,，') for s in re.split(r'[;；,，]', body) if s.strip(' ,，')]
        senses = [s for s in senses if not re.search(r'的(过去式|过去分词|复数|现在分词|第三人称)', s)]
        if not senses:
            continue
        kept.append((pos, senses))
    # merge same pos
    merged = []
    for pos, senses in kept:
        for mp in merged:
            if mp[0] == pos:
                mp[1].extend(s for s in senses if s not in mp[1])
                break
        else:
            merged.append([pos, list(dict.fromkeys(senses))])
    out = []
    total = 0
    for pos, senses in merged[:2]:
        take = []
        for s in senses[:3]:
            if total + len(s) > max_len and take:
                break
            take.append(s)
            total += len(s) + 1
        if take:
            out.append((pos + ' ' if pos else '') + '，'.join(take))
        if total >= max_len:
            break
    return '；'.join(out)

def is_word(w):
    return re.fullmatch(r"[a-z]+(-[a-z]+)?", w) is not None

def main():
    rank = ngsl_rank()
    ec = ecdict()
    ngsl_sorted = [w for w, k in sorted(rank.items(), key=lambda x: x[1])]
    ngsl_set = {w.lower() for w in ngsl_sorted}
    awl = [w for s in SUBLISTS for w in s]
    awl_set = set(awl)

    MANUAL = {'core': ['core', "kɒ:", 'n. 核心，要点；adj. 核心的']}
    def entry(w):
        if w in MANUAL:
            return list(MANUAL[w])
        row = ec.get(w) or ec.get(w.lower())
        if not row:
            return None
        mean = short_meaning(row['translation'])
        if not mean:
            return None
        ph = row['phonetic'].strip()
        return [w, ph, mean]

    missing_awl = [w for w in awl if entry(w) is None]
    print('AWL missing in dict:', missing_awl)

    SPELL_TOTAL = 44 * 5 * 10 + 6 * 5 * 5 + 9 * 5 * 5

    # --- recognition list: NGSL rank 501+ (not AWL), then IELTS words by frequency
    REC_TOTAL = 44 * 5 * 20 + 6 * 5 * 10 + 9 * 5 * 10
    rec = []
    rused = set()
    US_ONLY = {'democrat', 'republican', 'congress', 'congressional', 'catholic', 'baseball', 'senator', 'cop'}
    STOP = {'ken', 'york', 'hello', 'alright', 'okay', 'yeah', 'hi', 'bye', 'million', 'thousand', 'hundred', 'billion', 'third'}
    for w in ngsl_sorted[500:]:
        lw = w.lower()
        if lw != w or not is_word(lw) or lw in awl_set or lw in rused or lw in STOP:
            continue
        e = entry(lw)
        if not e:
            continue
        rec.append(e); rused.add(lw)
    n_ngsl_rec = len(rec)
    cands = []
    for w, row in ec.items():
        tags = row['tag'].split()
        if 'ielts' not in tags and 'toefl' not in tags:
            continue
        if not is_word(w) or len(w) < 3:
            continue
        if w in ngsl_set or w in awl_set or w in rused:
            continue
        if row['exchange'].startswith('0:') or '/0:' in row['exchange']:
            continue
        tr = row['translation']
        if '人名' in tr[:12] or '地名' in tr[:12] or tr.startswith('abbr'):
            continue
        if w in STOP or w in US_ONLY:
            continue
        frq = int(row['frq'] or 0); bnc = int(row['bnc'] or 0)
        # average of the American (COCA) and British (BNC) frequency ranks when both exist
        key = (frq + bnc) / 2 if frq > 0 and bnc > 0 else (frq or bnc or 10**7)
        cands.append((key, w))
    cands.sort()
    n_ielts_pool = len(cands)
    for key, w in cands:
        if len(rec) >= REC_TOTAL + 1500:   # headroom: the subject merge moves some words out
            break
        e = entry(w)
        if not e:
            continue
        rec.append(e); rused.add(w)
    print('rec pool', len(rec), 'from NGSL', n_ngsl_rec, 'ielts pool', n_ielts_pool)

    # --- subject words (IGCSE Economics, Physics, Maths, exam command words) merged in by importance;
    # spelling phase 1 = command words + subject terms + AWL, see subjects.py
    spell, rec = subjects.build(SUBLISTS, entry, rec, n_ngsl_rec, entry, ec, REC_TOTAL)
    n_phase1 = len(spell)
    print('rec total', len(rec), 'spell phase 1', n_phase1)

    # --- spelling phase 2: words already met in the recognition list, in that order (5+ letters)
    used = {e[0] for e in spell}
    rec_pos = {}
    for i, e in enumerate(rec):
        w = e[0]
        if len(spell) >= SPELL_TOTAL:
            break
        if len(w) < 5 or w in used or not is_word(w) or '-' in w:
            continue
        spell.append(list(e)); used.add(w); rec_pos[w] = i
    print('spell total', len(spell), 'phase 1', n_phase1, 'phase2 last rec index', max(rec_pos.values()))
    overlap = {e[0] for e in spell} & {e[0] for e in rec}
    print('spell/rec overlap', len(overlap))
    json.dump({'S': spell, 'R': rec}, open('words.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    main()
