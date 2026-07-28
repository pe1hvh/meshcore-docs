# -*- coding: utf-8 -*-
"""Reproduceert de MeshCore-opbouw van een direct message (PAYLOAD_TYPE_TXT_MSG),
   in beide routeringstoestanden: flood mét scope en direct zonder transport codes.

   Gevolgd: src/Mesh.cpp (createDatagram), src/Utils.cpp (encryptThenMAC),
   src/helpers/BaseChatMesh.cpp (composeMsgPacket, sendAckTo),
   src/helpers/TransportKeyStore.cpp (calcTransportCode).

   Let op: het ECDH shared secret is hier een vaste, uit een tekstseed afgeleide
   voorbeeldwaarde. Een echte waarde komt uit ed25519_key_exchange() op twee
   apparaten en is niet uit publieke gegevens te reproduceren. Alles wat daarna
   gebeurt — AES, MAC, transport code, framelengte — is wel exact het firmware-pad.
"""
import hashlib, hmac, struct
from Crypto.Cipher import AES

def sha256(b, n=32):            return hashlib.sha256(b).digest()[:n]
def hx(b, sep=' '):             return sep.join(f'{x:02X}' for x in b)

# ---- Utils::encrypt : AES-128 ECB, blok voor blok, laatste blok nul-gepad ----
def mc_encrypt(secret32, data):
    key = secret32[:16]                      # CIPHER_KEY_SIZE = 16
    pad = (-len(data)) % 16
    return AES.new(key, AES.MODE_ECB).encrypt(data + b'\x00'*pad)

# ---- Utils::encryptThenMAC : MAC(2) ‖ ciphertext ----
def mc_encrypt_then_mac(secret32, data):
    ct  = mc_encrypt(secret32, data)
    mac = hmac.new(secret32, ct, hashlib.sha256).digest()[:2]   # CIPHER_MAC_SIZE=2
    return mac + ct

# ---- TransportKey::calcTransportCode : HMAC-SHA256(key16, type ‖ payload)[:2] --
def transport_code(key16, payload_type, payload):
    d = hmac.new(key16, bytes([payload_type]) + payload, hashlib.sha256).digest()
    code = d[0] | (d[1] << 8)
    if code == 0: code += 1
    elif code == 0xFFFF: code -= 1
    return code, struct.pack('<H', code)

# ================= invoer =================
REGION = "nl-ov-zwo"
region_key = sha256(("#" + REGION).encode(), 16)

TS     = 1785412800                          # 2026-07-30 12:00:00 UTC
SENDER = "PE1HVH"
DEST   = "PE1RDP"
TEXT   = "Op Woensdag a.s. Blauwvingerdagen"

# Voorbeeld-identiteiten. De node-hash is de eerste byte van de public key.
pub_sender = sha256(("voorbeeld public key " + SENDER).encode())
pub_dest   = sha256(("voorbeeld public key " + DEST).encode())
src_hash   = pub_sender[0]
dest_hash  = pub_dest[0]

# Voorbeeld-ECDH-uitkomst; in werkelijkheid ed25519_key_exchange(), 32 bytes.
shared = sha256(f"voorbeeld shared secret {SENDER}<->{DEST}".encode())

PATH   = bytes([0xA3, 0x7F])                 # dezelfde twee repeaters als in
PATH_LEN = 0x02                              # example-calculation.py: 2 hops, 1-byte

# ================= klaartekst =================
# timestamp(4) ‖ flags(1) ‖ tekst   — géén "AFZENDER: " ervoor, anders dan bij
# een kanaalbericht: de afzender staat al als src_hash in het pakket.
TXT_TYPE_PLAIN, ATTEMPT = 0, 0
flags = (TXT_TYPE_PLAIN << 2) | ATTEMPT
plain = struct.pack('<I', TS) + bytes([flags]) + TEXT.encode()

body    = mc_encrypt_then_mac(shared, plain)          # MAC(2) ‖ ciphertext
payload = bytes([dest_hash, src_hash]) + body
code, wire = transport_code(region_key, 0x02, payload)

hdr_direct = (0x02 << 2) | 0x02              # 0x0A  ROUTE_TYPE_DIRECT
hdr_scoped = (0x02 << 2) | 0x00              # 0x08  ROUTE_TYPE_TRANSPORT_FLOOD

print("DIRECT MESSAGE  %s -> %s" % (SENDER, DEST))
print("  dest hash / src hash : %02X / %02X" % (dest_hash, src_hash))
print("  klaartekst (%d bytes): %s" % (len(plain), hx(plain)))
print("    timestamp %s  flags %02X  tekst %d tekens"
      % (hx(plain[:4]), flags, len(TEXT)))
print("  cipher MAC           :", hx(body[:2]))
print("  cijfertekst (%d)     : %s" % (len(body)-2, hx(body[2:])))
print("  payload len          :", len(payload))
print("  transport code       : 0x%04X -> wire %s" % (code, hx(wire)))
print()

frame_d = bytes([hdr_direct]) + bytes([PATH_LEN]) + PATH + payload
frame_f = bytes([hdr_scoped]) + wire + b'\x00\x00' + bytes([PATH_LEN]) + PATH + payload

print("  FRAME direct        (%d bytes, header %02X):" % (len(frame_d), hdr_direct))
print("   ", hx(frame_d))
print("  FRAME flood+scope   (%d bytes, header %02X):" % (len(frame_f), hdr_scoped))
print("   ", hx(frame_f))
print("  verschil            : %d bytes (%.1f%% meer)"
      % (len(frame_f)-len(frame_d), 100*(len(frame_f)-len(frame_d))/len(frame_d)))
print()

# ================= de ACK =================
# BaseChatMesh::sendAckTo : SHA256(timestamp ‖ flags ‖ tekst ‖ pubkey afzender)[:4]
# gevolgd door 1 byte pogingnummer en 1 willekeurige byte -> 6 bytes payload.
ack4 = sha256(plain + pub_sender, 4)
print("ACK")
print("  vergeleken hash (4) :", hx(ack4))
print("  payload             : %s <attempt> <random>  = 6 bytes" % hx(ack4))
print("  frame direct, 0 hops: %d bytes" % (1 + 1 + 6))

# ================= overhead per tekstlengte =================
print()
print("OVERHEAD per tekstlengte (2 hops, 1-byte hashes)")
print("  tekens  klaartekst  cijfertekst  payload  direct  flood+scope")
for n in (10, 33, 60, 120):
    p  = 4 + 1 + n
    ct = p + ((-p) % 16)
    pl = 1 + 1 + 2 + ct
    print("  %6d  %10d  %11d  %7d  %6d  %11d"
          % (n, p, ct, pl, 1+1+2+pl, 1+4+1+2+pl))
