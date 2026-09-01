---
name: code-review
description: Evaluate a PR against this project's standards — layered architecture, OWASP security, test coverage, SDD patterns, and stack conventions. Produces structured findings categorized as blocking, warning, or suggestion. Use /code-review for the current branch's PR, or /code-review <PR#> for a specific PR.
---

# Code Review

## Purpose

Evaluate a Pull Request against the specific standards of this repository.

This is NOT a generic review — it checks against the architecture rules in `docs/doc_architecture.md`, the stack conventions of each module declared there, OWASP controls already applied in this codebase, and SDD process compliance.

The output is a structured report with findings categorized as blocking, warning, or suggestion, ending with a clear verdict.

> **Adaptar al proyecto:** este skill viene con placeholders. Antes del primer uso,
> reemplaza `<módulo-backend>` y `<módulo-frontend>` por los nombres reales de tus
> módulos, y ajusta las rutas de las Dimensiones 1, 3 y 5 a la estructura declarada
> en `docs/doc_architecture.md`. Las reglas que no apliquen a tu stack, bórralas —
> no las dejes como ruido.

---

## Arguments

- No argument: review the open PR for the current branch
- `<PR#>`: review that specific PR number

---

## Process

### Step 1 — Resolve PR number

If a PR number was provided as argument, use it directly.

If no argument was provided:
- Run `git branch --show-current` to get the current branch name
- Run `gh pr list --state open --head <branch> --json number,title` to find the open PR
- If no PR is found, inform the user: "No hay un PR abierto para la rama actual. Usa `/code-review <PR#>` para revisar uno específico."
- If `gh` is not authenticated, stop and say: "Ejecuta `gh auth login` para autenticarte con GitHub."

### Step 2 — Gather PR metadata

Run:
```
gh pr view <number> --json title,body,author,baseRefName,headRefName,state,additions,deletions,changedFiles,labels
```

Extract: title, author login, base branch, head branch, files changed count, additions, deletions.

### Step 3 — Get the diff

Run:
```
gh pr diff <number>
```

Read the full diff. This is the primary input for the evaluation.

### Step 4 — Read modified files in current state

From the list of changed files in the PR metadata, read each file from the local repository (current state on disk, not just the diff). This provides context about placement, imports, and surrounding code.

Skip files that are binary, generated, or in `node_modules/`, `.git/`, `migrations/versions/`.

### Step 5 — Evaluate the 5 dimensions

Evaluate each dimension independently. For each finding, record:
- Category: 🔴 bloqueante / 🟡 advertencia / 🔵 sugerencia
- File and line number if identifiable
- Concise description of the issue

If a dimension does not apply to the PR (e.g., no backend files in a docs-only PR), mark it as "No aplica" — do not invent findings.

**Directed exploration is required, not optional.** A review based only on the diff misses findings that depend on repo context — e.g. a documented architecture exception, an existing test pattern that already covers the gap you're about to flag, or a claim about the PR description that was never actually checked. Before finalizing a finding:
- Allowed: read reference documents in full (`docs/doc_architecture.md`, `docs/doc_review_process.md`) even if the diff only touches a small section of what they cover; run a scoped grep/find in the repo to check whether a pattern or precedent cited in a suggestion actually exists; use `gh pr view --json body` (already fetched in Step 2) to verify claims about the PR description instead of inferring them from the diff.
- Not allowed: auditing or deep-reading modules/files unrelated to the diff. Directed exploration answers a specific question raised by a specific finding — it is not a license to review the whole codebase.

---

#### Dimensión 1: Arquitectura en capas

Reference: `docs/doc_architecture.md` — read it in full, not just "Reglas de placement". Before flagging a placement violation, check whether the document declares an explicit exception that covers the case. Citing the exception where relevant is part of the finding, not a separate step.

Check:
- New HTTP routes → must live in the transport layer declared in `doc_architecture.md`. If found elsewhere → 🔴
- New business logic → must live in the application/domain layer, never inside a request handler → 🔴
- New database models → must be in the persistence layer with a corresponding migration. Model without migration → 🟡
- Database queries → must go through the repository layer using the ORM. Raw SQL outside it, with no documented exception → 🔴
- New external integrations → must live in their own module. If the logic is mixed into domain or transport code → 🟡
- Circular imports between layers → 🔴

#### Dimensión 2: Seguridad OWASP

Check:
- Hardcoded credentials, tokens, secrets, or API keys in source code → 🔴
- Raw SQL strings (f-strings with user input, `.execute("SELECT...")`) outside the repository layer → 🔴
- Mass assignment: new `PATCH`/`POST` endpoints that assign the request `body` dict directly to model fields without an allowlist → 🔴
- HMAC or token comparison using `==` instead of a constant-time comparison → 🔴
- New cookies set without `secure=True` → 🟡
- New authentication or OTP endpoints without rate limiting → 🟡
- User-supplied input rendered in templates without escaping → 🔴
- New admin or internal endpoints without an auth header check → 🔴

#### Dimensión 3: Cobertura de tests

Before suggesting a missing test, check whether an equivalent pattern already exists in the repo (a scoped `find`/`grep` over the module's test directory). If it exists, the suggestion should point to that existing pattern by name/path instead of proposing to invent one from scratch.

Check:
- If the PR modifies business logic in `<módulo-backend>/` → look for corresponding new or updated tests. If none → 🟡
- If the PR modifies logic in `<módulo-frontend>/` → look for the module's test files. If none → 🟡
- If the PR only modifies templates, CSS, config, or documentation → mark as "No aplica"
- New tests that mock the database when integration tests are possible → 🔵 (check the repo's established integration-test convention before suggesting this from scratch)

#### Dimensión 4: Patrones SDD

Check claims against the real PR body fetched in Step 2 (`gh pr view --json body`) — never infer whether something is mentioned from the diff alone.

Check:
- Branch name follows convention: `feat/`, `fix/`, `docs/`, `chore/` → if not → 🟡
- PR description explains what changed and why (not just "adds X") → if missing → 🟡
- If the PR introduces new behavior or a new feature, the description should reference a closed requirement (enrich-user-story output or equivalent) → verify this against the actual body text, if absent → 🟡

#### Dimensión 5: Convenciones de stack

**Python:**
- No raw SQL outside the repository layer → if found → 🔴 (also caught in Dim 2)
- No business logic in request handlers — a handler should only receive, validate, and dispatch → if violated → 🔴
- No circular imports between layers → 🔴
- No hardcoded absolute paths → 🟡
- Logger used (`logger = logging.getLogger(__name__)`) instead of `print()` in production code → 🔵

**TypeScript:**
- No direct `fetch()` calls inside React components — API calls must go through service layer files → 🟡
- No `any` type without an explanatory comment → 🔵
- New API routes must validate input at the boundary (zod, manual check, or equivalent) → if missing → 🟡
- Auth checks present in protected API routes → if missing → 🔴

---

### Step 5.5 — Self-verification pass

Before writing the final report, re-check every draft finding against the real repo state:
- For findings grounded in a reference document (Dimensión 1, SDD dimension) — re-read the specific section/exception cited and confirm it still supports the finding.
- For findings grounded in a grep/find (Dimensión 3 precedent check) — re-run it and confirm the result.
- For findings grounded in PR metadata (Dimensión 4) — confirm against the `gh pr view --json body` output from Step 2, not a paraphrase of it.

If a draft finding does not hold up under this check, drop it silently — it does not appear in the final report, and its removal is not called out as a "fixed" or "corrected" finding (self-verification is internal to this pass, not a visible output).

If a reference document needed for grounding is missing or unreadable, do not silently skip the check — say so explicitly in the relevant dimension of the final report (e.g. "No se pudo verificar contra `docs/doc_architecture.md` — archivo no accesible").

---

### Step 6 — Produce the report

Print the following structure to the console. Do not save to disk.

```
# Code Review — PR #<N>: <título>

**Autor:** <author> · **Base:** <base> ← <head>
**Archivos:** <N> · +<additions> / -<deletions>

---

## 1. Arquitectura en capas
<hallazgos o "✅ Sin hallazgos">

## 2. Seguridad OWASP
<hallazgos o "✅ Sin hallazgos">

## 3. Cobertura de tests
<hallazgos o "✅ Sin hallazgos" o "— No aplica">

## 4. Patrones SDD
<hallazgos o "✅ Sin hallazgos">

## 5. Convenciones de stack
<hallazgos o "✅ Sin hallazgos">

---

## Veredicto

✅ Aprobable
⚠️ Aprobable con cambios menores — <N> advertencia(s), <N> sugerencia(s)
❌ Requiere cambios antes del merge — <N> hallazgo(s) bloqueante(s)
```

Each finding is formatted as:
```
🔴/🟡/🔵 `path/to/file.py` (línea N si aplica) — descripción concisa del hallazgo
```

---

## Rules

- Directed exploration is required for grounding (reference docs in full, scoped precedent checks, real PR metadata) — but stays scoped to the question a specific finding raises, never a full audit of unrelated code
- Every draft finding must survive the Step 5.5 self-verification pass before appearing in the report
- If a dimension does not apply, say so explicitly — never invent findings to fill sections
- The verdict is informational — it does not block the merge automatically
- Respond in the same language the user used to invoke the skill
- Do not repeat findings across dimensions — assign each finding to its most relevant dimension only
