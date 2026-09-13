"""Negative controls for the metamodel-only V1 freeze contract."""
import unittest
from check_mapping import check, load, MAPPING

class ContractTests(unittest.TestCase):
    def assert_invalid(self, mutate):
        data=load(MAPPING)
        mutate(data)
        self.assertEqual(check(data)['status'],'FAIL')

    def test_wrong_inheritance_kind(self):
        self.assert_invalid(lambda d:d['inheritanceMappings'][0].update(sourceKind='EReference'))

    def test_malformed_projection(self):
        self.assert_invalid(lambda d:d['verificationProjections'][0].update(target={}))

    def test_unknown_projection(self):
        self.assert_invalid(lambda d:d['verificationProjections'][0].update(id='VP999'))

    def test_missing_projection_source(self):
        self.assert_invalid(lambda d:d['verificationProjections'][3].update(source='Missing.operation -> Absent'))

    def test_unqualified_source(self):
        self.assert_invalid(lambda d:d['referenceMappings'][34].update(source='operation'))

    def test_schema_rejects_unknown_property(self):
        self.assert_invalid(lambda d:d.update(unknownContractField=True))

    def test_use_reserved_attribute_names_rejected(self):
        for owner,name in [('FormationConstraints','from'),('Link','from'),('OPlan','Sequence')]:
            with self.subTest(owner=owner):
                def mutate(d):
                    next(a for a in d['attributeMappings'] if a['sourceOwner']==owner and a['sourceName']==name)['target']['name']=name
                self.assert_invalid(mutate)

    def test_projection_contract_mutations(self):
        cases=[
            ('anchor missing',lambda c:c.update(sourceElements=['dSML4JaCaMo::Missing'])),
            ('target missing',lambda c:c.update(baseClass='Missing')),
            ('concept invalid',lambda c:c.update(targetConcept='MSystemState')),
            ('binding orphan',lambda c:c.update(structuralBindings=['R999'])),
            ('dependency cycle',lambda c:c.update(dependsOn=['VP001'])),
            ('wrong direction',lambda c:c.update(direction='USE_TO_JACAMO')),
            ('assumptions absent',lambda c:c.update(assumptions=[])),
            ('baseline mutation',lambda c:c.update(baselineMutation=True)),
        ]
        for label,mutate in cases:
            with self.subTest(label=label):
                self.assert_invalid(lambda d:mutate(d['verificationProjections'][0]['metamodelContract']))

    def test_schema_version_and_shapes(self):
        cases=[
            ('version',lambda d:d.update(schemaVersion='1.0.0')),
            ('contract version',lambda d:d['contract'].update(version='1.0.0')),
            ('missing section',lambda d:d.pop('contract')),
            ('wrong primitive',lambda d:d['classMappings'][0].update(sourceAbstract='false')),
            ('wrong array',lambda d:d.update(referenceMappings={})),
            ('runtime scope',lambda d:d['contract'].update(layer='RUNTIME_BINDING')),
            ('extra field',lambda d:d['referenceMappings'][0].update(receiver='auction1')),
        ]
        for label,mutate in cases:
            with self.subTest(label=label): self.assert_invalid(mutate)

    def test_owner_identity_and_reference_mutations(self):
        cases=[
            ('wrong owner',lambda d:d['attributeMappings'][0].update(sourceOwner='Agent')),
            ('duplicate source',lambda d:d['attributeMappings'][1].update(source=d['attributeMappings'][0]['source'])),
            ('duplicate ID',lambda d:d['referenceMappings'][1].update(id=d['referenceMappings'][0]['id'])),
            ('source target reversed',lambda d:d['referenceMappings'][0].update(sourceOwner='Agent',sourceTarget='MAS')),
            ('missing target',lambda d:d['referenceMappings'][0]['target']['secondEnd'].update(**{'class':'Missing'})),
            ('reversed inheritance',lambda d:d['inheritanceMappings'][0]['target'].update(subclass='Organisation',superclass='Norm')),
            ('ordered loss',lambda d:d['referenceMappings'][0]['target']['secondEnd'].update(ordered=False)),
            ('uniqueness loss',lambda d:d['referenceMappings'][0].update(sourceUnique=False)),
        ]
        for label,mutate in cases:
            with self.subTest(label=label): self.assert_invalid(mutate)

    def test_each_reverse_collision_is_error(self):
        for pair in [('R035','R058'),('R031','R046'),('R023','R025'),('R047','R048')]:
            with self.subTest(pair=pair):
                d=load(MAPPING)
                for x in d['referenceMappings']:
                    if x['id'] in pair:
                        x['target']['firstEnd']['role']='source_'+x['sourceName']
                        x['navigation']['reverse']=x['sourceTarget']+'.source_'+x['sourceName']
                self.assertIn('ROLE_COLLISION',{e['code'] for e in check(d)['errors']})

    def test_inherited_navigation_collision(self):
        d=load(MAPPING)
        r=next(x for x in d['referenceMappings'] if x['id']=='R035')
        # Alias on AbsOperation also affects Operation and its local guardedBy.
        r['target']['firstEnd']['role']='guardedBy'
        r['navigation']['reverse']='AbsOperation.guardedBy'
        self.assertIn('INHERITED_NAME_COLLISION',{e['code'] for e in check(d)['errors']})

if __name__=='__main__': unittest.main()
