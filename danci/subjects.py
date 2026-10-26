"""Subject vocabulary: Cambridge IGCSE Economics (0455), Physics (0625), Mathematics (0580), Computer Science (0478)
and the exam command words, merged into the general word lists by importance.

Each file in subjects/ is a list of {w, pos, zh, cls, tier, topic}: cls S = must spell (默写),
R = recognise (认识); tier 1 = in almost every paper, 2 = regular topic term, 3 = minor.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
# econ_class: the economics word list the teacher assigns (10 pages a week), in the book's page order; it comes first
SOURCES = [('econ_class', '经济'), ('command', '指令词'), ('econ', '经济'), ('physics', '物理'), ('math', '数学'), ('cs', '计算机')]
# phonetics ECDICT lacks (inflected forms, units), in its notation
MANUAL_PH = {'pascal': "'pæskәl", 'minimise': "'minimaiz", 'conserved': "kәn'sә:vd", 'responsiveness': "ri'spɒnsivnis",
             'diverging': "dai'vә:dʒiŋ", 'derived': "di'raivd", 'alternating': "'ɒ:ltәneitiŋ", 'purchasing': "'pә:tʃәsiŋ",
             'interquartile': ".intә'kwɒ:tail", 'competitiveness': "kәm'petitivnis", 'supplied': "sә'plaid",
             'inversely': "in'vә:sli", 'sightedness': "'saitidnis", 'emitting': "i'mitiŋ", 'recurring': "ri'kә:riŋ",
             'grouped': "gru:pt", 'curved': "kә:vd", 'expected': "ik'spektid", 'simplest': "'simplist",
             'emerging': "i'mә:dʒiŋ", 'nearest': "'niәrist", 'interior': "in'tiәriә", 'co': "kәu",
             'takeover': "'teik.әuvә", 'allocative': "'ælәkeitiv", 'ceteris': "'ketәris", 'paribus': "'pærәbәs",
             'crowding': "'kraudiŋ", 'managed': "'mænidʒd", 'gdp': "dʒi: di: 'pi:",
             # computer science words ECDICT lacks; acronyms inside phrases are read as letters
             "two's": "tu:z", 'unicode': "'ju:nikәud", 'checksum': "'tʃeksʌm", 'malware': "'mælwєә", 'firewall': "'faiәwɒ:l",
             'pseudocode': "'sju:dәukәud", 'boolean': "'bu:liәn", 'metadata': "'metәdeitә", 'mebibyte': "'mebibait",
             'gibibyte': "'ɡibibait", 'tebibyte': "'tebibait", 'timeout': "'taimaut", 'plaintext': "'pleintekst",
             'von': "vɒn", 'neumann': "'nɔimәn", 'inkjet': "'iŋkdʒet", 'hypertext': "'haipәtekst", 'blockchain': "'blɒktʃein",
             'cryptocurrency': "'kriptәu.kʌrәnsi", 'spyware': "'spaiwєә", 'adware': "'ædwєә", 'ransomware': "'rænsәmwєә",
             'pharming': "'fɑ:miŋ", 'automated': "'ɔ:tәmeitid", 'structured': "'strʌktʃәd", 'totalling': "'tәutәliŋ",
             'mac': "mæk", 'ip': "ai 'pi:", 'qr': "kju: 'ɑ:", '3d': "θri: 'di:"}
POS_SHOW = {'n.': 'n.', 'v.': 'v.', 'adj.': 'adj.', 'adv.': 'adv.', 'phr.': ''}


def load():
    out = {}
    for key, tag in SOURCES:
        rows = json.load(open(os.path.join(HERE, 'subjects', key + '.json'), encoding='utf-8'))
        for e in rows:
            e['src'], e['tag'] = key, tag
            # minor terms only need recognising; keeps the spelling load on what exams make students write
            if e['tier'] == 3 and key not in ('command', 'econ_class'):
                e['cls'] = 'R'
            # physics: only the core terms are spelt, like the class list's option C, so a chapter takes days, not weeks
            if key == 'physics' and e['tier'] == 2:
                e['cls'] = 'R'
        out[key] = rows
    return out


def spread(*lists):
    """Interleave lists evenly by relative position, so every day gets a share of each source."""
    keyed = []
    for li, items in enumerate(lists):
        n = len(items)
        keyed += [((i + 0.5) / n, li, x) for i, x in enumerate(items)]
    keyed.sort(key=lambda t: (t[0], t[1]))
    return [x for _, _, x in keyed]


def phonetic(w, ec):
    """Dictionary phonetic for a word; for a phrase, the phonetics of its words.
    Tries the British spelling's American form and the singular, which is how ECDICT lists many words."""
    if w.isupper():
        return ''                      # acronyms are read letter by letter
    out = []
    for p in [p for p in re.split(r'[ \-–]+', w) if p]:
        if p.isupper() and p.lower() not in MANUAL_PH:
            return ''
        cands = [p, p.lower(), p.capitalize()]
        for a, b in (('isation', 'ization'), ('ise', 'ize'), ('ised', 'ized'), ('yse', 'yze'), ('our', 'or'), ('tre', 'ter'), ('ogue', 'og')):
            if a in p:
                cands.append(p.replace(a, b))
        for c in list(cands):
            if c.endswith('ies'):
                cands.append(c[:-3] + 'y')
            if c.endswith('es'):
                cands.append(c[:-2])
            if c.endswith('s'):
                cands.append(c[:-1])
        if p.lower() in MANUAL_PH:
            out.append(MANUAL_PH[p.lower()]); continue
        row = next((ec[c] for c in cands if c in ec and ec[c]['phonetic'].strip()), None)
        if not row:
            return ''
        out.append(row['phonetic'].strip())
    return ' '.join(out)


def merge_meaning(subject_parts, general):
    """Subject meanings first (tagged with the subject), then whatever the general meaning adds."""
    # the same sense in two subjects becomes one item with both tags: 体积，容积（物理、数学）
    first = lambda z: re.split('[，；（]', z)[0]
    items = []
    for pos, zh, tag in subject_parts:
        for it in items:
            if it[0] == pos and first(it[1]) == first(zh):
                it[1] = max(it[1], zh, key=len)
                if tag not in it[2]:
                    it[2].append(tag)
                break
        else:
            items.append([pos, zh, [tag]])
    text = '；'.join(f"{pos} {zh}（{'、'.join(tags)}）".strip() for pos, zh, tags in items)
    if not general:
        return text
    covered = ''.join(zh for _, zh, _ in subject_parts)
    rest = []
    for group in general.split('；'):
        m = re.match(r'^((?:n|v|adj|adv|prep|conj|pron|num|int|pl|abbr)\.\s*)?(.*)$', group)
        pos, body = (m.group(1) or ''), m.group(2)
        senses = [s for s in body.split('，') if s and s not in covered and not any(s in z or z in s for z in covered.split('，'))]
        if senses:
            rest.append(pos + '，'.join(senses[:2]))
    for g in rest:
        if len(text) + len(g) + 1 > 32:
            break
        text += '；' + g
    return text


def build(awl_sublists, spell_entry, rec, n_ngsl, entry, ec, rec_total):
    """Return the spelling list before phase-2 upgrades, and the final recognition list.

    awl_sublists: the AWL headwords per sublist; spell_entry(w) -> [w, phonetic, meaning]
    rec: the general recognition list in its original order, with headroom past rec_total;
    its first n_ngsl entries come from the NGSL, the rest from the IELTS/TOEFL pool.
    """
    subj = load()
    general = {e[0]: e for e in rec}
    for sub in awl_sublists:
        for w in sub:
            e = spell_entry(w)
            if e:
                general[w] = e

    # one record per term, even when two subjects (or a subject and the command words) share it
    terms = {}
    for key, _ in SOURCES:
        for e in subj[key]:
            k = e['w'] if e['w'].isupper() else e['w'].lower()
            t = terms.setdefault(k, {'w': e['w'], 'parts': [], 'cls': 'R', 'tier': 3})
            t['parts'].append((POS_SHOW.get(e['pos'], e['pos']), e['zh'], e['tag']))
            if e['cls'] == 'S':
                t['cls'] = 'S'
            t['tier'] = min(t['tier'], e['tier'])
    # the teacher's economics list decides 默写 / 认识 for its own words
    for e in subj['econ_class']:
        k = e['w'] if e['w'].isupper() else e['w'].lower()
        terms[k]['cls'] = e['cls']

    def term_entry(k):
        t = terms[k]
        g = general.get(k)
        ph = g[1] if g and g[1] else phonetic(t['w'], ec)
        return [t['w'], ph, merge_meaning(t['parts'], g[2] if g else '')]

    def final(k):
        return term_entry(k) if k in terms else general.get(k) or spell_entry(k)

    def pick(src, cls, tiers):
        seen, out = set(), []
        for e in subj[src]:
            k = e['w'] if e['w'].isupper() else e['w'].lower()
            t = terms[k]
            if t['cls'] == cls and t['tier'] in tiers and k not in seen:
                seen.add(k); out.append(k)
        return out

    # --- from 10-26, before the midterm: the days already studied keep their words; after them every physics word
    # comes first, chapter by chapter, with a share of computer science (from its chapter 1) and the exam command words;
    # economics, maths and general English wait
    learned = json.load(open(os.path.join(HERE, 'subjects', 'learned.json'), encoding='utf-8'))
    tags = lambda k: {p[2] for p in terms[k]['parts']} if k in terms else set()
    key = lambda e: e['w'] if e['w'].isupper() else e['w'].lower()
    # physics in the coursebook's order: its chapters 1–5 (the midterm revision covers units 1–5) hold syllabus 1.1–1.6
    # and 1.8; energy, 1.7, is chapters 6–8
    book = lambda e: float(e['topic'].split()[0].replace('1.7', '1.85'))
    sect, cs_at = {}, {}
    for i, e in enumerate(sorted(subj['physics'], key=book)):
        sect.setdefault(key(e), i)
    for i, e in enumerate(subj['cs']):                 # the file is in the coursebook's order
        cs_at.setdefault(key(e), i)

    def midterm(order, done, n_phys, n_cs=0, n_cmd=0):
        """done, then a block of n_phys physics terms a day with n_cs computer science terms and n_cmd exam command words,
        then the rest in order."""
        done_set = set(done)
        rest = [k for k in dict.fromkeys(order) if k not in done_set]
        phys = sorted((k for k in rest if '物理' in tags(k)), key=sect.get)
        days = len(phys) / n_phys
        cs = sorted((k for k in rest if '计算机' in tags(k) and '物理' not in tags(k)), key=cs_at.get)
        cmd = [k for k in rest if '指令词' in tags(k) and not tags(k) & {'物理', '经济', '计算机'}]
        block = spread(phys, cs[:round(days * n_cs)], cmd[:round(days * n_cmd)])
        return list(dict.fromkeys(done + block + rest))

    # --- spelling: the teacher's economics words first (in page order), then command words and core subject terms
    s_order = pick('econ_class', 'S', {1, 2, 3})
    s_order += spread(pick('command', 'S', {1, 2, 3}), pick('econ', 'S', {1}), pick('physics', 'S', {1}),
                     pick('math', 'S', {1}), pick('cs', 'S', {1}), list(awl_sublists[0]))
    s_order += spread(pick('econ', 'S', {2}), pick('physics', 'S', {2}), pick('math', 'S', {2}), pick('cs', 'S', {2}),
                      [w for sub in awl_sublists[1:4] for w in sub])
    s_order += [w for sub in awl_sublists[4:] for w in sub]
    s_order = midterm(s_order, learned['S'], 7, 2, 1)
    spell, used = [], set()
    for k in s_order:
        if k in used:
            continue
        e = final(k)
        if e:
            spell.append(e); used.add(k)

    # --- recognition: subject terms spread through the general words of the same importance
    ngsl = [e[0] for e in rec[:n_ngsl]]
    ielts = [e[0] for e in rec[n_ngsl:]]
    r_subj = lambda tier: spread(*[pick(src, 'R', {tier}) for src in ('econ', 'physics', 'math', 'cs')])
    r1, r2, r3 = r_subj(1), r_subj(2), r_subj(3)
    r_order = pick('econ_class', 'R', {1, 2, 3}) + spread(r1, ngsl[:500]) + spread(r2, ngsl[500:])
    seen = set(used)
    head = [k for k in r_order if not (k in seen or seen.add(k))]
    r3 = [k for k in r3 if k not in seen]
    room = rec_total - len(head) - len(r3)
    tail_pool = [k for k in ielts if k not in seen and k not in set(r3)][:max(room, 0)]
    for k in spread(r3, tail_pool):
        if k not in seen:
            seen.add(k); head.append(k)
    recs = [final(k) for k in midterm(head, learned['R'], 15, 5)][:rec_total]
    return spell, recs
