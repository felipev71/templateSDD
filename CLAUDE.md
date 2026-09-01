# [Nombre del proyecto] — contexto para Claude Code

Describe aquí el propósito del proyecto y el contexto relevante para que Claude Code entienda el negocio detrás del código.

## Proyectos / módulos

Los módulos se organizan en carpetas en la raíz del repositorio. Cada carpeta es un proyecto independiente.

## Principios de desarrollo

- Todo desarrollo sigue **Spec-Driven Development (SDD)**.
- Flujo de PR: crear rama → desarrollar → PR → revisión → Squash and merge.

## Metodología de desarrollo: SDD

Todo nuevo desarrollo sigue **Spec-Driven Development (SDD)**. El flujo es:

1. Cerrar el requisito formalmente con `/enrich-user-story` antes de escribir código.
2. Generar un contrato técnico (plan aprobado) antes de implementar.
3. Ejecutar con checkboxes verificables.
4. Documentar el PR con `/write-pr-report`.

### Regla de gate — OBLIGATORIA

Antes de escribir, editar o generar cualquier código de implementación para una funcionalidad nueva o un cambio de comportamiento, el asistente DEBE verificar que:

1. `/enrich-user-story` fue ejecutado en esta sesión y produjo un requisito cerrado.
2. El usuario aprobó explícitamente el requisito antes de proceder.

Si alguna de las dos condiciones no se cumple:
- **Rechazar la implementación.**
- Informar al usuario: _"Para continuar debes correr `/enrich-user-story` primero y cerrar el requisito."_
- No escribir ni editar ningún archivo de código fuente hasta que el requisito esté cerrado y aprobado.

Esta regla aplica sin excepción. No aplica a correcciones de typos, ajustes de configuración triviales ni cambios exclusivos de documentación.

Referencias:
- `ai-specs/skills/` — workflows reutilizables disponibles en Claude Code
- `ai-specs/.agents/` — agentes especializados por rol
- `docs/doc_architecture.md` — arquitectura del repositorio (leer antes de planificar)
- `docs/doc_ai_planning_mode.md` — reglas de planificación para IA
- `docs/doc_verification_guide.md` — cómo verificar cambios por tipo

## Convención de ramas y flujo de PR

### Nombrado de ramas

```
feat/<descripcion-corta>   # Nueva funcionalidad
fix/<descripcion-corta>    # Corrección de bug
docs/<descripcion-corta>   # Solo documentación
chore/<descripcion-corta>  # Mantenimiento / configuración
```

### Flujo estándar

1. Crear rama desde `main` actualizado con la convención anterior.
2. Desarrollar siguiendo SDD: `/enrich-user-story` → plan aprobado → implementación.
3. Antes de abrir el PR, ejecutar `/write-pr-report` y pegar el output en GitHub.
4. Revisar el diff en GitHub siguiendo el checklist de `docs/doc_review_process.md`.
5. Merge con **Squash and merge**. Nunca push directo a `main`.

Guía completa: `docs/doc_git_workflow.md`

## Proceso de revisión de PRs — arranque automático

Cuando el usuario indique que quiere revisar un PR — frases como "vamos a revisar", "quiero revisar el PR", "hay algo para aprobar", "empecemos la revisión" — hacer lo siguiente **sin esperar instrucción adicional**:

1. Ejecutar `gh pr list --repo <owner>/<repo> --state open` para ver los PRs abiertos.
2. Si hay un PR concreto indicado, invocar el skill `/code-review <número-PR>` directamente.
3. Seguir las 4 fases definidas en `docs/doc_review_process.md` en orden.
4. Al terminar el análisis, preguntar si registrar el review en GitHub.

**Verificación del autor:** siempre confirmar el autor real del PR con `git log --format="%an" origin/<rama>` antes de mencionar quién lo hizo. Nunca asumir por el contexto del proyecto.

Referencia completa del proceso: `docs/doc_review_process.md`
