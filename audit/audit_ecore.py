"""Read-only canonical extraction and structural checks. Not an EMF Diagnostician substitute."""
import json, hashlib
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

XSI='{http://www.w3.org/2001/XMLSchema-instance}type'
root=ET.parse('Core/JaCaMo-Metamodel.ecore').getroot()
def annotations(e):
    return [{'source':a.get('source'), 'details':{d.get('key'):d.get('value') for d in a.findall('details')}} for a in e.findall('eAnnotations')]
def typ(v): return v.split('#//')[-1] if v else None
cs=[]; ats=[]; rs=[]; errors=[]
nodes=root.findall('eClassifiers')
names=[e.get('name') for e in nodes]
cn=set(names)
class_names={e.get('name') for e in nodes if e.get(XSI)=='ecore:EClass'}
datatype_names={e.get('name') for e in nodes if e.get(XSI) in ('ecore:EDataType','ecore:EEnum')}
for n,c in Counter(names).items():
    if c>1: errors.append('Duplicate classifier '+str(n))
for e in nodes:
    n=e.get('name')
    if e.get(XSI)!='ecore:EClass': errors.append('Non-EClass classifier: '+str(n)); continue
    su=[typ(v) for v in e.get('eSuperTypes','').split()]
    cs.append(dict(name=n,abstract=e.get('abstract','false')=='true',eSuperTypes=su,annotations=annotations(e)))
    for s in su:
        if s not in class_names: errors.append('Unresolved/invalid superclass '+n+' -> '+s)
    fs=e.findall('eStructuralFeatures')
    for fn,c in Counter(f.get('name') for f in fs).items():
        if c>1: errors.append('Duplicate structural feature '+n+'.'+str(fn))
    for f in fs:
        d=dict(owner=n,name=f.get('name'),lowerBound=int(f.get('lowerBound','0')),upperBound=int(f.get('upperBound','1')),annotations=annotations(f),rawEType=f.get('eType'))
        if d['lowerBound']<0 or d['upperBound'] < -1 or (d['upperBound']!=-1 and d['lowerBound']>d['upperBound']): errors.append('Invalid bounds '+n+'.'+str(f.get('name')))
        t=typ(f.get('eType'))
        if f.get(XSI)=='ecore:EAttribute':
            d.update(EType=t,defaultValueLiteral=f.get('defaultValueLiteral'))
            ats.append(d)
            if not (t in datatype_names or (t in ('EString','EBoolean','EInt') and f.get('eType','').startswith('ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//'))): errors.append('Invalid attribute EType '+n+'.'+str(f.get('name')))
            v=d['defaultValueLiteral']
            if t=='EBoolean' and v is not None and v not in ('true','false'): errors.append('Invalid boolean literal '+n+'.'+d['name'])
            if t=='EInt' and v is not None:
                try: int(v)
                except ValueError: errors.append('Invalid integer literal '+n+'.'+d['name'])
        elif f.get(XSI)=='ecore:EReference':
            d.update(target=t,containment=f.get('containment','false')=='true',eOpposite=f.get('eOpposite'))
            rs.append(d)
            if t not in class_names or not f.get('eType','').startswith('#//'): errors.append('Unresolved/invalid reference target '+n+'.'+str(f.get('name')))
        else: errors.append('Unsupported feature kind '+str(f.get(XSI)))

cm={c['name']:c for c in cs}
def cycles(graph):
    # Canonical directed simple cycles; bounded by this small metamodel.
    found=set()
    def visit(start,n,path):
        for nxt in graph.get(n,set()):
            if nxt==start: found.add(tuple(path+[start]))
            elif nxt not in path and nxt>=start: visit(start,nxt,path+[nxt])
    for n in sorted(graph): visit(n,n,[n])
    return [list(c) for c in sorted(found)]
ig={n:set(c['eSuperTypes']) for n,c in cm.items()}
ic=cycles(ig)
if ic: errors.append('Inheritance cycles')
def supers(n,seen=None):
    seen=set() if seen is None else seen
    for s in ig.get(n,[]):
        if s not in seen: seen.add(s); supers(s,seen)
    return seen
anc={n:supers(n) for n in cm}
feature_map={(f['owner'],f['name']):f for f in ats+rs}
for n in cm:
    effective=[(k,f) for k,f in feature_map.items() if k[0]==n or k[0] in anc[n]]
    for fn,c in Counter(k[1] for k,f in effective).items():
        if c>1: errors.append('Inherited feature collision '+n+'.'+fn)
for r in rs:
    if r['eOpposite']:
        op=tuple(r['eOpposite'].removeprefix('#//').split('/'))
        if op not in feature_map: errors.append('Unresolved eOpposite '+r['owner']+'.'+r['name'])
cg={n:set() for n in cm}
for r in rs:
    if r['containment']: cg[r['owner']].add(r['target'])
# Effective graph accounts for inherited containments and allowed target subtypes.
eg={n:set() for n in cm}
for n in cm:
    for r in rs:
        if r['containment'] and (r['owner']==n or r['owner'] in anc[n]):
            eg[n].update(t for t in cm if t==r['target'] or r['target'] in anc[t])

inv=dict(package=dict(root.attrib),annotations=annotations(root),classes=cs,attributes=ats,references=rs)
Path('audit/ecore-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False),encoding='utf-8')
src=json.loads(Path('audit/source-inventory.json').read_text(encoding='utf-8'))
diff=[]
for cat,keys in [('classes',('name',)),('attributes',('owner','name')),('references',('owner','name'))]:
    sm={tuple(s[k] for k in keys):s for s in src[cat]}; em={tuple(s[k] for k in keys):s for s in inv[cat]}
    for key in sm.keys()|em.keys():
        s=sm.get(key); e=em.get(key)
        if s is None: diff.append([cat,'.'.join(key),'EXTRA_IN_ECORE',None,e]); continue
        if e is None:
            status='UNRESOLVED_FROM_SOURCE' if cat=='attributes' and s['EType'] is None else 'MISSING_IN_ECORE'
            diff.append([cat,'.'.join(key),status,s,None]); continue
        check=['abstract','eSuperTypes'] if cat=='classes' else ['EType'] if cat=='attributes' else ['target','lowerBound','upperBound','containment']
        mismatch={k:[s[k],e[k]] for k in check if s[k] is not None and s[k]!=e[k]}
        if cat=='attributes' and s['defaultValueLiteral'] not in ('NOT_SHOWN','UNRESOLVED') and s['defaultValueLiteral']!=e['defaultValueLiteral']: mismatch['defaultValueLiteral']=[s['defaultValueLiteral'],e['defaultValueLiteral']]
        if mismatch: diff.append([cat,'.'.join(key),'MISMATCH',mismatch,e])
report=dict(errors=errors,xml_well_formed=True,xmi_root_and_version=(root.tag=='{http://www.eclipse.org/emf/2002/Ecore}EPackage' and root.get('{http://www.omg.org/XMI}version')=='2.0'),inheritance_cycles=ic,direct_containment_type_cycles=cycles(cg),effective_containment_type_cycles=cycles(eg),nonexact=sorted(diff,key=lambda x:(x[0],x[1])),counts={k:len(inv[k]) for k in ('classes','attributes','references')},hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['Core/Bài báo 1.pdf','Core/Metamodel-2024.jpg','Core/JaCaMo-Metamodel.drawio','Core/JaCaMo-Metamodel.ecore','audit/source-inventory.json']})
Path('audit/validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
