#!/usr/bin/env python3
"""
Gera o custom.txt assinado para o cliente Suporte Raiget.

Formato esperado pelo RustDesk (src/common.rs::read_custom_client):
1. JSON com app-name, default-settings, override-settings, etc.
2. Serializa em bytes JSON.
3. Assina com ed25519 (modo combined: signature || message), via libsodium.
4. base64 (standard, with padding) do resultado.
5. Conteúdo do custom.txt = string base64.
"""
import base64, json, sys
from pathlib import Path
import nacl.signing

HERE = Path(__file__).parent
KEYPAIR = json.loads((HERE / "keypair.json").read_text())

PRIVATE_KEY_B64 = KEYPAIR["private"]
PUBLIC_KEY_B64 = KEYPAIR["public"]

config = {
    "app-name": "Suporte Raiget",
    "default-settings": {
        "custom-rendezvous-server": "debian.raiget.com",
        "relay-server": "debian.raiget.com",
        "key": "9Xzzle845RKd+hT3pOaTTd97bxHBhpuHIm6UBny2VsE=",
        "api-server": "",
    },
    "override-settings": {},
}

payload = json.dumps(config, separators=(",", ":")).encode("utf-8")

sk = nacl.signing.SigningKey(base64.b64decode(PRIVATE_KEY_B64))
signed = sk.sign(payload)
signed_bytes = bytes(signed)

custom_txt = base64.b64encode(signed_bytes).decode("ascii")

out_path = HERE / "custom.txt"
out_path.write_text(custom_txt)

print(f"Public key (em src/common.rs:2187 const KEY): {PUBLIC_KEY_B64}")
print(f"Payload JSON ({len(payload)} bytes): {payload.decode()}")
print(f"Signed bytes: {len(signed_bytes)} bytes")
print(f"custom.txt ({len(custom_txt)} chars) escrito em: {out_path}")
