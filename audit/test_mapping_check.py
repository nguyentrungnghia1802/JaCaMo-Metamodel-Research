"""Mutation controls for the read-only mapping checker; never edit baseline."""
import copy
import unittest
from check_mapping import check, load, MAPPING

class MappingChecks(unittest.TestCase):
    def test_control(self):
        r=check(load(MAPPING))
        self.assertEqual(r['errors'],[])
        collisions={x['detail'] for x in r['warnings'] if x['code']=='REVERSE_ROLE_COLLISION'}
        self.assertIn('TriggeringEvent.source_Splan',collisions)

    def test_mutated_bindings_are_rejected(self):
        cases=[
            ('hash',lambda d:d['sourceMetamodel'].update(sha256='0'*64),'RECONCILE_REQUIRED'),
            ('path',lambda d:d['sourceMetamodel'].update(artifact='missing.ecore'),'SOURCE_PATH_STALE'),
            ('class',lambda d:d['classMappings'][0]['target'].update(name='Missing'),'TARGET_MISMATCH'),
            ('spelling',lambda d:d['attributeMappings'][1].update(sourceName='PlatformParameters'),'MISSING_SOURCE'),
            ('type',lambda d:d['attributeMappings'][0]['target'].update(type='Boolean'),'TARGET_MISMATCH'),
            ('default',lambda d:d['attributeMappings'][61].update(sourceExplicitDefaultLiteral='false'),'DEFAULT_MISMATCH'),
            ('bounds',lambda d:d['referenceMappings'][0]['sourceMultiplicity'].update(lower=0),'MULTIPLICITY_MISMATCH'),
            ('containment',lambda d:d['referenceMappings'][0].update(sourceContainment=False),'CONTAINMENT_MISMATCH'),
            ('direction',lambda d:d['referenceMappings'][36]['target']['secondEnd'].update(**{'class':'Agent'}),'TARGET_MISMATCH'),
            ('inheritance',lambda d:d['inheritanceMappings'][0]['target'].update(superclass='Agent'),'INHERITANCE_MISMATCH'),
            ('missing',lambda d:d['referenceMappings'].pop(),'COVERAGE_MISMATCH'),
            ('duplicate',lambda d:d['classMappings'].append(copy.deepcopy(d['classMappings'][0])),'DUPLICATE_BINDING'),
            ('unresolved',lambda d:d['unresolvedSourceFeatures'][0].update(mappingStatus='MAPPED'),'UNRESOLVED_POLICY_MISMATCH'),
        ]
        for name,mutate,code in cases:
            with self.subTest(name=name):
                d=load(MAPPING); mutate(d)
                self.assertIn(code,{x['code'] for x in check(d)['errors']})

if __name__=='__main__': unittest.main()
