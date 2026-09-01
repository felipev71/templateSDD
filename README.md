# [Nombre del proyecto]

Descripción breve del proyecto.

Metodología: **Spec-Driven Development (SDD)** con Claude Code.

## Inicio rápido

1. Clona este repositorio (o úsalo como template desde GitHub).
2. Abre la carpeta en Claude Code.
3. Edita `CLAUDE.md` con el contexto de tu proyecto.
4. Comienza con `/enrich-user-story` antes de escribir código.

## Skills disponibles

| Skill | Uso |
|-------|-----|
| `/enrich-user-story` | Cierra el requisito antes de implementar (gate obligatorio del flujo SDD) |
| `/write-pr-report` | Genera la descripción del PR |
| `/code-review` | Autorevisión de un PR contra los estándares del repo antes de mergear |
| `/frontend-design` | Guía de diseño visual al construir o rediseñar UI |
| `/commit` | Orquesta commit + PR |
| `/explain` | Aprende conceptos del código |
| `/meta-prompt` | Reescribe un prompt ambiguo como uno preciso y accionable |

## Sincronización

Este template se sincronizó por última vez el **2026-09-01** contra el repositorio
interno de origen en su commit `7fbd423`, portando la evolución de la metodología
SDD (recordatorio del gate SDD vía hook, skill de code-review, proceso formal de
revisión de PRs, handoff entre sesiones) y genericizando todo dato específico del
negocio de origen. Es una copia manual, no un mecanismo de sincronización
automática — la próxima actualización también será manual.

> El hook `.claude/hooks/sdd-check.py` es un recordatorio, no un bloqueo forzado:
> no hay estado persistente entre invocaciones para verificar si el requisito
> ya se cerró, así que el cumplimiento del gate depende de que el asistente
> siga la instrucción.
