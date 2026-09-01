# Guía de Verificación — [Nombre del proyecto]

## Propósito

Guía para elegir el camino de verificación correcto según el tipo de cambio. Usa la verificación más barata que pueda detectar el riesgo introducido.

## Estrategia general

1. Tests unitarios para cambios en lógica pura
2. Tests de integración para comportamiento multi-capa
3. Tests E2E o smoke manual cuando el comportamiento real del sistema es el criterio de éxito

---

## `<módulo-backend>/` — comandos de verificación

> Reemplaza los comandos de ejemplo por los reales del proyecto, alineados con la
> estructura declarada en `docs/doc_architecture.md`.

### Cambié lógica pura (dominio, parseo, reglas de negocio)

```bash
cd <módulo-backend> && python -m pytest tests/unit -q
```

### Cambié repositorio o modelos de base de datos

```bash
cd <módulo-backend> && python -m pytest tests/integration -q
```

### Cambié una ruta HTTP o una integración externa

Verificación manual con payload de prueba:

```bash
curl -X POST http://localhost:8000/<ruta> \
  -H "Content-Type: application/json" \
  -d '{"...":"..."}'
```

### Arrancar el servidor local

```bash
cd <módulo-backend> && uvicorn app.main:app --reload --port 8000
```

### Health check

```bash
curl http://localhost:8000/health
```

### Verificar migraciones de BD

```bash
cd <módulo-backend> && alembic upgrade head
alembic current
```

---

## `<módulo-frontend>/` — comandos de verificación

```bash
cd <módulo-frontend> && npm test
```

---

## Anti-patrones de verificación

- No usar E2E como primer y único recurso para cada cambio
- No confiar solo en pruebas manuales para bugs de integración
- No saltarse tests porque "es un cambio pequeño"
