#!/usr/bin/env python3
"""
Hook PreToolUse — Agent
Recuerda el gate SDD antes de invocar agentes de implementación.

No bloquea la invocación: el hook no tiene forma de saber si
/enrich-user-story se corrió en esta sesión (no hay estado persistente
entre invocaciones), así que solo reinyecta el recordatorio para que el
asistente lo autoevalúe. El cumplimiento real del gate depende de que el
asistente siga esta instrucción, igual que la regla equivalente en CLAUDE.md.
"""
import json
import sys

SDD_AGENTS = {"backend-developer", "frontend-developer"}

try:
    data = json.load(sys.stdin)
    subagent = data.get("tool_input", {}).get("subagent_type", "")
    if subagent in SDD_AGENTS:
        print(json.dumps({
            "systemMessage": (
                "SDD GATE — RECORDATORIO\n"
                "Antes de invocar un agente de implementación debes verificar:\n"
                "1. ¿Se corrió /enrich-user-story en esta sesión?\n"
                "2. ¿El requisito está completamente cerrado (decisiones sin ambigüedad)?\n"
                "3. ¿El usuario aprobó el High-Level Technical Contract?\n\n"
                "Si alguna respuesta es NO → responde al usuario que debe correr "
                "/enrich-user-story primero y detén la implementación.\n"
                "NO procedas con el agente hasta que el requisito esté cerrado."
            )
        }))
except Exception as e:
    print(f"sdd-check.py: error al procesar el hook: {e}", file=sys.stderr)
