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

Referencias:
- `ai-specs/skills/` — workflows reutilizables disponibles en Claude Code
- `ai-specs/.agents/` — agentes especializados por rol
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
4. Revisar el diff en GitHub.
5. Merge con **Squash and merge**. Nunca push directo a `main`.

Guía completa: `docs/doc_git_workflow.md`
