# Git Workflow — Felipe (repositorio personal)

## Propósito

Referencia canónica del flujo de trabajo con Git. Define cómo crear ramas, abrir PRs y mergear a `main`.

---

## Convención de ramas

```
feat/<descripcion-corta>   # Nueva funcionalidad
fix/<descripcion-corta>    # Corrección de bug
docs/<descripcion-corta>   # Solo documentación
chore/<descripcion-corta>  # Mantenimiento / configuración
```

**Reglas de nombrado:**
- Minúsculas y guiones medios, sin espacios ni caracteres especiales.
- Descripción concisa en español o inglés.
- Siempre crear desde `main` actualizado.

**Ejemplos válidos:**
- `feat/agente-recordatorios`
- `fix/error-encoding-pdf`
- `docs/guia-setup-local`
- `chore/actualizar-dependencias`

---

## Flujo paso a paso

### 1. Preparar la rama

```bash
git checkout main
git pull origin main
git checkout -b feat/nombre-del-cambio
```

### 2. Desarrollar siguiendo SDD

1. `/enrich-user-story` — cerrar el requisito antes de escribir código.
2. Plan aprobado — generar contrato técnico y aprobarlo.
3. Implementar con checkboxes verificables.
4. Commits con convención: `feat:`, `fix:`, `docs:`, `chore:`.

### 3. Generar descripción del PR

Antes de abrir el PR, ejecutar desde Claude Code:

```
/write-pr-report
```

Pegar el output en el campo de descripción del PR en GitHub.

### 4. Abrir el PR en GitHub

1. Ir a `https://github.com/felipev71/Felipe`.
2. Hacer clic en "Compare & pull request" o ir a **Pull requests → New pull request**.
3. Confirmar: Base `main` ← Compare `tu-rama`.
4. Pegar el output de `/write-pr-report` en la descripción.
5. Crear el PR.

### 5. Revisar y mergear

- Revisar el diff en la pestaña **Files changed** del PR.
- Verificar que los cambios tienen sentido y no introducen regresiones.
- Una vez satisfecho, hacer clic en **Merge pull request** usando **Squash and merge**.

---

## Reglas no negociables

- **Nunca hacer push directo a `main`** — usar siempre PRs.
- **Nunca usar `git push --force` en `main`** — está deshabilitado.
- **Solo Squash and merge** — mantiene el historial de `main` limpio con un commit por PR.

---

## Configuración de GitHub Settings (referencia)

Opciones activas en `https://github.com/felipev71/Felipe/settings/branches` (regla para `main`):

| Opción | Estado |
|--------|--------|
| Require a pull request before merging | ON |
| Required number of approvals | 0 (sin requerir otros revisores) |
| Allow force pushes | OFF |
| Allow deletions | OFF |

En `https://github.com/felipev71/Felipe/settings` (general):

| Opción | Estado |
|--------|--------|
| Allow merge commits | OFF |
| Allow squash merging | ON |
| Allow rebase merging | OFF |
| Automatically delete head branches | ON |

---

## Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `.github/pull_request_template.md` | Template del PR alineado con `/write-pr-report` |
| `CLAUDE.md` | Convención de ramas y metodología SDD (resumen) |
| `docs/doc_git_workflow.md` | Este documento |
