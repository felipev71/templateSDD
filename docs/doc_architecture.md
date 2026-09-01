# Guía de Arquitectura — [Nombre del proyecto]

> **Plantilla.** Este archivo es la referencia canónica de arquitectura del repositorio
> y lo leen `/enrich-user-story` y `/code-review` antes de trabajar. Reemplaza todos
> los placeholders `<...>` por la realidad de tu proyecto antes del primer uso.
> Un archivo sin completar no bloquea los skills, pero los deja sin contexto.

## Propósito

Este documento es la referencia canónica de arquitectura para agentes IA que trabajan en este repositorio. Úsalo para decidir dónde va cada archivo nuevo, cómo se estructuran los módulos y qué límites no deben cruzarse.

## Estructura del repositorio

```
<nombre-del-repo>/
├── <módulo-backend>/     # <descripción breve>
├── <módulo-frontend>/    # <descripción breve>
├── ai-specs/             # Metodología SDD (agentes, skills, comandos)
└── docs/                 # Documentación técnica
```

---

## Módulo: `<módulo-backend>/`

### Stack

- **Runtime:** <lenguaje y versión>
- **Framework:** <framework>
- **Base de datos:** <motor + ORM>
- **Herramienta de migraciones:** <herramienta, ej. Alembic>
- **Framework de tests:** <framework, ej. pytest>
- **Deployment:** <destino>

### Estructura interna

```
<módulo-backend>/
├── <carpeta-app>/
│   ├── <entrypoint>          # Entry point, arranque, middleware
│   ├── <config>              # Configuración desde variables de entorno
│   ├── <transporte>/         # Rutas HTTP / handlers
│   ├── <dominio>/            # Reglas de negocio
│   ├── <persistencia>/       # Modelos y acceso a datos
│   └── <integraciones>/      # Clientes de servicios externos
└── tests/
```

### Capas y responsabilidades

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| Transporte | `<transporte>/` | Recibir peticiones, validar, despachar |
| Aplicación | `<dominio>/` | Orquestar casos de uso, gestionar estado |
| Dominio | `<dominio>/` | Reglas de negocio |
| Persistencia | `<persistencia>/` | Acceso a datos vía ORM |
| Integraciones | `<integraciones>/` | Clientes externos |

### Reglas de placement

1. Nueva ruta HTTP → `<transporte>/`
2. Nueva lógica de negocio → `<dominio>/`
3. Nuevo modelo de datos → `<persistencia>/` + migración
4. Nueva consulta a BD → capa de repositorio (ORM siempre)
5. Nueva integración externa → carpeta propia bajo `<integraciones>/`

**Excepciones documentadas:** si alguna regla tiene una excepción legítima y
permanente, decláralas aquí con su precedente en código. `/code-review` las lee
antes de reportar una violación de placement.

---

## Módulo: `<módulo-frontend>/`

### Stack

- **Runtime:** <lenguaje y versión>
- **Framework:** <framework>
- **Cliente HTTP:** <librería, ej. axios / fetch>
- **Router:** <librería de routing>
- **Librería de componentes UI:** <librería, ej. React Bootstrap / MUI>
- **Design tokens / estilos:** <archivo o convención, ej. src/index.css>
- **Deployment:** <destino>

### Estructura interna

```
<módulo-frontend>/
├── <carpeta-componentes>/    # Componentes de UI reutilizables
├── <carpeta-servicios>/      # Capa de servicios para comunicación con la API
└── <carpeta-rutas>/          # Configuración de routing
```

### Reglas de placement

1. Nueva pantalla o ruta → `<carpeta-rutas>/`
2. Componente reutilizable → `<carpeta-componentes>/`
3. Llamada a API → capa de servicios en `<carpeta-servicios>/`, nunca `fetch()` directo en un componente
4. Nueva ruta de API → validar la entrada en el borde

---

## Anti-patrones (no introducir)

- SQL raw fuera de la capa de repositorio
- Lógica de negocio en handlers de transporte
- Credenciales hardcodeadas en código fuente
- Rutas absolutas de máquinas externas en archivos de configuración
- Importaciones circulares entre capas
- `<anti-patrón propio del proyecto>`
