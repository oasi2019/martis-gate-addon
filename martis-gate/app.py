import json
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPTIONS_PATH = "/data/options.json"
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN", "")

def load_options():
    try:
        with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

@app.get("/")
def index():
    return jsonify({
        "ok": True,
        "service": "Martis Gate",
        "message": "Servizio attivo"
    })

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/open")
def open_gate():
    data = request.get_json(silent=True) or {}
    pin = str(data.get("pin", "")).strip()

    # PIN di test temporaneo
    if pin != "1234":
        return jsonify({
            "ok": False,
            "message": "Codice non valido"
        }), 401

    options = load_options()
    script_entity_id = options.get("ha_script_entity_id", "script.apri_varco_martis_gate")

    url = "http://supervisor/core/api/services/script/turn_on"
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": script_entity_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.ok:
            return jsonify({
                "ok": True,
                "message": "Apertura inviata correttamente"
            })
        return jsonify({
            "ok": False,
            "message": f"Errore Home Assistant: {response.status_code}"
        }), 500
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Errore di comunicazione: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
