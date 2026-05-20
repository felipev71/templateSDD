# Guía de Verificación — proyecto2026

## Propósito

Guía para elegir el camino de verificación correcto según el tipo de cambio. Usa la verificación más barata que pueda detectar el riesgo introducido.

## Estrategia general

1. Tests unitarios para cambios en lógica pura
2. Tests de integración para comportamiento multi-capa
3. Tests E2E o smoke manual cuando el comportamiento real del agente es el criterio de éxito

---

## `whatsapp-agent/` — comandos de verificación

### Cambié lógica pura (conversación, detección de idioma, parseo)

```bash
cd whatsapp-agent && python -m pytest tests/unit -q
```

### Cambié repositorio o modelos de base de datos

```bash
cd whatsapp-agent && python -m pytest tests/integration -q
```

### Cambié el webhook o la integración con WhatsApp

Verificación manual con payload de prueba:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"object":"whatsapp_business_account",...}'
```

### Arrancar el servidor local

```bash
cd whatsapp-agent && uvicorn app.main:app --reload --port 8000
```

### Health check

```bash
curl http://localhost:8000/health
```

### Verificar migraciones de BD

```bash
cd whatsapp-agent && alembic upgrade head
alembic current
```

---

## Verificación de agentes de clientes (`clientes/{cliente}/05-agentes/`)

Cada agente de cliente puede tener su propio README con instrucciones de verificación. Si no las tiene, el mínimo es:

1. Verificar que el agente arranca sin errores
2. Enviar un mensaje de prueba y verificar respuesta esperada
3. Confirmar que los datos se persisten correctamente

---

## Anti-patrones de verificación

- No usar E2E como primer y único recurso para cada cambio
- No confiar solo en pruebas manuales para bugs de integración
- No saltarse tests porque "es un cambio pequeño"
