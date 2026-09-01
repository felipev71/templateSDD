# Handoff — Tareas Pendientes

Registro vivo de lo que quedó abierto entre sesiones de trabajo. Es lo primero que
debe leer una sesión nueva antes de proponer en qué seguir.

## Protocolo

**Cuándo se abre un pendiente.** Cuando algo queda sin cerrar y su cierre no depende
de la sesión actual: una acción manual en una consola externa, una validación que
necesita datos que aún no existen, una decisión que espera a otra persona, o un
bug conocido que se decidió no atacar todavía. Lo que se resuelve dentro de la
misma sesión no se registra aquí.

**Cómo se escribe.** Una fila por pendiente. El título debe ser autocontenido —
que se entienda sin el contexto de la conversación que lo originó. Fecha límite en
formato ISO (`AAAA-MM-DD`). Estado en `pendiente`, `en_progreso` o `completada`.
La columna "Épica" agrupa pendientes de un mismo frente de trabajo; usa un código
corto y estable.

**Cómo se cierra.** Cambiar el estado de la fila a `completada`. No borrar la fila:
el histórico sirve para reconstruir qué pasó y cuándo.

**Cómo lo retoma la siguiente sesión.** Leer este archivo completo, filtrar por
estado distinto de `completada`, y contrastar contra el estado real del repositorio
antes de dar nada por vigente — un pendiente puede haberse resuelto sin que su fila
se actualizara.

## Pendientes activos

| Título | Responsable | Fecha límite | Estado | Épica |
|---|---|---|---|---|

<!-- Fila de ejemplo — borrar al registrar el primer pendiente real:
| Rotar la credencial de despliegue tras la migración | <persona> | 2026-01-31 | pendiente | INFRA |
-->
