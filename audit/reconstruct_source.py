"""Phase A/B transcription from PDF Figure 1, before reading target Ecore.
None is unresolved; NOT_SHOWN is not evidence of an author default.
No draw.io, Ecore, existing notes, mapping or validator is read here.
"""
import json
from pathlib import Path

classes = {}
def cls(name, attrs='', abstract=False, supers=''):
    classes[name] = dict(name=name, abstract=abstract, eSuperTypes=supers.split())
    for spec in attrs.split(';'):
        if not spec: continue
        n,t,*d = spec.split(':')
        attributes.append(dict(owner=name, name=n, EType=None if t=='?' else t,
            lowerBound=None, upperBound=None,
            defaultValueLiteral=d[0] if d else 'NOT_SHOWN',
            evidence='P1 Figure 1, '+name+' attribute compartment'))
attributes=[]
cls('MAS','Name:EString;PlatformParamters:EString')
cls('Agent','Name:EString')
cls('Workspace','Name:EString;Path:EString;Host:EString')
cls('Artifact','artifactName:EString;className:EString;Parameter:EString;IDVar:EString;isInitial:EBoolean:false')
cls('Port','Name:EString')
cls('ObsProperty','ParamName:EString;Name:EString;initialValue:?')
cls('AbsOperation','className:EString;signalExpression:EString;awaitExpression:EString;await_timeExpression:EString;paramName:?', True)
for n in ['LinkedOperation','InternalOperation','GuardOperation','Operation']: cls(n,supers='AbsOperation')
cls('Organisation','id:EString')
for n in ['NormativeSpecification','StructuralSpecification','FunctionalSpecification']: cls(n)
cls('Norm','type:EString;timeConstraint:EString',supers='Organisation')
cls('Group','Name:EString;min:EInt;max:EInt',supers='Organisation')
cls('Role','Name:EString;min:EInt;max:EInt',supers='Organisation')
cls('Scheme','PlanOperator:EString',supers='Organisation')
cls('FormationConstraints','Name:EString;biDir:EBoolean:false;scope:EString:intra-group;type:EString;to:EString;from:EString')
cls('Link','type:EString;biDir:EBoolean:false;scope:EString:intra-group;from:EString;to:EString')
cls('Mission','max:EInt;min:EInt')
cls('OPlan','Sequence:EBoolean:false;Parallel:EBoolean:false')
cls('OGoal','Name:EString;isRootGoal:EBoolean:false')
cls('Belief','Name:EString;isInitial:EBoolean:false')
cls('Rule','Expression:EString')
cls('Goal','Name:EString')
cls('Plan','Name:EString;asBeliefAddition:EString;asQuery:EString;isAtomic:EString;atomicLabel:EString;argID:EString;isInitial:EBoolean:false')
cls('Body','Name:EString')
cls('Context','Expression:EString')
cls('BodyTerm',abstract=True)
cls('Action','Name:EString;Expression:EString',True,'BodyTerm')
cls('ExternalAction',supers='Action')
cls('InternalAction',supers='Action')
cls('TriggeringEvent','isSeparateIntention:EBoolean:false;isInitial:EBoolean:false;ttf:EInt;ds:EString;deletion:EBoolean:false;addAndDel:?',supers='Action')
cls('MentalNotes',supers='BodyTerm')
cls('Message','content:EString;isBroadcast:EBoolean:UNRESOLVED',supers='InternalAction')

# Every line is a separately traced arrow; C means a filled source diamond.
raw='''MAS agent Agent 1 * C
MAS workspace Workspace 0 * C
MAS organisation Organisation 0 * C
Agent belief Belief 0 * C
Agent rule Rule 0 * C
Agent hasGoal Goal 0 * C
Agent plan Plan 0 * C
Agent joinWorkspace Workspace 0 * N
Agent artifact Artifact 0 * N
Organisation normativespecification NormativeSpecification 1 1 C
Organisation structuralspecification StructuralSpecification 1 1 C
Organisation functionalspecification FunctionalSpecification 1 1 C
Organisation deploysAgent Agent 1 * N
NormativeSpecification norm Norm 0 * C
StructuralSpecification group Group 0 * C
StructuralSpecification role Role 0 * C
FunctionalSpecification scheme Scheme 0 * C
Norm Nrole Role 1 1 N
Norm NMission Mission 1 1 N
Group hasSubGroups Group 0 * N
Group RefRole Role 1 * N
Group formationconstraints FormationConstraints 0 * C
Group link Link 0 * C
Role Extendsrole Role 0 1 N
Role players Agent 0 * N
Scheme SchemeOPlan OPlan 0 * C
Scheme SchemeOgoal OGoal 1 * C
Scheme mission Mission 1 * C
Scheme Splan TriggeringEvent 0 * N
Mission ogoal OGoal 1 * N
Mission Mplan TriggeringEvent 0 * N
OPlan FirstOgoal OGoal 1 1 N
OPlan Splan TriggeringEvent 0 * N
OGoal NextOgoal OGoal 0 1 N
OGoal OGoalToOPlan OPlan 0 1 N
OGoal OGoalToGoal Goal 0 1 N
TriggeringEvent planoperator OPlan 0 1 N
TriggeringEvent triggersPlan Plan 1 1 N
Belief triggeredBy TriggeringEvent 1 1 N
Goal triggeredBy TriggeringEvent 1 * N
Workspace artifact Artifact 0 * C
Workspace hasSubworkspace Workspace 0 * N
Artifact port Port 0 * C
Artifact obsproperty ObsProperty 0 * C
Artifact operation AbsOperation 0 * C
Port linkArtifacts Artifact 0 * N
ObsProperty obsproperty Belief 0 * N
AbsOperation RefObsproperty ObsProperty 0 * N
Operation guardedBy GuardOperation 0 1 N
Operation callsInternal InternalOperation 0 1 N
ExternalAction operation AbsOperation 0 1 N
Plan RefArtifact Artifact 0 * N
Plan hasContext Context 1 1 C
Plan hasBody Body 1 1 C
Plan hasAction Action 0 * C
Body bodyterm BodyTerm 0 * C
Body firstAction Action 1 1 N
Action nextAction Action 0 1 N
Context contextRule Rule 0 * N
Context contextBelief Belief 0 * N
MentalNotes impliesG Goal 1 1 N
MentalNotes impliesB Belief 1 1 N
Message messageToagent Agent 0 * N'''
refs=[]
for line in raw.splitlines():
    o,n,t,lo,hi,c=line.split()
    refs.append(dict(owner=o,name=n,target=t,lowerBound=int(lo),upperBound=-1 if hi=='*' else int(hi),containment=c=='C',direction='source -> target',evidence='P1 Figure 1: labelled arrow '+o+'.'+n+'; '+('filled source diamond' if c=='C' else 'no source diamond')))
out=dict(provenance='Independent transcription of PDF page 3 / embedded R34.jp2; target Ecore not read during transcription. Attribute bounds are not printed. Unshown default is not evidence of absence.',classes=list(classes.values()),attributes=attributes,references=refs,
    unresolved=['ObsProperty.initialValue datatype','AbsOperation.paramName datatype','TriggeringEvent.addAndDel datatype','Message.isBroadcast explicit default','Attribute multiplicities not displayed','Completeness of attribute compartments with scrollbars cannot be proven'],
    listing_checks=['MAS.agent','MAS.workspace','MAS.organisation','Agent.plan','Workspace.artifact','Artifact.operation','Organisation.structuralspecification','Organisation.functionalspecification','Organisation.normativespecification','FunctionalSpecification.scheme','Scheme.SchemeOgoal','OGoal.OGoalToOPlan','OPlan.FirstOgoal','Plan.hasContext','Plan.hasBody','Plan.hasAction','Body.firstAction','NormativeSpecification.norm'],
    source_conflicts=['Listing 1 line 53 uses sch.id; Figure 1 Scheme inherits Organisation.id, so no need to add a local id.', 'Section III FormationConstaints is a prose typo; Figure 1 FormationConstraints prevails.', 'Section III says mission contains goals; Figure 1 Mission.ogoal has no diamond, so non-containment prevails.'])
Path('audit/source-inventory.json').write_bytes(json.dumps(out,indent=2,ensure_ascii=False).encode('utf-8'))
print('Independent source:',len(classes),'classes;',len(attributes),'visible attributes;',len(refs),'references;',sum(len(c['eSuperTypes']) for c in classes.values()),'generalizations')
