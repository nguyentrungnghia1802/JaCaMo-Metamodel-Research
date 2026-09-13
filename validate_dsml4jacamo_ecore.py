"""Validate the conservative DSML4JaCaMo 2024 reconstruction.
Literal expectations were transcribed from Figure 1 / Listing 1 before editing
the model. PASS does not resolve metadata clipped from the publication.
Standard library only; --emf-classpath additionally uses real Eclipse EMF.
"""
import argparse
import copy
import os
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ECORE = 'http://www.eclipse.org/emf/2002/Ecore'
XSI = '{http://www.w3.org/2001/XMLSchema-instance}type'
XMI = '{http://www.omg.org/XMI}version'
MODEL = Path(__file__).resolve().parent / 'Core' / 'JaCaMo-Metamodel.ecore'

# Declared attributes only. Scheme.id is inherited; three clipped types omitted.
# name:type[=explicit default]; unprinted attribute bounds use Ecore 0..1.
ATTRIBUTES = {
    'MAS': 'Name:EString PlatformParamters:EString',
    'Organisation': 'id:EString',
    'NormativeSpecification': '',
    'StructuralSpecification': '',
    'FunctionalSpecification': '',
    'Norm': 'type:EString timeConstraint:EString',
    'Group': 'Name:EString min:EInt max:EInt',
    'Role': 'Name:EString min:EInt max:EInt',
    'FormationConstraints': 'Name:EString biDir:EBoolean=false scope:EString=intra-group type:EString to:EString from:EString',
    'Link': 'type:EString biDir:EBoolean=false scope:EString=intra-group from:EString to:EString',
    'Scheme': 'PlanOperator:EString',
    'OPlan': 'Sequence:EBoolean=false Parallel:EBoolean=false',
    'OGoal': 'Name:EString isRootGoal:EBoolean=false',
    'Mission': 'min:EInt max:EInt',
    'Workspace': 'Name:EString Path:EString Host:EString',
    'Artifact': 'artifactName:EString className:EString Parameter:EString IDVar:EString isInitial:EBoolean=false',
    'Port': 'Name:EString',
    'ObsProperty': 'ParamName:EString Name:EString',
    'AbsOperation': 'className:EString signalExpression:EString awaitExpression:EString await_timeExpression:EString',
    'LinkedOperation': '',
    'InternalOperation': '',
    'GuardOperation': '',
    'Operation': '',
    'Agent': 'Name:EString',
    'Belief': 'Name:EString isInitial:EBoolean=false',
    'Rule': 'Expression:EString',
    'Goal': 'Name:EString',
    'Context': 'Expression:EString',
    'Plan': 'Name:EString asBeliefAddition:EString asQuery:EString isAtomic:EString atomicLabel:EString argID:EString isInitial:EBoolean=false',
    'Body': 'Name:EString',
    'BodyTerm': '',
    'Action': 'Name:EString Expression:EString',
    'ExternalAction': '',
    'InternalAction': '',
    'MentalNotes': '',
    'Message': 'content:EString isBroadcast:EBoolean',
    'TriggeringEvent': 'isSeparateIntention:EBoolean=false isInitial:EBoolean=false ttf:EInt ds:EString deletion:EBoolean=false',
}
ABSTRACT = {'AbsOperation', 'BodyTerm', 'Action'}
SUPERS = {
    'Norm': 'Organisation', 'Group': 'Organisation',
    'Role': 'Organisation', 'Scheme': 'Organisation',
    'LinkedOperation': 'AbsOperation', 'InternalOperation': 'AbsOperation',
    'GuardOperation': 'AbsOperation', 'Operation': 'AbsOperation',
    'Action': 'BodyTerm', 'ExternalAction': 'Action',
    'InternalAction': 'Action', 'MentalNotes': 'BodyTerm',
    'Message': 'InternalAction', 'TriggeringEvent': 'Action',
}
# Owner.feature Target lower upper containment(1=yes). No inferred opposites.
REFERENCES = '''
MAS.agent Agent 1 -1 1
MAS.workspace Workspace 0 -1 1
MAS.organisation Organisation 0 -1 1
Organisation.normativespecification NormativeSpecification 1 1 1
Organisation.structuralspecification StructuralSpecification 1 1 1
Organisation.functionalspecification FunctionalSpecification 1 1 1
Organisation.deploysAgent Agent 1 -1 0
NormativeSpecification.norm Norm 0 -1 1
StructuralSpecification.group Group 0 -1 1
StructuralSpecification.role Role 0 -1 1
FunctionalSpecification.scheme Scheme 0 -1 1
Norm.Nrole Role 1 1 0
Norm.NMission Mission 1 1 0
Group.hasSubGroups Group 0 -1 0
Group.RefRole Role 1 -1 0
Group.formationconstraints FormationConstraints 0 -1 1
Group.link Link 0 -1 1
Role.Extendsrole Role 0 1 0
Role.players Agent 0 -1 0
Scheme.mission Mission 1 -1 1
Scheme.SchemeOgoal OGoal 1 -1 1
Scheme.SchemeOPlan OPlan 0 -1 1
Scheme.Splan TriggeringEvent 0 -1 0
OPlan.FirstOgoal OGoal 1 1 0
OPlan.Splan TriggeringEvent 0 -1 0
OGoal.NextOgoal OGoal 0 1 0
OGoal.OGoalToOPlan OPlan 0 1 0
OGoal.OGoalToGoal Goal 0 1 0
Mission.ogoal OGoal 1 -1 0
Mission.Mplan TriggeringEvent 0 -1 0
Workspace.artifact Artifact 0 -1 1
Workspace.hasSubworkspace Workspace 0 -1 0
Artifact.port Port 0 -1 1
Artifact.obsproperty ObsProperty 0 -1 1
Artifact.operation AbsOperation 0 -1 1
Port.linkArtifacts Artifact 0 -1 0
AbsOperation.RefObsproperty ObsProperty 0 -1 0
Operation.guardedBy GuardOperation 0 1 0
Operation.callsInternal InternalOperation 0 1 0
Agent.belief Belief 0 -1 1
Agent.rule Rule 0 -1 1
Agent.plan Plan 0 -1 1
Agent.hasGoal Goal 0 -1 1
Agent.joinWorkspace Workspace 0 -1 0
Agent.artifact Artifact 0 -1 0
ObsProperty.obsproperty Belief 0 -1 0
Belief.triggeredBy TriggeringEvent 1 1 0
Goal.triggeredBy TriggeringEvent 1 -1 0
Context.contextRule Rule 0 -1 0
Context.contextBelief Belief 0 -1 0
Plan.hasBody Body 1 1 1
Plan.hasContext Context 1 1 1
Plan.hasAction Action 0 -1 1
Plan.RefArtifact Artifact 0 -1 0
Body.bodyterm BodyTerm 0 -1 1
Body.firstAction Action 1 1 0
Action.nextAction Action 0 1 0
ExternalAction.operation AbsOperation 0 1 0
MentalNotes.impliesG Goal 1 1 0
MentalNotes.impliesB Belief 1 1 0
Message.messageToagent Agent 0 -1 0
TriggeringEvent.planoperator OPlan 0 1 0
TriggeringEvent.triggersPlan Plan 1 1 0
'''


def expected_features():
    expected = {}
    for owner, attributes in ATTRIBUTES.items():
        for token in attributes.split():
            name, typed = token.split(':')
            dtype, sep, default = typed.partition('=')
            expected[owner + '.' + name] = (
                'ecore:EAttribute', 'ecore:EDataType ' + ECORE + '#//' + dtype,
                0, 1, False, default if sep else None)
    for line in REFERENCES.strip().splitlines():
        key, target, lower, upper, contain = line.split()
        expected[key] = ('ecore:EReference', '#//' + target,
                         int(lower), int(upper), contain == '1', None)
    return expected


def validate(root):
    errors = []
    if root.tag != '{' + ECORE + '}EPackage':
        errors.append('EPackage: wrong XML namespace/root')
    for key, value in {'name': 'dSML4JaCaMo',
                       'nsURI': 'urn:dsml4jacamo:2024:reconstructed',
                       'nsPrefix': 'dSML4JaCaMo', XMI: '2.0'}.items():
        if root.get(key) != value:
            errors.append(f'EPackage: unexpected {key}={root.get(key)!r}')
    for child in root:
        if child.tag not in {'eAnnotations', 'eClassifiers'}:
            errors.append(f'EPackage: unsupported child {child.tag}')
    classes, features, parents = {}, {}, {}
    for cls in root.findall('eClassifiers'):
        name = cls.get('name', '')
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
            errors.append(f'invalid classifier name: {name!r}')
        if name in classes:
            errors.append(f'duplicate classifier: {name}')
        classes[name] = cls
        if cls.get(XSI) != 'ecore:EClass':
            errors.append(f'{name}: unexpected classifier kind (no paper enum/datatype)')
        if cls.get('abstract', 'false') != str(name in ABSTRACT).lower():
            errors.append(f'{name}: abstract flag differs from Figure 1')
        if cls.get('interface', 'false') != 'false':
            errors.append(f'{name}: unsupported interface flag')
        expected_parent = '#//' + SUPERS[name] if name in SUPERS else ''
        if cls.get('eSuperTypes', '') != expected_parent:
            errors.append(f'{name}: eSuperTypes expected {expected_parent!r}')
        parents[name] = []
        for ref in cls.get('eSuperTypes', '').split():
            if not re.fullmatch(r'#//[A-Za-z_][A-Za-z0-9_]*', ref):
                errors.append(f'{name}: invalid supertype URI {ref!r}')
            else:
                parents[name].append(ref[3:])
        for child in cls:
            if child.tag not in {'eAnnotations', 'eStructuralFeatures'}:
                errors.append(f'{name}: unsupported child {child.tag}')
        for feature in cls.findall('eStructuralFeatures'):
            fname = feature.get('name', '')
            key = name + '.' + fname
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', fname):
                errors.append(f'{key}: invalid feature name')
            if key in features:
                errors.append(f'{key}: duplicate feature')
            features[key] = feature
    if set(classes) != set(ATTRIBUTES):
        errors.append(f'class inventory: missing={sorted(set(ATTRIBUTES)-set(classes))}, '
                      f'extra={sorted(set(classes)-set(ATTRIBUTES))}')

    def ancestry(name, path):
        if name in path:
            errors.append('inheritance cycle: ' + ' -> '.join(path + [name]))
            return set()
        result = set()
        for parent in parents.get(name, []):
            if parent not in classes:
                errors.append(f'{name}: dangling supertype {parent}')
            else:
                result.add(parent)
                result.update(ancestry(parent, path + [name]))
        return result

    ancestors = {name: ancestry(name, []) for name in classes}
    expected = expected_features()
    for key in sorted(set(expected) - set(features)):
        errors.append(f'{key}: missing paper feature')
    for key in sorted(set(features) - set(expected)):
        errors.append(f'{key}: unsupported declared feature')
    for key, feature in features.items():
        owner, fname = key.split('.', 1)
        for parent in ancestors[owner]:
            if parent + '.' + fname in features:
                errors.append(f'{key}: duplicate inherited feature from {parent}')
        kind, etype = feature.get(XSI), feature.get('eType', '')
        try:
            lower = int(feature.get('lowerBound', '0'))
            upper = int(feature.get('upperBound', '1'))
            if lower < 0 or upper < -1 or (upper != -1 and lower > upper):
                errors.append(f'{key}: invalid bounds {lower}..{upper}')
        except ValueError:
            errors.append(f'{key}: non-integer bounds')
            continue
        for flag, default in [('ordered', 'true'), ('unique', 'true'),
                              ('changeable', 'true'), ('volatile', 'false'),
                              ('transient', 'false'), ('unsettable', 'false'),
                              ('derived', 'false')]:
            if feature.get(flag, default) != default:
                errors.append(f'{key}: unsupported {flag} setting')
        contain = feature.get('containment', 'false')
        if contain not in {'true', 'false'}:
            errors.append(f'{key}: malformed containment')
        if kind == 'ecore:EAttribute':
            valid_types = {'ecore:EDataType ' + ECORE + '#//' + t
                           for t in ['EString', 'EBoolean', 'EInt']}
            if etype not in valid_types:
                errors.append(f'{key}: invalid datatype URI/EType {etype!r}')
            if contain != 'false' or feature.get('eOpposite'):
                errors.append(f'{key}: EAttribute has reference properties')
            if feature.get('iD', 'false') != 'false':
                errors.append(f'{key}: unsupported EAttribute ID flag')
            default = feature.get('defaultValueLiteral')
            if etype.endswith('#//EBoolean') and default not in {None, 'true', 'false'}:
                errors.append(f'{key}: invalid boolean default')
            if etype.endswith('#//EInt') and default is not None:
                try:
                    if not -(2**31) <= int(default) < 2**31:
                        raise ValueError()
                except ValueError:
                    errors.append(f'{key}: invalid EInt default')
        elif kind == 'ecore:EReference':
            if not re.fullmatch(r'#//[A-Za-z_][A-Za-z0-9_]*', etype):
                errors.append(f'{key}: invalid reference URI {etype!r}')
            elif etype[3:] not in classes:
                errors.append(f'{key}: dangling reference target {etype!r}')
            if feature.get('resolveProxies', 'true') != 'true':
                errors.append(f'{key}: unsupported resolveProxies setting')
            opposite = feature.get('eOpposite')
            if opposite:
                errors.append(f'{key}: opposite not established by Figure 1')
                match = re.fullmatch(r'#//([^/]+)/([^/]+)', opposite)
                other_key = '.'.join(match.groups()) if match else ''
                other = features.get(other_key)
                if other is None or other.get(XSI) != 'ecore:EReference':
                    errors.append(f'{key}: dangling/invalid eOpposite')
                else:
                    if other.get('eOpposite') != '#//' + key.replace('.', '/'):
                        errors.append(f'{key}: non-reciprocal eOpposite')
                    if other_key.split('.')[0] not in {etype[3:]} | ancestors.get(etype[3:], set()):
                        errors.append(f'{key}: incompatible eOpposite owner')
                    if other.get('eType', '')[3:] not in {owner} | ancestors[owner]:
                        errors.append(f'{key}: incompatible eOpposite type')
                    if contain == 'true' and (other.get('containment') == 'true'
                                             or other.get('upperBound', '1') != '1'):
                        errors.append(f'{key}: invalid containment opposite')
        else:
            errors.append(f'{key}: invalid feature kind {kind!r}')
        actual = (kind, etype, lower, upper, contain == 'true',
                  feature.get('defaultValueLiteral'))
        if key in expected and actual != expected[key]:
            errors.append(f'{key}: expected {expected[key]!r}, got {actual!r}')
    # Classifier-level containment cycles are legal Ecore; inheritance in the
    # published Organisation hierarchy must not be removed to avoid such cycles.
    return errors


def self_test(root):
    """Real mutated XML trees must be rejected for the named defect."""
    def feature(tree, owner, name):
        return tree.find(f"eClassifiers[@name='{owner}']/eStructuralFeatures[@name='{name}']")

    cases = [
        ('nextAction cardinality', lambda r: feature(r, 'Action', 'nextAction').set('upperBound', '-1'), 'Action.nextAction: expected'),
        ('nextAction containment', lambda r: feature(r, 'Action', 'nextAction').set('containment', 'true'), 'Action.nextAction: expected'),
        ('nextAction must be self-reference', lambda r: feature(r, 'Action', 'nextAction').set('eType', '#//Goal'), 'Action.nextAction: expected'),
        ('observable-property arrow target', lambda r: feature(r, 'ObsProperty', 'obsproperty').set('eType', '#//Agent'), 'ObsProperty.obsproperty: expected'),
        ('dangling target', lambda r: feature(r, 'Action', 'nextAction').set('eType', '#//Missing'), 'dangling reference target'),
        ('wrong reference URI', lambda r: feature(r, 'Action', 'nextAction').set('eType', 'wrong.ecore#//Action'), 'invalid reference URI'),
        ('missing datatype', lambda r: feature(r, 'Agent', 'Name').attrib.pop('eType'), 'invalid datatype URI'),
        ('wrong datatype URI', lambda r: feature(r, 'Agent', 'Name').set('eType', 'ecore:EDataType urn:wrong#//EString'), 'invalid datatype URI'),
        ('bad bounds', lambda r: feature(r, 'Agent', 'Name').set('lowerBound', '-2'), 'invalid bounds'),
        ('non-integer bounds', lambda r: feature(r, 'Agent', 'Name').set('upperBound', 'many'), 'non-integer bounds'),
        ('inheritance cycle', lambda r: r.find("eClassifiers[@name='Action']").set('eSuperTypes', '#//TriggeringEvent'), 'inheritance cycle'),
        ('missing superclass', lambda r: r.find("eClassifiers[@name='Action']").set('eSuperTypes', '#//Missing'), 'dangling supertype'),
        ('duplicate declaration', lambda r: r.find("eClassifiers[@name='Agent']").append(copy.deepcopy(feature(r, 'Agent', 'Name'))), 'duplicate feature'),
        ('inherited id redeclared', lambda r: r.find("eClassifiers[@name='Scheme']").append(copy.deepcopy(feature(r, 'Organisation', 'id'))), 'duplicate inherited feature'),
        ('bad opposite', lambda r: feature(r, 'Action', 'nextAction').set('eOpposite', '#//Action/missing'), 'dangling/invalid eOpposite'),
        ('wrong namespace', lambda r: r.set('nsURI', 'urn:wrong'), 'EPackage: unexpected nsURI'),
        ('invalid root', lambda r: setattr(r, 'tag', '{urn:wrong}EPackage'), 'wrong XML namespace/root'),
        ('abstract regression', lambda r: r.find("eClassifiers[@name='Action']").set('abstract', 'false'), 'abstract flag'),
        ('boolean default', lambda r: feature(r, 'Belief', 'isInitial').set('defaultValueLiteral', 'maybe'), 'invalid boolean default'),
        ('lost feature', lambda r: r.find("eClassifiers[@name='ExternalAction']").remove(feature(r, 'ExternalAction', 'operation')), 'missing paper feature'),
    ]
    assert not validate(root), 'self-test requires a valid control model'
    for name, mutate, diagnostic in cases:
        changed = copy.deepcopy(root)
        mutate(changed)
        result = validate(changed)
        if not any(diagnostic in error for error in result):
            raise RuntimeError(f'self-test failed to detect {name}: {result}')
    print(f'Validator mutation tests: PASS ({len(cases)} rejected; valid control accepted)')


JAVA_CHECK = r'''
import org.eclipse.emf.common.util.*;
import org.eclipse.emf.ecore.*;
import org.eclipse.emf.ecore.resource.*;
import org.eclipse.emf.ecore.resource.impl.*;
import org.eclipse.emf.ecore.xmi.impl.*;
import org.eclipse.emf.ecore.util.*;
class CheckEcore {
    static void report(Diagnostic d) {
        if (d.getSeverity() != Diagnostic.OK) System.out.println(d.getMessage());
        for (Diagnostic child : d.getChildren()) report(child);
    }
    public static void main(String[] args) throws Exception {
        ResourceSet rs = new ResourceSetImpl();
        rs.getPackageRegistry().put(EcorePackage.eNS_URI, EcorePackage.eINSTANCE);
        rs.getResourceFactoryRegistry().getExtensionToFactoryMap()
            .put("ecore", new EcoreResourceFactoryImpl());
        Resource resource = rs.getResource(URI.createFileURI(args[0]), true);
        EcoreUtil.resolveAll(rs);
        if (!resource.getErrors().isEmpty() || !resource.getWarnings().isEmpty())
            throw new IllegalStateException(resource.getErrors()+" / "+resource.getWarnings());
        if (resource.getContents().size()!=1 || !(resource.getContents().get(0) instanceof EPackage))
            throw new IllegalStateException("Expected one EPackage");
        EPackage pkg = (EPackage) resource.getContents().get(0);
        Diagnostic d = Diagnostician.INSTANCE.validate(pkg);
        report(d);
        if (d.getSeverity()!=Diagnostic.OK) throw new IllegalStateException("EMF diagnostics failed");
        if (!EcoreUtil.UnresolvedProxyCrossReferencer.find(rs).isEmpty())
            throw new IllegalStateException("Unresolved proxies");
        EClass scheme = (EClass)pkg.getEClassifier("Scheme");
        EStructuralFeature id = scheme.getEStructuralFeature("id");
        if (id == null || !id.getEContainingClass().getName().equals("Organisation"))
            throw new IllegalStateException("Listing 1 sch.id must resolve through Organisation");
        EClass action = (EClass)pkg.getEClassifier("Action");
        EReference next = (EReference)action.getEStructuralFeature("nextAction");
        if (next.getEType()!=action || next.isContainment() || next.getLowerBound()!=0 || next.getUpperBound()!=1)
            throw new IllegalStateException("Invalid nextAction chain");
        System.out.println("EMF load + Diagnostician + proxy resolution: PASS");
        System.out.println("EMF Scheme.id inheritance + Action.nextAction: PASS");
    }
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', nargs='?', type=Path, default=MODEL)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--emf-classpath', help='OS-separated EMF common, ecore and ecore.xmi JAR paths')
    parser.add_argument('--java', default='java', help='Java 11+ executable for optional EMF validation')
    args = parser.parse_args()
    try:
        root = ET.parse(args.model).getroot()
    except (ET.ParseError, OSError) as exc:
        print(f'VALIDATION: FAIL\nXML/input: {exc}')
        return 1
    errors = validate(root)
    print('Parsed XML: OK')
    if errors:
        print('VALIDATION: FAIL')
        for error in errors:
            print(' - ' + error)
        return 1
    if args.self_test:
        self_test(root)
    if args.emf_classpath:
        for jar in args.emf_classpath.split(os.pathsep):
            if not Path(jar).is_file():
                print(f'VALIDATION: FAIL\nMissing EMF JAR: {jar}')
                return 1
        with tempfile.TemporaryDirectory(prefix='dsml4jacamo-emf-') as tmp:
            source = Path(tmp) / 'CheckEcore.java'
            source.write_text(JAVA_CHECK, encoding='utf-8')
            result = subprocess.run([args.java, '--class-path', args.emf_classpath,
                                     str(source), str(args.model.resolve())],
                                    capture_output=True, text=True, timeout=60)
            print(result.stdout, end='')
            if result.returncode:
                print(result.stderr)
                print('VALIDATION: FAIL (EMF)')
                return 1
    else:
        print('EMF Diagnostician: not requested (use --emf-classpath)')
    features = root.findall('eClassifiers/eStructuralFeatures')
    attrs = sum(f.get(XSI) == 'ecore:EAttribute' for f in features)
    refs = [f for f in features if f.get(XSI) == 'ecore:EReference']
    print(f'EClasses: {len(root.findall("eClassifiers"))}; abstract: {len(ABSTRACT)}; inheritance edges: {len(SUPERS)}')
    print(f'EAttributes: {attrs}; EReferences: {len(refs)} (containment: {sum(f.get("containment") == "true" for f in refs)})')
    print('Structural checks + paper reconstruction inventory: PASS')
    print('Unresolved paper metadata: see notes; PASS is not author-artifact equivalence.')
    print('VALIDATION: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
