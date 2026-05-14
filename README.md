# 🏭 Plant Call Attention System — ACME Reporter

> Sistema de reporte interactivo para gestión de llamadas de atención en planta industrial, con arquitectura monolito modular y roadmap hacia notificaciones multicanal en tiempo real.

---

## 📋 Descripción General

Este proyecto automatiza el monitoreo y reporte de **llamadas de atención entre departamentos** en planta industrial. Consume directamente el archivo `acme.export.csv` generado por la plataforma ACME, produce reportes interactivos con gráficas y estadísticas, y está diseñado para escalar progresivamente hacia un **sitio web con alarmas y notificaciones multicanal**.

El sistema permite que cada departamento de la planta (Mantenimiento, Producción, Calidad, Seguridad, Logística, etc.) tenga visibilidad inmediata de los llamados que le corresponden, con el objetivo de **minimizar el tiempo de respuesta**.

---

## 🗂️ Estructura del Proyecto

```
acme-reporter/
│
├── main.py                  # Reporte interactivo: vista diaria/actual
├── mainyear.py              # Reporte anual: tendencias y comparativas
│
├── middleware/              # (Roadmap) Capa de notificaciones multicanal
│   ├── __init__.py
│   ├── config.py            # Configuración por canal (env vars / YAML)
│   ├── dispatcher.py        # Enrutador central de alertas
│   └── channels/
│       ├── sms.py
│       ├── email.py
│       ├── telegram.py
│       ├── whatsapp.py
│       ├── teams.py
│       ├── slack.py
│       ├── discord.py
│       └── google_chat.py
│
├── web/                     # (Roadmap) Capa web / dashboard
│   ├── app.py               # Flask / FastAPI entry point
│   ├── templates/
│   └── static/
│
├── data/
│   └── acme.export.csv      # Archivo fuente exportado por la plataforma ACME
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

### Requisitos

- Python 3.9+
- pip

### Dependencias

```txt
matplotlib>=3.4.2
pandas>=2.3.3
```

> Las librerías `requests` y `beautifulsoup4` están disponibles para activarse cuando se habilite el fetch directo a la plataforma ACME.

### Setup

```bash
git clone https://github.com/tu-org/acme-reporter.git
cd acme-reporter
pip install -r requirements.txt
```

---

## 🚀 Uso

### Reporte diario / actual

```bash
python main.py
```

- Lee `data/acme.export.csv` directamente desde la plataforma ACME vía fetch HTTP.
- Genera gráficas interactivas con `matplotlib`.
- Muestra llamados activos por departamento, tiempos de respuesta y estatus.

### Reporte anual

```bash
python mainyear.py
```

- Análisis histórico por mes y año.
- Comparativas entre departamentos.
- Exporta resumen en gráficas de tendencia.

---

## 🔄 Flujo de Datos

```
Plataforma ACME
      │
      │  HTTP fetch
      ▼
acme.export.csv
      │
      │  pandas (limpieza y transformación)
      ▼
DataFrame procesado
      │
      ├──► main.py ──► Reporte diario (matplotlib)
      │
      └──► mainyear.py ──► Reporte anual (matplotlib)
```

---

## 🏗️ Arquitectura: Monolito Modular

El proyecto sigue una arquitectura de **monolito modular**: un único proceso/despliegue con responsabilidades claramente separadas en módulos independientes. Esto facilita el mantenimiento actual y la migración futura a microservicios si fuese necesario.

```
┌─────────────────────────────────────────────────────┐
│                  ACME Reporter App                  │
│                                                     │
│  ┌─────────────┐   ┌──────────────┐                 │
│  │  Data Layer │   │ Report Layer │                 │
│  │  (pandas)   │──►│ (matplotlib) │                 │
│  └─────────────┘   └──────────────┘                 │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │           Middleware de Notificaciones       │   │
│  │                                              │   │
│  │  Dispatcher ──► SMS / Email / Telegram /     │   │
│  │                 WhatsApp / Teams / Slack /   │   │
│  │                 Discord / Google Chat        │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │              Web Layer (Roadmap)             │   │
│  │         Dashboard + Alarmas en tiempo real   │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 📡 Roadmap de Features

### ✅ Fase 1 — Core (actual)
- [x] Fetch directo del `acme.export.csv` desde la plataforma ACME
- [x] Reporte interactivo diario (`main.py`)
- [x] Reporte anual con tendencias (`mainyear.py`)
- [x] Visualizaciones con `matplotlib` y `pandas`

### 🔧 Fase 2 — Middleware de Notificaciones
- [ ] Alarmas configurables por umbral de tiempo de respuesta
- [ ] Notificaciones por **SMS** (Twilio / AWS SNS)
- [ ] Notificaciones por **Email** (SMTP / SendGrid)
- [ ] Bot de **Telegram**
- [ ] Mensajes de **WhatsApp** (Twilio / Meta Cloud API)
- [ ] Tarjetas adaptativas en **Microsoft Teams** (webhooks)
- [ ] Mensajes en **Slack** (Slack API / webhooks)
- [ ] Embeds en **Discord** (webhooks)
- [ ] Mensajes en **Google Chat** (webhooks)
- [ ] Configuración por canal desde variables de entorno o archivo YAML

### 🌐 Fase 3 — Sitio Web
- [ ] Dashboard web en tiempo real (Flask / FastAPI + HTMX o React)
- [ ] Panel de administración de departamentos y umbrales
- [ ] Historial de llamados con filtros
- [ ] Autenticación por departamento
- [ ] Despliegue en servidor de planta o nube privada

---

## 🔔 Configuración del Middleware de Notificaciones (Roadmap)

Cada canal se habilita y configura de forma independiente. Ejemplo de configuración futura (`middleware/config.yaml`):

```yaml
notifications:
  sms:
    enabled: true
    provider: twilio
    account_sid: "ACxxxx"
    auth_token: "xxxx"
    from_number: "+1234567890"

  email:
    enabled: true
    smtp_host: "smtp.empresa.com"
    smtp_port: 587
    from: "alertas@empresa.com"

  telegram:
    enabled: false
    bot_token: "xxxx"
    chat_id: "-100xxxx"

  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/xxxx"

  teams:
    enabled: true
    webhook_url: "https://outlook.office.com/webhook/xxxx"

  discord:
    enabled: false
    webhook_url: "https://discord.com/api/webhooks/xxxx"

  whatsapp:
    enabled: false
    provider: twilio
    from_number: "whatsapp:+14155238886"

  google_chat:
    enabled: false
    webhook_url: "https://chat.googleapis.com/v1/spaces/xxxx/messages"
```

---

## 🧩 Decisiones de Diseño

| Decisión | Justificación |
|---|---|
| Monolito modular | Inicio simple, fácil mantenimiento, sin overhead de microservicios |
| pandas + matplotlib | Stack estable, amplia documentación, suficiente para el volumen de datos de planta |
| Middleware como módulo separado | Permite agregar o quitar canales sin tocar la lógica de reportes |
| Config por YAML / env vars | Cada instalación de planta puede tener canales distintos sin tocar código |
| Fetch directo al CSV de ACME | Sin dependencia de exportaciones manuales; datos siempre actualizados |

---

## 🤝 Contribuir

1. Haz fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nombre-canal`
3. Haz commit de tus cambios: `git commit -m 'feat: agregar notificación por Discord'`
4. Abre un Pull Request

---

## 📄 Licencia

MIT — uso libre para proyectos internos de planta.

---

> **Proyecto en desarrollo activo.** Las fases 2 y 3 se irán integrando de forma incremental manteniendo compatibilidad con los scripts actuales.
