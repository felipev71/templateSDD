# Guía de Revisión de PRs

Proceso para revisar un PR antes de mergearlo a `main`. Tiempo estimado: 20-30 min por PR promedio.

Este flujo asume un solo desarrollador: el autor revisa su propio PR antes de mergear. No se requiere la aprobación de un tercero.

---

## Fase 1 — Conformidad SDD (5 min, en GitHub)

Antes de ver código, verificar que el PR cumple el flujo SDD. Si algún criterio falla, corregirlo antes de continuar.

| Criterio | Cómo verificar |
|---|---|
| Descripción generada con `/write-pr-report` | Tiene secciones: Summary, What Changed, Validation, Reviewer Notes, Risks, Rollback |
| Cambio viene de requisito formal | PR description o commits mencionan `/enrich-user-story` o un plan aprobado |
| Tests declarados (si aplica) | "Validation > Automated" tiene resultados concretos, no está vacía ni dice "N/A" sin justificación |
| Convención de rama correcta | `feat/`, `fix/`, `docs/` o `chore/` según el tipo de cambio |

---

## Fase 2 — Análisis con Claude Code (10 min, en local)

### Cómo abrir Claude Code

**Desde la terminal** (recomendado):
```bash
cd <ruta-del-repositorio>
claude               # abre Claude Code en el directorio actual
```

**Desde VSCode:** panel lateral de Claude Code o `Cmd+Shift+P → "Claude Code"`.

### Ejecutar el review

Con Claude Code abierto en el directorio del proyecto, escribir en el chat:

```
/code-review <número-PR>
```

Ejemplo para el PR #2:
```
/code-review 2
```

El skill descarga el diff directamente desde GitHub — **no es necesario hacer `git checkout` en este paso**.

> **Atajo:** también funciona escribir en lenguaje natural, por ejemplo `"vamos a revisar el PR #2"`. Claude iniciará el proceso automáticamente.

### Qué produce el skill

- Resumen de cambios agrupados por capa
- Bugs y riesgos clasificados: 🔴 bloqueantes, 🟡 menores
- Preguntas abiertas que deben resolverse antes del merge

El análisis no se limita al diff: cruza cada hallazgo candidato contra la documentación del repo (por ejemplo, las excepciones de arquitectura declaradas en `doc_architecture.md`) y contra precedentes existentes (patrones de test ya usados en el repo) antes de reportarlo, y corre una pasada de auto-verificación final que descarta cualquier hallazgo que no se sostenga — pensado para que una sola corrida sea suficiente, sin necesidad de repetirla.

### Registrar los hallazgos en GitHub

Si el review deja observaciones que conviene dejar por escrito antes de mergear:

```bash
gh pr comment <número> --repo <owner>/<repo> \
  --body "## Code Review

### 🔴 Bug...

### 🟡 Riesgo..."
```

Si no hay observaciones bloqueantes, pasar a la Fase 3.

### Git checkout (solo si necesitas correr código localmente en Fase 3)

```bash
git fetch origin
git checkout -b review/<nombre-rama> origin/<nombre-rama>
```

---

## Fase 3 — Verificación técnica (5-15 min)

Usar [`doc_verification_guide.md`](doc_verification_guide.md) según los archivos que cambiaron. Esa guía es la fuente de los comandos concretos por tipo de cambio; la tabla siguiente es solo el criterio de qué nivel de verificación exigir.

| Si cambió... | Qué exigir |
|---|---|
| Lógica pura (parseo, cálculo, reglas de negocio) | Suite de tests unitarios del módulo en verde |
| Persistencia, modelos o migraciones | Tests de integración contra una base real, más la migración aplicada y revertida |
| Rutas HTTP, integraciones externas o UI | Verificación manual del flujo end-to-end, documentada en "Validation > Manual" |

---

## Fase 4 — Decisión

Checklist antes de mergear:

- [ ] Descripción no tiene secciones vacías sin justificación
- [ ] Ninguna capa nueva viola el placement de [`doc_architecture.md`](doc_architecture.md)
- [ ] Tests declarados en el PR pasan (o hay razón explícita documentada)
- [ ] No hay secrets, tokens ni credenciales hardcodeadas
- [ ] Rollback está definido con una sola oración concreta

**Si el PR pasa el checklist** → **Squash and merge**.

**Si quedan cambios pendientes** → dejar comentarios en la línea de código exacta, aplicar los ajustes y hacer push a la misma rama antes de mergear.

---

## Reglas de negocio de la revisión

- Ningún PR se mergea sin haber pasado el checklist de la Fase 4.
- Solo se permite **Squash and merge** (nunca merge commit ni rebase merge).
- Si el PR recibe commits nuevos después del review, repetir al menos las Fases 3 y 4 sobre el estado final.

---

## Referencia rápida

| Documento | Propósito |
|---|---|
| [`doc_git_workflow.md`](doc_git_workflow.md) | Flujo completo de ramas y PR |
| [`doc_verification_guide.md`](doc_verification_guide.md) | Comandos de verificación por tipo de cambio |
| [`doc_architecture.md`](doc_architecture.md) | Capas y placement rules del repositorio |
| [`.github/pull_request_template.md`](../.github/pull_request_template.md) | Template que deben usar los autores |
