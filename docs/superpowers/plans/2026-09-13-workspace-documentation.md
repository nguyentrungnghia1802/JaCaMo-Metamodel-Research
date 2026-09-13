# JaCaMo Workspace Documentation Implementation Plan

**Goal:** Document and validate the existing Core/mapping/audit workspace, then commit and push valid changes on main.
**Architecture:** Preserve Core and mapping semantics. Repair relocated file references, retain reproducible audit evidence, and explicitly distinguish source consistency from runtime readiness.
**Tech Stack:** Python standard library, Eclipse EMF/Java, Markdown, Git.
**Spec:** User request of 2026-09-13: inspect Core first, all mapping second, document root/Core/mapping, ignore only generated scratch, validate before commit/push.

## Global constraints

- Keep current branch; no reset/rebase/force push.
- Paper/Figure 1 wins; no guessed datatype/default or semantics changes.
- Preserve original Core bytes and mapping bindings; only reconcile the stale source artifact path using matching SHA-256.
- Execute inline as already authorized; no separate implementation task or approval pause.

## Tasks

- [x] Inspect all Core XML and mapping sections; compare Core hash and canonical inventory with existing forensic evidence.
- [x] Repair existing audit/default validator paths for Core layout; preserve reconstruction transcription and checks.
- [x] Add a read-only mapping consistency checker with mutation controls; report runtime/schema limitations separately from structural pass/fail.
- [x] Create root/Core/mapping/audit documentation and targeted .gitignore; preserve source/evidence and list disposable generated files without deleting them.
- [x] Run baseline validator self-tests and EMF, independent audit, mapping checks, README links and ignore policy; inspect status/diff.
- Final delivery: commit valid files with docs(jacamo) message, push main without force, verify remote SHA and clean worktree. Completion evidence is recorded in Git and the final task report, not pre-recorded here.
