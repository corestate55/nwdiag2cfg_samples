#!/usr/bin/env python3
"""drawio_nwdiag_extract.py

物理・論理合成図（drawio）を、コンフィグ生成用の構造化データに変換する補助スクリプト。

使い方:
  python3 drawio_nwdiag_extract.py <file.drawio.svg|file.drawio|file.xml>            # ページ一覧
  python3 drawio_nwdiag_extract.py <file> --page "<ページ名>" [--json out.json] [--md out.md]

出力（--md）:
  1. 機器（ホスト名・機種・枠の座標）
  2. 機器ごとの要素（ポート / Port-channel / セグメント横線 / IPバッジ / ルーティング箱 / vrf箱）
  3. 物理リンク（ポート同士の線。線幅・端点記号つき）
  4. 論理接続（ポート・Po・GRT とセグメント横線をつなぐ線）
  5. セグメント横線 → ラベル（VLAN名・ID・CIDR）の対応
  6. 冗長ペア（VRRP/HSRP の太線・vipラベル）
  7. 機械チェックで見つかった不整合の候補（WARN）
     HOSTNAME_DUP(N-01) / DEVICE_NO_BOX / EDGE_DANGLING(P-01。機器・サーバー・VM の中の線も対象)
     PORT_MULTI_LINK(P-02) / SPEED_MISMATCH(P-03) / CIDR_CONFLICT(A-01)
     LINE_COLOR_MISMATCH(D-03: 所属線の色と横線の色が違う) / EDGE_TO_LABEL(D-04: 線が横線でなくラベルに接続)

※ 判定はヒューリスティック。最終判断は図の目視とナレッジ文書のルールで行うこと。
標準ライブラリだけで動く（Python 3.8+）。
"""
import sys, re, html, json, base64, zlib, argparse, urllib.parse
import xml.etree.ElementTree as ET

PORT_RE = re.compile(r'^(Te|Tw|Fo|Hu|Gi|Fa|Eth|Et|xe|ge|et|mgmt|Mgmt|MGMT|BMC|eth|ens|eno|bond|Po|ae|lag|Vl|vlan|Lo|wan|lan|port)[\w/\-\.:]*', re.I)
PO_RE = re.compile(r'^(Po|Port-channel|ae|lag|bond)\d+', re.I)
IP_BADGE_RE = re.compile(r'^(\.?\d{1,3}(-\d{1,3})?|\.[a-z](\+\d+)?|\d{1,3}(\.\d{1,3}){3}(/\d+)?)$', re.I)
CIDR_RE = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2})')
VLAN_RE = re.compile(r'VLAN\s*(\d+(?:\s*-\s*\d+)?)', re.I)
HOST_RE = re.compile(r'^[a-z0-9][a-z0-9\-_]*\d\d', re.I)
# ホスト名: 英字で始まり、ハイフンの後ろに英字を含み、数字で終わる（例 tk1-core01, os1-fmacc02）
HOSTNAME_RE = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*-[a-z]+[a-z0-9]*\d+([A-Z].*)?$', re.I)


def load_mxfile(path):
    src = open(path, encoding='utf-8').read()
    if src.lstrip().startswith('<mxfile'):
        return ET.fromstring(src)
    m = re.search(r'content="([^"]*)"', src)
    if not m:
        raise SystemExit('drawio データ（content 属性 / mxfile）が見つかりません')
    return ET.fromstring(html.unescape(m.group(1)))


def page_model(diagram):
    m = diagram.find('mxGraphModel')
    if m is not None:
        return m
    data = (diagram.text or '').strip()
    raw = zlib.decompress(base64.b64decode(data), -15).decode('utf-8')
    return ET.fromstring(urllib.parse.unquote(raw))


def sty(s):
    d = {}
    for kv in (s or '').split(';'):
        if '=' in kv:
            k, v = kv.split('=', 1); d[k] = v
        elif kv:
            d[kv] = ''
    return d


def txt(v):
    v = re.sub(r'<br\s*/?>|</div>|</p>', ' / ', v or '')
    v = re.sub(r'<[^>]+>', '', v)
    return re.sub(r'\s+', ' ', html.unescape(v)).strip(' /')


class Page:
    def __init__(self, model):
        self.items = {}
        order = []
        for el in model.find('root'):
            if el.tag == 'mxCell':
                c, label, extra = el, el.get('value'), {}
            else:  # object / UserObject: カスタム属性を保持
                c = el.find('mxCell'); label = el.get('label')
                extra = {k: v for k, v in el.attrib.items() if k not in ('id', 'label', 'placeholders')}
            iid = el.get('id')
            self.items[iid] = dict(id=iid, text=txt(label), cell=c, style=sty(c.get('style')),
                                   props=extra, edge=c.get('edge') == '1', vertex=c.get('vertex') == '1',
                                   parent=c.get('parent'), source=c.get('source'), target=c.get('target'))
            order.append(iid)
        self.order = order
        for it in self.items.values():
            it['rect'] = self._rect(it) if it['vertex'] else None

    def _abs(self, it):
        x = y = 0; seen = set()
        while it is not None and it['id'] not in seen:
            seen.add(it['id']); g = it['cell'].find('mxGeometry')
            if g is not None and g.get('relative') != '1' and not it['edge']:
                x += float(g.get('x', 0)); y += float(g.get('y', 0))
            it = self.items.get(it['parent']) if it['parent'] else None
        return x, y

    def _rect(self, it):
        g = it['cell'].find('mxGeometry')
        if g is None or g.get('relative') == '1':
            return None
        x, y = self._abs(it)
        return (x, y, float(g.get('width', 0)), float(g.get('height', 0)))

    def color(self, it):
        s = it['style']
        for k in ('fillColor', 'strokeColor'):
            v = s.get(k, '')
            if v and v.lower() not in ('none', 'default', '#ffffff', '#000000', '#f5f5f5', 'light-dark(#ffffff,#121212)'):
                return v.upper()
        return ''


def overlap(a, b):
    return not (a[0] + a[2] < b[0] or b[0] + b[2] < a[0] or a[1] + a[3] < b[1] or b[1] + b[3] < a[1])


def center_in(r, b):
    cx, cy = r[0] + r[2] / 2, r[1] + r[3] / 2
    return b[0] <= cx <= b[0] + b[2] and b[1] <= cy <= b[1] + b[3]


def analyze(p):
    V = [it for it in p.items.values() if it['vertex'] and it['rect']]
    # --- 機器: 「hostname / model」形式のテキストと、それに重なる最小の枠 ---
    hosts = [it for it in V if HOSTNAME_RE.match(it['text'].split(' ')[0])
             and not CIDR_RE.search(it['text']) and not VLAN_RE.search(it['text']) and not PORT_RE.match(it['text'])]
    devices = []
    for h in hosts:
        best = None
        for v in V:
            if v is h or v['text']: continue
            x, y, w, hh = v['rect']
            if w < 120 or hh < 80 or 'text' in v['style']: continue
            if overlap(h['rect'], v['rect']):
                if best is None or w * hh < best['rect'][2] * best['rect'][3]:
                    best = v
        parts = [s.strip() for s in re.split(r' / |\n', h['text']) if s.strip()]
        name = parts[0]
        m = re.match(r'^(\S+?)(C社.*|[A-Z].*社.*)$', name)  # 「os1-core01C社 L3switch」のような改行欠落
        model = ' '.join(parts[1:])
        if m and not model:
            name, model = m.group(1), m.group(2)
        devices.append(dict(name=name, uid=name, model=model, label_id=h['id'], box=best['rect'] if best else None,
                            box_id=best['id'] if best else None))
    # 同名の機器は uid に #2, #3 を付けて区別する（ホスト名重複は WARN で報告）
    cnt = {}
    for dv in devices:
        cnt[dv['name']] = cnt.get(dv['name'], 0) + 1
        if cnt[dv['name']] > 1: dv['uid'] = '%s#%d' % (dv['name'], cnt[dv['name']])
    def owner(it):
        r = it['rect']
        if r is None: return None
        cands = [d for d in devices if d['box'] and center_in(r, d['box']) and it['id'] != d['box_id']]
        if not cands: return None
        return min(cands, key=lambda d: d['box'][2] * d['box'][3])['uid']

    def kind(it):
        t = it['text']; s = it['style']; r = it['rect']
        if it['edge']: return 'edge'
        if r is None: return 'edgelabel'
        if any(d['label_id'] == it['id'] for d in devices): return 'hostlabel'
        if t in ('GRT',) or re.match(r'^(vrf|VRF)\b', t) or t.lower().startswith('vrf'): return 'routing'
        if PO_RE.match(t): return 'portchannel'
        if CIDR_RE.search(t) or VLAN_RE.search(t): return 'seglabel'
        if PORT_RE.match(t) and r[2] <= 140: return 'port'
        if re.match(r'^vip\b', t, re.I): return 'vip'
        if IP_BADGE_RE.match(t) and p.color(it): return 'ipbadge'
        if not t and r[3] <= 14 and r[2] >= 40 and p.color(it): return 'segment'
        if CIDR_RE.search(t) or VLAN_RE.search(t): return 'seglabel'
        if t: return 'text'
        return 'shape'

    for it in p.items.values():
        it['kind'] = kind(it)
        it['owner'] = owner(it) if it['rect'] else None

    def d(i):
        it = p.items.get(i)
        if it is None: return {'id': i, 'kind': 'MISSING'}
        return {'id': i, 'kind': it['kind'], 'text': it['text'], 'owner': it['owner'], 'color': p.color(it)}

    phys, logical, seglabels, pairs, others = [], [], [], [], []
    for it in p.items.values():
        if not it['edge']: continue
        s, t = d(it['source']) if it['source'] else None, d(it['target']) if it['target'] else None
        st = it['style']
        e = dict(id=it['id'], a=s, b=t, color=p.color(it), width=st.get('strokeWidth', '1'),
                 start=(st.get('startArrow', 'none'), st.get('startFill', '1')),
                 end=(st.get('endArrow', 'classic'), st.get('endFill', '1')),
                 dashed=st.get('dashed') == '1', label=it['text'])
        ks = {s['kind'] if s else None, t['kind'] if t else None}
        if s is None and t is None:
            e['problem'] = 'free'; others.append(e)  # 凡例の線や、端点を接続せずに描いた線（冗長ペア線など）
        elif s is None or t is None or 'MISSING' in ks:
            e['problem'] = 'dangling'
            e['free_end'] = free_end(p, it, 'sourcePoint' if s is None else 'targetPoint')
            e['near'] = nearest(p, e['free_end'])
            others.append(e)
        elif 'seglabel' in ks and ks & {'port', 'portchannel', 'routing', 'ipbadge'}:
            e['problem'] = 'to_label'; others.append(e)  # 横線ではなくラベルに接続（D-04）
        elif ks <= {'port', 'shape', 'text', 'portchannel'} and s['owner'] != t['owner']:
            phys.append(e)
        elif 'segment' in ks and 'seglabel' in ks:
            seglabels.append(e)
        elif 'segment' in ks:
            logical.append(e)
        elif s['kind'] == 'routing' and t['kind'] == 'routing':
            pairs.append(e)
        else:
            others.append(e)
    elements = [dict(id=it['id'], kind=it['kind'], text=it['text'], owner=it['owner'], color=p.color(it),
                     rect=it['rect'], props=it['props'])
                for it in p.items.values() if it['vertex'] and it['kind'] not in ('shape',) and it['rect']]
    return dict(devices=devices, elements=elements, physical=phys, logical=logical,
                seglabels=seglabels, pairs=pairs, others=others, warns=checks(devices, elements, phys, others, logical))


def free_end(p, it, which):
    """未接続の端点の絶対座標（mxPoint as=sourcePoint/targetPoint）。無ければ None"""
    g = it['cell'].find('mxGeometry')
    if g is None: return None
    for pt in g.findall('mxPoint'):
        if pt.get('as') == which:
            par = p.items.get(it['parent'])
            ox, oy = p._abs(par) if par else (0, 0)
            return (ox + float(pt.get('x', 0)), oy + float(pt.get('y', 0)))
    return None


def nearest(p, pt, limit=60):
    """未接続端点の近くにある要素（接続先の推定候補。ナレッジ 6.5）"""
    if pt is None: return None
    best = None
    for it in p.items.values():
        r = it.get('rect')
        if not r or it.get('kind') not in ('port', 'portchannel', 'segment', 'routing', 'seglabel', 'text'): continue
        dx = max(r[0] - pt[0], 0, pt[0] - (r[0] + r[2])); dy = max(r[1] - pt[1], 0, pt[1] - (r[1] + r[3]))
        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= limit and (best is None or dist < best[0]):
            best = (dist, it)
    if not best: return None
    it = best[1]
    return dict(id=it['id'], kind=it['kind'], text=it['text'], owner=it['owner'], dist=round(best[0], 1))


def checks(devices, elements, phys, others, logical=()):
    w = []
    names = {}
    for dv in devices:
        names.setdefault(dv['name'], []).append(dv)
        if not dv['box']: w.append(('DEVICE_NO_BOX', dv['name'], 'ホスト名ラベルに対応する機器枠が見つからない'))
    for n, l in names.items():
        if len(l) > 1: w.append(('HOSTNAME_DUP', n, '同じホスト名の機器が%d台' % len(l)))
    for e in others:
        if e.get('problem') == 'dangling':
            end = e['a'] or e['b'] or {}
            msg = '線の片端が図形に接続されていない（もう一端: %s %s[%s]' % (end.get('owner'), end.get('text') or '', end.get('kind'))
            if e.get('free_end'):
                msg += '、未接続端の座標 (%d,%d)' % e['free_end']
            nr = e.get('near')
            if nr:
                msg += '、近くの要素: %s %s[%s] cell %s 距離%s' % (nr['owner'], nr['text'] or '', nr['kind'], nr['id'], nr['dist'])
            w.append(('EDGE_DANGLING', e['id'], msg + '）'))
        if e.get('problem') == 'to_label':
            lab, oth = (e['a'], e['b']) if e['a']['kind'] == 'seglabel' else (e['b'], e['a'])
            w.append(('EDGE_TO_LABEL', e['id'], '%s %s[%s] の線が横線ではなくラベル「%s」（cell %s）に接続されている' % (
                oth.get('owner'), oth.get('text'), oth.get('kind'), lab.get('text'), lab.get('id'))))
    for e in logical:
        seg, oth = (e['a'], e['b']) if e['a']['kind'] == 'segment' else (e['b'], e['a'])
        if seg['color'] and e['color'] != seg['color']:
            w.append(('LINE_COLOR_MISMATCH', e['id'], '%s %s[%s] → 横線（cell %s）: 線の色 %s、横線の色 %s' % (
                oth.get('owner'), oth.get('text') or '', oth.get('kind'), seg['id'], e['color'] or '(既定/黒)', seg['color'])))
    used = {}
    for e in phys:
        for x in (e['a'], e['b']):
            if x['kind'] != 'port': continue
            key = (x['owner'], x['text'])
            used.setdefault(key, []).append(e['id'])
    for k, l in used.items():
        if len(l) > 1 and k[1] and not PO_RE.match(k[1]):
            w.append(('PORT_MULTI_LINK', '%s %s' % k, '1つの物理ポートに%d本の物理リンク' % len(l)))
    for e in phys:
        for x, y in ((e['a'], e['b']), (e['b'], e['a'])):
            if x['text'].lower().startswith('gi') and e['width'] not in ('1', '') and float(e['width']) >= 3:
                w.append(('SPEED_MISMATCH', '%s %s' % (x['owner'], x['text']), '1Gポート名だが太線（10G系ケーブル凡例）で接続'))
    # CIDR 重複（同じ文字列のCIDRが異なるセグメント名に付いている）
    cidr = {}
    for el in elements:
        if el['kind'] == 'seglabel':
            for c in CIDR_RE.findall(el['text']):
                nm = re.sub(CIDR_RE, '', el['text']).strip(' ,/')
                cidr.setdefault(c, set()).add(re.sub(r'\s+', '', nm))
    for c, s in cidr.items():
        if len(s) > 1: w.append(('CIDR_CONFLICT', c, '同一CIDRが複数のセグメント名に付いている: %s' % ', '.join(sorted(s))))
    return [dict(code=a, where=b, detail=c) for a, b, c in w]


def to_md(name, r):
    L = ['# 抽出結果: %s' % name, '', '## 1. 機器（同名機器は #2, #3 を付けて区別）', '', '| ホスト名 | 機種 | 枠(x,y,w,h) |', '|---|---|---|']
    for dv in r['devices']:
        L.append('| %s | %s | %s |' % (dv['uid'], dv['model'], tuple(int(v) for v in dv['box']) if dv['box'] else '-'))
    L += ['', '## 2. 機器ごとの要素', '']
    by = {}
    for el in r['elements']:
        if el['kind'] in ('port', 'portchannel', 'segment', 'ipbadge', 'routing', 'vip', 'seglabel'):
            by.setdefault(el['owner'] or '(機器外)', []).append(el)
    for o in sorted(by):
        L.append('### %s' % o)
        for el in sorted(by[o], key=lambda e: (e['kind'], e['rect'][1], e['rect'][0])):
            L.append('- %s: `%s` color=%s @(%d,%d)%s' % (el['kind'], el['text'], el['color'] or '-', el['rect'][0], el['rect'][1],
                                                         (' props=%s' % el['props']) if el['props'] else ''))
        L.append('')
    def nd(x): return '%s %s' % (x.get('owner') or '-', x.get('text') or '[%s %s]' % (x.get('kind'), x.get('color')))
    def mark(st): return '●' if st[0] == 'oval' and st[1] == '1' else ('○' if st[0] == 'oval' else '-')
    L += ['## 3. 物理リンク', '', '| A | 端点A | B | 端点B | 線幅 | 色 | 線ID |', '|---|---|---|---|---|---|---|']
    for e in r['physical']:
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (nd(e['a']), mark(e['start']), nd(e['b']), mark(e['end']), e['width'], e['color'] or '-', e['id']))
    L += ['', '## 4. 論理接続（セグメント横線との接続）', '', '| 機器 | 要素 | セグメント色 | 線ID |', '|---|---|---|---|']
    for e in r['logical']:
        seg, oth = (e['a'], e['b']) if e['a']['kind'] == 'segment' else (e['b'], e['a'])
        L.append('| %s | %s `%s` | %s | %s |' % (seg['owner'], oth['kind'], oth['text'], seg['color'], e['id']))
    L += ['', '## 5. セグメント横線 → ラベル', '', '| 機器 | 横線色 | ラベル |', '|---|---|---|']
    for e in r['seglabels']:
        seg, lab = (e['a'], e['b']) if e['a']['kind'] == 'segment' else (e['b'], e['a'])
        L.append('| %s | %s | %s |' % (seg['owner'], seg['color'], lab['text']))
    L += ['', '## 6. ルーティング箱どうしの線（冗長ペア候補）', '']
    for e in r['pairs']:
        L.append('- %s ⇔ %s color=%s width=%s' % (nd(e['a']), nd(e['b']), e['color'], e['width']))
    L += ['', '## 7. 機械チェックの警告（要目視確認）', '', '| コード | 場所 | 内容 |', '|---|---|---|']
    for x in r['warns']:
        L.append('| %s | %s | %s |' % (x['code'], x['where'], x['detail']))
    L += ['', '## 8. 分類できなかった線（目視確認用）', '']
    for e in r['others']:
        L.append('- %s: %s -- %s color=%s dashed=%s label=%s' % (e['id'], nd(e['a']) if e['a'] else 'None', nd(e['b']) if e['b'] else 'None', e['color'], e['dashed'], e['label']))
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('--page'); ap.add_argument('--json'); ap.add_argument('--md')
    a = ap.parse_args()
    mx = load_mxfile(a.file)
    pages = mx.findall('diagram')
    if not a.page:
        for dg in pages:
            print(dg.get('name'))
        return
    dg = [x for x in pages if x.get('name') == a.page]
    if not dg: raise SystemExit('ページが見つかりません: %s' % a.page)
    r = analyze(Page(page_model(dg[0])))
    if a.json: json.dump(r, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    md = to_md(a.page, r)
    if a.md: open(a.md, 'w', encoding='utf-8').write(md)
    if not a.json and not a.md: sys.stdout.write(md)


if __name__ == '__main__':
    main()
