"""JSON Schema and semantic validation for metamodel mapping schema 1.1.0.

Not a project parser or runtime binder. USE compilation is a separate gate.
"""
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'Core/JaCaMo-Metamodel.ecore'
MAPPING = ROOT / 'mapping/jacamo-use-mapping-v1.json'
SCHEMA = ROOT / 'mapping/jacamo-use-mapping.schema.json'
XSI = '{http://www.w3.org/2001/XMLSchema-instance}type'
TYPES = {'EString': 'String', 'EInt': 'Integer', 'EBoolean': 'Boolean'}

def check(data, model=MODEL):
    schema=load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    schema_errors=list(Draft202012Validator(schema).iter_errors(data))
    if schema_errors:
        return dict(status='FAIL',schemaStatus='FAIL',errors=[dict(code='SCHEMA_INVALID',detail='/'.join(map(str,x.absolute_path))+': '+x.message) for x in schema_errors],warnings=[])
    root = ET.parse(model).getroot()
    cs = {c.get('name'): c for c in root.findall('eClassifiers')}
    attrs = {}; refs = {}; inheritance = set()
    for name, c in cs.items():
        inheritance.update((name, t.removeprefix('#//')) for t in c.get('eSuperTypes', '').split())
        for f in c.findall('eStructuralFeatures'):
            if f.get(XSI) not in ('ecore:EAttribute','ecore:EReference'):
                return dict(status='FAIL',errors=[dict(code='INVALID_ECORE',detail='Unsupported structural feature kind')])
            (attrs if f.get(XSI) == 'ecore:EAttribute' else refs)[name+'.'+f.get('name')] = f
    errors=[]; warnings=[]
    def require(ok, code, detail):
        if not ok: errors.append({'code':code,'detail':detail})
    def equal(actual, expected, code, detail):
        require(actual==expected,code,f'{detail}: expected {expected!r}, got {actual!r}')
    def multi(f):
        lo,hi=int(f.get('lowerBound','0')),int(f.get('upperBound','1'))
        text='*' if (lo,hi)==(0,-1) else str(lo) if lo==hi else f'{lo}..'+('*' if hi==-1 else str(hi))
        return {'lower':lo,'upper':hi,'text':text}
    equal(data['schemaVersion'],'1.1.0','VERSION_UNSUPPORTED','schemaVersion')
    equal(data['contract']['version'],data['schemaVersion'],'VERSION_UNSUPPORTED','contract.version')
    equal(root.tag,'{http://www.eclipse.org/emf/2002/Ecore}EPackage','INVALID_ECORE','root')
    require(len(cs)==len(root.findall('eClassifiers')),'INVALID_ECORE','Duplicate EClass')
    require(all(c.get(XSI)=='ecore:EClass' for c in cs.values()),'INVALID_ECORE','Wrong classifier kind')
    for c in cs.values():
        fs=c.findall('eStructuralFeatures')
        require(len({f.get('name') for f in fs})==len(fs),'INVALID_ECORE','Duplicate EStructuralFeature')
    src=data['sourceMetamodel']
    equal((ROOT/src['artifact']).resolve(),model.resolve(),'SOURCE_PATH_STALE','source artifact')
    equal(src['sha256'],hashlib.sha256(model.read_bytes()).hexdigest(),'RECONCILE_REQUIRED','source hash')
    for mk,ek in [('packageName','name'),('nsURI','nsURI'),('nsPrefix','nsPrefix')]:
        equal(src[mk],root.get(ek),'NAMESPACE_MISMATCH',mk)
    equal(src['expectedStatistics'],dict(EClasses=len(cs),EAttributes=len(attrs),EReferences=len(refs),EGeneralizations=len(inheritance)),'COVERAGE_MISMATCH','expectedStatistics')
    equal(data['policies']['datatypeMappings'],[{'source':k,'target':v} for k,v in TYPES.items()],'TYPE_MISMATCH','datatype policy')
    reverse_counts=Counter((f.get('eType').removeprefix('#//'),key.split('.')[1]) for key,f in refs.items())
    groups=['classMappings','attributeMappings','referenceMappings','inheritanceMappings']
    ids=[x['id'] for k in groups+['verificationProjections'] for x in data[k]]
    require(len(ids)==len(set(ids)),'DUPLICATE_BINDING','duplicate ID')
    for group in groups:
        keys=[x['source'] for x in data[group]]
        require(len(keys)==len(set(keys)),'DUPLICATE_BINDING',group)
        equal(data['statistics'][group],len(data[group]),'COVERAGE_MISMATCH',group+' statistics')
    equal({x['source'] for x in data['classMappings']},{'dSML4JaCaMo::'+n for n in cs},'COVERAGE_MISMATCH','classes')
    for x in data['classMappings']:
        name=x['source'].removeprefix('dSML4JaCaMo::'); c=cs.get(name)
        if c is None: require(False,'MISSING_SOURCE',x['source']); continue
        abstract=c.get('abstract','false')=='true'
        equal(x['sourceAbstract'],abstract,'CLASS_MISMATCH',x['id'])
        equal(x['target'],dict(kind='USE_CLASS',internalConcept='MClass',name=name,abstract=abstract),'TARGET_MISMATCH',x['id'])
        equal(x['sourceKind'],'EClass','BINDING_KIND',x['id'])
        equal(x['policy'],'FAITHFUL_STRUCTURAL','BINDING_KIND',x['id']+' policy')
    for group,features in [('attributeMappings',attrs),('referenceMappings',refs)]:
        equal({x['source'] for x in data[group]},{'dSML4JaCaMo::'+k.replace('.','#') for k in features},'COVERAGE_MISMATCH',group)
        for x in data[group]:
            key=x['sourceOwner']+'.'+x['sourceName']; f=features.get(key)
            if f is None: require(False,'MISSING_SOURCE',key); continue
            equal(x['source'],'dSML4JaCaMo::'+key.replace('.','#'),'SOURCE_KEY_MISMATCH',x['id'])
            equal(x['sourceMultiplicity'],multi(f),'MULTIPLICITY_MISMATCH',key)
            t=f.get('eType').split('#//')[-1]
            if group=='attributeMappings':
                equal(x['sourceKind'],'EAttribute','BINDING_KIND',key)
                equal(x['sourceType'],t,'TYPE_MISMATCH',key)
                equal(x.get('sourceExplicitDefaultLiteral'),f.get('defaultValueLiteral'),'DEFAULT_MISMATCH',key)
                target_name=data['policies']['identifierPolicy']['targetAttributeEscapes'].get(key,x['sourceName'])
                equal(x['target'],dict(kind='USE_ATTRIBUTE',internalConcept='MAttribute',owner=x['sourceOwner'],name=target_name,type=TYPES[t]),'TARGET_MISMATCH',key)
                equal(x['valuePolicy'],'COPY_RESOLVED_SEMANTIC_VALUE','VALUE_POLICY_MISMATCH',key)
                equal(x['absencePolicy'],'LEAVE_UNDEFINED_IF_SOURCE_VALUE_IS_UNSET','VALUE_POLICY_MISMATCH',key)
            else:
                o,n=x['sourceOwner'],x['sourceName']; contain=f.get('containment','false')=='true'
                reverse_role='source_'+(o+'_' if reverse_counts[(t,n)]>1 else '')+n
                equal(x['sourceKind'],'EReference','BINDING_KIND',key)
                equal(x['sourceTarget'],t,'TARGET_MISMATCH',key)
                equal(x['sourceContainment'],contain,'CONTAINMENT_MISMATCH',key)
                ordered=f.get('ordered','true')=='true'
                unique=f.get('unique','true')=='true'
                equal(x['sourceOrdered'],ordered,'ORDERING_MISMATCH',key)
                equal(x['sourceUnique'],unique,'UNIQUENESS_MISMATCH',key)
                require(unique,'UNSUPPORTED_COLLECTION','USE association requires unique links: '+key)
                target=dict(kind='USE_COMPOSITION' if contain else 'USE_ASSOCIATION',internalConcept='MAssociation',name=f'{o}_{n}_{t}',firstEnd=dict(class_=o,multiplicity='0..1' if contain else '*',role=reverse_role),secondEnd={'class':t,'multiplicity':multi(f)['text'],'role':n,'ordered':ordered and multi(f)['upper']!=1})
                target['firstEnd']['class']=target['firstEnd'].pop('class_')
                if contain: target['diamondEnd']='firstEnd'
                equal(x['target'],target,'TARGET_MISMATCH',key)
                equal(x['navigation'],dict(forward=key,sourceAuthoritative=True,reverse=t+'.'+reverse_role,reverseAuthoritative=False),'NAVIGATION_MISMATCH',key)
                equal(x['runtimeLinkCommand'],f'!insert (<{o}_object>, <{t}_object>) into {o}_{n}_{t}','LINK_TEMPLATE_MISMATCH',key)
                equal(x['policy'],'CONTAINMENT_TO_COMPOSITION' if contain else 'REFERENCE_TO_ASSOCIATION','BINDING_KIND',key)
    equal({x['source'] for x in data['inheritanceMappings']},{f'dSML4JaCaMo::{a}->super::{b}' for a,b in inheritance},'INHERITANCE_MISMATCH','coverage')
    for x in data['inheritanceMappings']:
        equal(x['sourceKind'],'eSuperType','BINDING_KIND',x['id'])
        sub,sup=x['source'].removeprefix('dSML4JaCaMo::').split('->super::')
        equal(x['target'],dict(kind='USE_GENERALIZATION',subclass=sub,superclass=sup),'INHERITANCE_MISMATCH',x['id'])
        equal(x['policy'],'PRESERVE_SOURCE_INHERITANCE','INHERITANCE_MISMATCH',x['id'])
    unresolved={}
    for name,c in cs.items():
        for a in c.findall('eAnnotations'):
            ds={d.get('key'):d.get('value') for d in a.findall('details')}
            if a.get('source')=='urn:reconstruction:unresolved' and 'visibleAttribute' in ds:
                unresolved[f'dSML4JaCaMo::{name}#{ds["visibleAttribute"]}']=ds
    equal({x['source'] for x in data['unresolvedSourceFeatures']},set(unresolved),'UNRESOLVED_POLICY_MISMATCH','unresolved coverage')
    for x in data['unresolvedSourceFeatures']:
        equal(x['source'],f'dSML4JaCaMo::{x["owner"]}#{x["visibleAttribute"]}','UNRESOLVED_POLICY_MISMATCH','owner-qualified name')
        equal(x['mappingStatus'],'NOT_MAPPED_NOT_AN_EATTRIBUTE','UNRESOLVED_POLICY_MISMATCH',x['source'])
        if x['source'] in unresolved:
            for k in ['visibleAttribute','evidence','decision','status']:
                equal(x[k],unresolved[x['source']][k],'UNRESOLVED_POLICY_MISMATCH',x['source']+' '+k)
    equal(data['statistics']['verificationProjectionRules'],len(data['verificationProjections']),'COVERAGE_MISMATCH','projections')
    equal(data['statistics']['unresolvedNamedButUndeclaredAttributes'],len(unresolved),'COVERAGE_MISMATCH','unresolved statistics')
    targets=[x['target']['name'] for x in data['classMappings']+data['referenceMappings']]
    require(len(targets)==len(set(targets)),'DUPLICATE_TARGET','class/association names')
    for flag in data['reviewFlags']:
        require(flag['source'] in {x['source'] for x in data['inheritanceMappings']},'STALE_REVIEW_FLAG',flag['source'])
    # Resolve all projected anchors independently; a projection is not an Ecore
    # declaration. Templates name USE metaconcepts, not nonexistent concrete types.
    bindings={x['id']:x for group in groups for x in data[group]}
    projections={x['id']:x for x in data['verificationProjections']}
    equal(set(projections),{f'VP{i:03}' for i in range(1,8)},'PROJECTION_COVERAGE','projection IDs')
    known_sources={'dSML4JaCaMo::'+n for n in cs}|{'dSML4JaCaMo::'+k.replace('.','#') for k in attrs|refs}
    for p in projections.values():
        c=p['metamodelContract']
        for source in c['sourceElements']:
            require(source in known_sources,'PROJECTION_SOURCE_MISSING',p['id']+': '+source)
        for binding in c['structuralBindings']:
            require(binding in bindings,'PROJECTION_TARGET_MISSING',p['id']+': '+binding)
            if binding in bindings:
                require(bindings[binding]['source'] in c['sourceElements'],'PROJECTION_ANCHOR_MISMATCH',p['id']+': '+binding)
        if c['baseClass'] is not None:
            require(c['baseClass'] in {x['target']['name'] for x in data['classMappings']},'PROJECTION_TARGET_MISSING',p['id'])
        for dep in c['dependsOn']:
            require(dep in projections and dep!=p['id'],'PROJECTION_DEPENDENCY',p['id'])
    nav=defaultdict(list)
    for x in data['referenceMappings']:
        nav[x['navigation']['forward']].append(x['id'])
        nav[x['navigation']['reverse']].append(x['id'])
    for key,bindings in sorted(nav.items()):
        require(len(bindings)==1,'ROLE_COLLISION',key+' '+str(bindings))
    def ancestors(name,path=()):
        require(name not in path,'INVALID_INHERITANCE','cycle: '+str(path+(name,)))
        if name in path: return set()
        parents={b for a,b in inheritance if a==name}
        require(parents<=set(cs),'INVALID_INHERITANCE','unresolved parent: '+name)
        return parents | set().union(*(ancestors(p,path+(name,)) for p in parents)) if parents else set()
    for name in cs:
        owners={name}|ancestors(name)
        namespace=defaultdict(list)
        for key,binding_ids in nav.items():
            owner,feature=key.split('.')
            if owner in owners: namespace[feature].extend(binding_ids)
        for attribute in data['attributeMappings']:
            owner,feature=attribute['target']['owner'],attribute['target']['name']
            key=owner+'.'+feature
            if owner in owners: namespace[feature].append(key)
        for feature,uses in namespace.items():
            require(len(uses)==1,'INHERITED_NAME_COLLISION',name+'.'+feature+': '+str(uses))
    return dict(status='FAIL' if errors else 'PASS',schemaStatus='PASS',scope='Metamodel mapping contract; USE compilation is a separate gate, runtime is out of scope',errors=errors,warnings=warnings,counts=dict(classes=len(cs),attributes=len(attrs),references=len(refs),inheritance=len(inheritance),projections=len(data['verificationProjections'])),sourceSHA256=hashlib.sha256(model.read_bytes()).hexdigest())

def load(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapping',type=Path,default=MAPPING)
    parser.add_argument('--model',type=Path,default=MODEL)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try: result=check(load(args.mapping),args.model)
    except (KeyError,TypeError,ValueError,OSError,ET.ParseError) as exc:
        result=dict(status='FAIL',errors=[dict(code='INPUT_INVALID',detail=str(exc))])
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output: args.output.write_bytes((text+'\n').encode('utf-8'))
    print(text)
    raise SystemExit(result['status']!='PASS')
