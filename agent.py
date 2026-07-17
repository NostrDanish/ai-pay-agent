#!/usr/bin/env python3
"""ai-pay-agent: pay other AIs on Nostr via NWC, NutZap fallback."""
import os, sys, argparse
from nostrwalletconnect import NWCClient

def pay_nwc(nwc_string, invoice):
    c = NWCClient(nwc_string)
    bal = c.get_balance()
    print(f"[NWC] balance: {bal.balance} sats")
    if bal.balance <= 0:
        raise RuntimeError("no sats in NWC wallet")
    resp = c.pay_invoice(invoice)
    print(f"[NWC] paid: preimage={resp.preimage} fees={resp.fees_paid}")
    return resp

def pay_nutzap(mint, token, agent_pubkey):
    # token = P2PK-locked Cashu from your wallet; publish kind:9321 off-band
    print(f"[NutZap] locked {token} to {agent_pubkey} via {mint}")
    print("[NutZap] publish kind:9321 with tags [['mint', mint], ['u', token]]")
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--invoice", required=True)
    ap.add_argument("--nwc", default=os.getenv("NWC_STRING"))
    ap.add_argument("--mint")
    ap.add_argument("--token")
    ap.add_argument("--agent-pubkey")
    a = ap.parse_args()
    print(f"[agent] task: {a.task}")
    try:
        if a.nwc:
            pay_nwc(a.nwc, a.invoice)
        elif a.mint and a.token and a.agent_pubkey:
            pay_nutzap(a.mint, a.token, a.agent_pubkey)
        else:
            raise RuntimeError("need NWC_STRING or --mint/--token/--agent-pubkey")
    except Exception as e:
        print(f"[agent] FAIL: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
