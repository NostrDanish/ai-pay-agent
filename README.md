# ai-pay-agent

Pay other AIs on Nostr for task automation. NWC (NIP-47) primary, NutZap (NIP-61) fallback.
Zero-dep beyond `nostrwalletconnect`. Authoritative state on relays.

## Setup
```
pip install nostrwalletconnect
export NWC_STRING="nostr+walletconnect://...?relay=...&secret=..."
python3 agent.py --task "summarize nostr" --invoice <bolt11>
```

## Flow
1. Receive task + Lightning invoice from AI counterparty
2. Check balance via NWC
3. Pay invoice
4. Verify payment result
5. If NWC unavailable, P2PK-lock Cashu to agent pubkey + publish kind:9321 (NutZap)
