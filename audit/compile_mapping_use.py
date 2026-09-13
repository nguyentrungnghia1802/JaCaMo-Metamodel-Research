"""Static USE compiler gate. No runtime model, receiver or object bindings.

Pass the classpath of pinned use-core 7.5.0 and its Maven dependencies.
The hypothetical projection signature is a type-system fixture, not a case study.
"""
import argparse
import copy
import subprocess
import tempfile
from pathlib import Path
from check_mapping import check, load, MAPPING, ROOT

def render(data, projection_fixture=False):
    lines=['model JaCaMoMetamodelMappingV1']
    for entry in data['classMappings']:
        name=entry['target']['name']
        parents=[i['target']['superclass'] for i in data['inheritanceMappings'] if i['target']['subclass']==name]
        lines.append(('abstract ' if entry['target']['abstract'] else '')+'class '+name+(' < '+', '.join(parents) if parents else ''))
        attributes=[a['target'] for a in data['attributeMappings'] if a['target']['owner']==name]
        if attributes:
            lines.append('attributes')
            lines.extend('  '+a['name']+' : '+a['type'] for a in attributes)
        lines.append('end')
    for entry in data['referenceMappings']:
        t=entry['target']
        lines.append(('composition' if t['kind']=='USE_COMPOSITION' else 'association')+' '+t['name']+' between')
        for key in ['firstEnd','secondEnd']:
            end=t[key]
            lines.append(f'  {end["class"]}[{end["multiplicity"]}] role {end["role"]}'+(' ordered' if end.get('ordered',False) else ''))
        lines.append('end')
    if projection_fixture:
        lines+=['-- Hypothetical VP001/002/003 declaration only; no concrete model binding.',
                'class ProjectionContractType < Artifact','attributes','  projectionContractValue : Integer',
                'operations','  projectionContractOperation(argument : String) : Boolean','end']
    return '\n'.join(lines)+'\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--use-classpath',required=True)
    parser.add_argument('--java',default='java')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    d=load(MAPPING); r=check(d)
    if r['errors']: raise SystemExit(str(r['errors']))
    counts=[len(d[k]) for k in ['classMappings','attributeMappings','referenceMappings','inheritanceMappings']]
    counts.append(sum(x['target']['secondEnd']['ordered'] for x in d['referenceMappings']))
    counts.append(0)
    source=ROOT/'audit/ValidateMappingUse.java'; log=[]
    def run(path,mode,expected):
        p=subprocess.run([args.java,'--class-path',args.use_classpath,str(source),str(path),mode,*map(str,expected)],capture_output=True,text=True,timeout=60)
        if p.returncode: raise RuntimeError(p.stdout+p.stderr)
        log.append(p.stdout.strip())
    with tempfile.TemporaryDirectory(prefix='jacamo-metamodel-') as tmp:
        path=Path(tmp)/'baseline.use'
        path.write_text(render(d),encoding='utf-8')
        run(path,'accept',counts)
        path.write_text(render(d,True),encoding='utf-8')
        fixture_counts=counts.copy(); fixture_counts[0]+=1; fixture_counts[1]+=1; fixture_counts[3]+=1; fixture_counts[5]+=1
        run(path,'accept',fixture_counts)
        # Reintroduce each old collision independently, proving the compiler
        # checks the actual failure instead of merely accepting our validator.
        for pair in [('R035','R058'),('R031','R046'),('R023','R025'),('R047','R048')]:
            changed=copy.deepcopy(d)
            for x in changed['referenceMappings']:
                if x['id'] in pair: x['target']['firstEnd']['role']='source_'+x['sourceName']
            path.write_text(render(changed),encoding='utf-8')
            run(path,'reject',[])
            log[-1]+=' '+','.join(pair)
        for key in d['policies']['identifierPolicy']['targetAttributeEscapes']:
            changed=copy.deepcopy(d)
            for a in changed['attributeMappings']:
                if a['sourceOwner']+'.'+a['sourceName']==key: a['target']['name']=a['sourceName']
            path.write_text(render(changed),encoding='utf-8')
            run(path,'reject-identifier',[])
            log[-1]+=' '+key
    text='USE 7.5.0 @ '+d['targetUSE']['validatedRevision']+'\n'+'\n'.join(log)+'\nScope: metamodel declarations only; no runtime state or concrete bindings.\n'
    if args.output: args.output.write_bytes(text.encode('utf-8'))
    print(text)

if __name__=='__main__': main()
