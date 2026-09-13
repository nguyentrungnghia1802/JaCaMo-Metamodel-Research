# Metamodel Mapping V1 Freeze Plan

**Scope:** Canonical Core Ecore → USE-side metamodel declarations. No concrete
model, receiver/object binding, runtime state, adapter or OCL execution.

**Design:** Preserve owner-qualified source keys and source semantics. Repair
the four reverse-role collision pairs with `source_<Owner>_<feature>` for those
eight ends only, retaining unambiguous existing role names. Add schema 1.1.0 and
typed projection contracts, with deferred project-derived operands explicitly
outside the baseline. Validate USE declarations with a pinned USE compiler.

Schema changes are additive except invalid ambiguous reverse target names being
repaired; source identities and forward roles do not change. The repaired aliases
were not valid unique USE navigations. No executable consumer exists in this repo.
V1 is a metamodel contract, not a promise of lossless program/runtime semantics.

## Steps

- Reproduce validator gaps with negative controls before implementation.
- Recompute inventories from Core; preserve Core SHA and four unresolved facts.
- Add complete JSON Schema, typed projection anchors/targets and explicit scope.
- Validate every entry, inherited navigation namespaces, collection ordering,
  cardinality and projection dependencies; reject malformed/orphan/stale entries.
- Compile baseline USE declarations and hypothetical projection type signatures
  only; no state or concrete model bindings.
- Extend tests, document projection loss/assumptions and freeze criteria.
- Run all relevant checks; commit/push current branch only when gates pass.
