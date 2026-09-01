#!/usr/bin/env python3
"""
Hook PreToolUse — Agent
Bloquea invocación de agentes de implementación si no se corrió /enrich-user-story.
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
                "🚫 SDD GATE — OBLIGATORIO\n"
                "Antes de invocar un agente de implementación debes verificar:\n"
                "1. ¿Se corrió /enrich-user-story en esta sesión?\n"
                "2. ¿El requisito está completamente cerrado (decisiones sin ambigüedad)?\n"
                "3. ¿El usuario aprobó el High-Level Technical Contract?\n\n"
                "Si alguna respuesta es NO → responde al usuario que debe correr "
                "/enrich-user-story primero y detén la implementación.\n"
                "NO procedas con el agente hasta que el requisito esté cerrado."
            )
        }))
except Exception:
    pass
