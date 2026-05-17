<!--
Sync Impact Report
- Version change: N/A → 1.0.0
- Modified principles: None (initial creation)
- Added sections:
  - Principle I: Code Quality
  - Principle II: Testing Standards (NON-NEGOTIABLE)
  - Principle III: User Experience Consistency
  - Principle IV: Performance Requirements
  - Section: Quality Gates
  - Section: Development Workflow
  - Section: Governance
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ reviewed (no changes needed)
  - .specify/templates/spec-template.md ✅ reviewed (no changes needed)
  - .specify/templates/tasks-template.md ✅ reviewed (no changes needed)
- Follow-up TODOs: None
-->

# Black Dragon Constitution

## Core Principles

### I. Code Quality

All production code MUST adhere to the following non-negotiable standards:

- Every module, function, and component MUST have a single, clear
  responsibility. Violations MUST be refactored before merge.
- Dead code, unused imports, and commented-out blocks MUST NOT exist
  in the main branch. CI MUST enforce linting with zero tolerance for
  warnings.
- All public APIs MUST use descriptive, unambiguous naming. Abbreviations
  are prohibited unless they are industry-standard (e.g., `HTTP`, `URL`).
- Code duplication MUST be eliminated through extraction when the same
  logic appears in three or more locations.
- All changes MUST pass static analysis, formatting checks, and type
  checking (where applicable) before merge.

**Rationale**: Consistent, clean code reduces cognitive load, accelerates
onboarding, and prevents defect accumulation over time.

### II. Testing Standards (NON-NEGOTIABLE)

All features and bug fixes MUST include corresponding tests:

- Unit tests MUST cover all public functions and methods. Minimum code
  coverage threshold is 80% per module; critical paths MUST have 100%.
- Integration tests MUST verify interactions between components,
  services, and external dependencies.
- Tests MUST be deterministic — no flaky tests allowed. Any test that
  fails intermittently MUST be quarantined and fixed within one sprint.
- Test names MUST describe the scenario and expected outcome using the
  pattern: `[unit]_[scenario]_[expectedResult]`.
- Regression tests MUST be added for every bug fix to prevent
  recurrence.
- Test execution MUST complete within acceptable time limits: unit tests
  < 30 seconds total, integration tests < 5 minutes total.

**Rationale**: Comprehensive testing is the primary defense against
regressions and the foundation of deployment confidence. No exceptions.

### III. User Experience Consistency

All user-facing interfaces MUST maintain visual and behavioral coherence:

- All UI components MUST follow the project's design system. Custom
  styling MUST NOT override design tokens without explicit approval.
- Interaction patterns MUST be consistent across all views and flows.
  Users MUST NOT encounter different behaviors for the same action in
  different contexts.
- Error states, loading states, and empty states MUST be handled
  explicitly in every user-facing component.
- Accessibility MUST meet WCAG 2.1 AA compliance at minimum. All
  interactive elements MUST be keyboard-navigable and screen-reader
  compatible.
- User feedback (success, error, progress) MUST be immediate and
  unambiguous. No silent failures in the UI.
- Responsive behavior MUST be validated across defined breakpoints
  before merge.

**Rationale**: Inconsistent UX erodes user trust and increases support
burden. A unified experience is a competitive requirement, not a
nice-to-have.

### IV. Performance Requirements

All features MUST meet defined performance baselines:

- Page/view initial load MUST complete within 2 seconds on a standard
  broadband connection (10 Mbps).
- Interactive responses (clicks, form submissions) MUST provide feedback
  within 100 milliseconds.
- API responses MUST complete within 500 milliseconds at the 95th
  percentile under normal load.
- Memory usage MUST NOT grow unboundedly. Long-running processes MUST
  demonstrate stable memory consumption over time.
- Bundle size impact MUST be measured for every change. Any increase
  exceeding 5% MUST include justification and optimization plan.
- Database queries MUST be reviewed for N+1 patterns and missing
  indexes. Any query exceeding 100ms MUST be optimized.

**Rationale**: Performance directly impacts user satisfaction, retention,
and operational costs. Degradation is treated as a defect.

## Quality Gates

All changes MUST pass the following gates before merge:

- **Lint Gate**: Zero warnings, zero errors from configured linters.
- **Type Gate**: Full type-check pass with no suppressions unless
  documented and justified.
- **Test Gate**: All unit and integration tests pass. Coverage thresholds
  met.
- **Performance Gate**: No regressions against established baselines.
  Bundle size delta reported.
- **UX Gate**: Design review completed for all user-facing changes.
  Accessibility audit passed.
- **Code Review Gate**: At least one approving review from a team member
  who did not author the change.

## Development Workflow

The development process MUST follow these conventions:

- All work MUST occur on feature branches. Direct commits to the main
  branch are prohibited.
- Commits MUST use conventional commit format:
  `type(scope): description`.
- Pull requests MUST reference the related issue or task. Orphan PRs
  MUST NOT be merged.
- Breaking changes MUST be documented in the PR description and flagged
  with a `BREAKING CHANGE` footer in the commit.
- Dependencies MUST be reviewed for security vulnerabilities before
  addition. No package with known critical CVEs may be introduced.
- Documentation MUST be updated in the same PR as the code change it
  describes.

## Governance

This constitution is the authoritative source of project standards.
It supersedes all informal practices, tribal knowledge, and ad-hoc
agreements.

- All pull requests and code reviews MUST verify compliance with these
  principles. Non-compliant code MUST NOT be merged.
- Amendments to this constitution require: (1) a written proposal
  documenting the change and rationale, (2) review and approval, and
  (3) a migration plan for existing code if the change is retroactive.
- The constitution MUST be reviewed quarterly to ensure principles
  remain relevant and actionable.
- Version numbering follows semantic versioning: MAJOR for principle
  removals or redefinitions, MINOR for additions or expansions, PATCH
  for clarifications and typo fixes.
- Complexity or exceptions MUST be justified in writing. "It was easier"
  is not a valid justification.

**Version**: 1.0.0 | **Ratified**: 2026-05-16 | **Last Amended**: 2026-05-16
