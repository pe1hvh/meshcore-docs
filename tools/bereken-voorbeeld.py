# -*- coding: utf-8 -*-
"""Reproduceert de MeshCore-opbouw van een kanaalbericht, exact volgens
   src/Mesh.cpp (createGroupDatagram), src/Utils.cpp (encryptThenMAC),
   src/helpers/TransportKeyStore.cpp (getAutoKeyFor, calcTransportCode)."""
import hashlib, hmac, struct, base64
from Crypto.Cipher import AES

def sha256(b, n=32):            return hashlib.sha256(b).digest()[:n]
def hx(b, sep=' '):             return sep.join(f'{x:02X}' for x in b)

# ---- Utils::encrypt : AES-128 ECB, blok voor blok, laatste blok nul-gepad ----
def mc_encrypt(secret32, data):
    key = secret32[:16]                      # CIPHER_KEY_SIZE = 16
    pad = (-len(data)) % 16
    buf = data + b'\x00'*pad
    return AES.new(key, AES.MODE_ECB).encrypt(buf)

# ---- Utils::encryptThenMAC : MAC(2) ‖ ciphertext ; HMAC-sleutel = 32 bytes ----
def mc_encrypt_then_mac(secret32, data):
    ct  = mc_encrypt(secret32, data)
    mac = hmac.new(secret32, ct, hashlib.sha256).digest()[:2]   # PUB_KEY_SIZE=32
    return mac + ct

# ---- TransportKey::calcTransportCode : HMAC-SHA256(key16, type ‖ payload)[:2] --
def transport_code(key16, payload_type, payload):
    d = hmac.new(key16, bytes([payload_type]) + payload, hashlib.sha256).digest()
    code = d[0] | (d[1] << 8)                # uint16, little-endian in geheugen
    if code == 0: code += 1
    elif code == 0xFFFF: code -= 1
    return code, struct.pack('<H', code)     # wire-bytes

# ================= invoer =================
REGION = "nl-ov-zwo"
# getTransportKeysFor(): kale naam -> impliciete hashtag-regio -> SHA-256("#naam")[:16]
region_key = sha256(("#" + REGION).encode(), 16)

# kanaal A: hashtag #zwolle  (PSK door de app uit de naam afgeleid)
psk_hashtag = sha256("#zwolle".encode(), 16)
# kanaal B: private "zwolle" (PSK willekeurig, hier een vaste voorbeeldwaarde)
psk_private = bytes.fromhex("3f8c1a94d20b67e5aa41c7053e9d8b62")

TS     = 1785412800                          # 2026-07-30 12:00:00 UTC
SENDER = "PE1HVH"      # moet gelijk zijn aan de doctekst in techniek-scope.md
TEXT   = "Op Woensdag a.s. Blauwvingerdagen"

plain = struct.pack('<I', TS) + b'\x00' + f"{SENDER}: {TEXT}".encode()

print("REGIO", REGION)
print("  transport key = SHA-256(\"#%s\")[:16] = %s" % (REGION, hx(region_key,'')))
print()
print("PLAINTEXT (%d bytes) = %s" % (len(plain), hx(plain)))
print()

for label, name, psk in [("A", "#zwolle (hashtag)", psk_hashtag),
                         ("B", "zwolle (private)", psk_private)]:
    secret32 = psk + b'\x00'*16              # channel.secret[32], 128-bits sleutel
    ch_hash  = sha256(psk, 32)[0]            # sha256 over 16 bytes -> hash[0]
    body     = mc_encrypt_then_mac(secret32, plain)
    payload  = bytes([ch_hash]) + body
    code, wire = transport_code(region_key, 0x05, payload)

    print(f"--- KANAAL {label}: {name} ---")
    print("  PSK (base64)      :", base64.b64encode(psk).decode())
    print("  PSK (hex)         :", hx(psk,''))
    print("  channel hash      : %02X" % ch_hash)
    print("  cipher MAC        :", hx(body[:2]))
    print("  cijfertekst (%d)  : %s" % (len(body)-2, hx(body[2:])))
    print("  payload len       :", len(payload))
    print("  transport_code_1  : 0x%04X  -> wire bytes %s" % (code, hx(wire)))
    hdr_scoped   = (0x05 << 2) | 0x00
    hdr_unscoped = (0x05 << 2) | 0x01
    print("  header gescoopt   : %02X   (route 0x00 TRANSPORT_FLOOD)" % hdr_scoped)
    print("  header ongescoopt : %02X   (route 0x01 FLOOD)" % hdr_unscoped)
    print("  frame 0 hops      : gescoopt %d bytes / ongescoopt %d bytes"
          % (1+4+1+len(payload), 1+1+len(payload)))
    print("  frame 2 hops      : gescoopt %d bytes / ongescoopt %d bytes"
          % (1+4+1+2+len(payload), 1+1+2+len(payload)))
    print("  VOLLEDIG FRAME, gescoopt, 2 hops (pad A3 7F):")
    frame = bytes([hdr_scoped]) + wire + b'\x00\x00' + bytes([0x02, 0xA3, 0x7F]) + payload
    print("   ", hx(frame))
    print("  VOLLEDIG FRAME, ongescoopt, 2 hops:")
    frame_u = bytes([hdr_unscoped]) + bytes([0x02, 0xA3, 0x7F]) + payload
    print("   ", hx(frame_u))
    print()
