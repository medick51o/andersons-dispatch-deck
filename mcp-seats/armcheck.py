import json, subprocess, sys, os, glob, io, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SEATS = r"C:\Sync\Projects\andersons-dispatch-deck\mcp-seats"
PLAYPEN = r"C:\Sync\_playpen\cursor"
RESV = os.path.join(os.path.expanduser("~"), ".anderson-method", "reservations.json")

def seat(server):
    p = subprocess.Popen([sys.executable, os.path.join(SEATS, server)],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         text=True, encoding="utf-8", bufsize=1)
    def rpc(m):
        p.stdin.write(json.dumps(m)+"\n"); p.stdin.flush()
        if "id" in m: return json.loads(p.stdout.readline())
    return p, rpc

results = []
def check(label, ok, detail=""):
    results.append((label, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))

print("=== 1. all three seats start and list tools ===")
for srv, want in (("wmw_grok_mcp.py", ["grok","grok-reply"]),
                  ("wmw_gemini_mcp.py", ["gemini","gemini-reply"]),
                  ("wmw_cursor_mcp.py", ["cursor","cursor-reply"])):
    p, rpc = seat(srv)
    r = rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    v = r["result"]["serverInfo"]
    t = [x["name"] for x in rpc({"jsonrpc":"2.0","id":2,"method":"tools/list"})["result"]["tools"]]
    check(f"{srv:22} v{v['version']}", t == want, ",".join(t))
    p.stdin.close(); p.wait(timeout=10)

print("\n=== 2. the guards that cost money or safety ===")
p, rpc = seat("wmw_cursor_mcp.py")
rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
def cur(args):
    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":args}})["result"]
check("credit model refused without spend_credits", cur({"prompt":"x","model":"kimi-k3-high"})["isError"])
check("auto/UNKNOWN refused even WITH spend_credits", cur({"prompt":"x","model":"auto","spend_credits":True})["isError"])
check("model id with metacharacters refused", cur({"prompt":"x","model":"bad;id&whoami"})["isError"])
check("write-capable with no cwd refused", cur({"prompt":"x","always_approve":True})["isError"])
sysroot = os.environ.get("SystemRoot", r"C:\Windows")
check("write-capable in System32 refused", cur({"prompt":"x","always_approve":True,"cwd":os.path.join(sysroot,"System32")})["isError"])
check("YOLO on a non-allowlisted model refused",
      "WRITE REFUSED" in cur({"prompt":"x","model":"gpt-5.3-codex","always_approve":True,"cwd":PLAYPEN,"spend_credits":True})["content"][0]["text"])

# --- the guard, wired 2026-08-24 (council). Regression for the burn incident. ---
_empty = os.path.join(PLAYPEN, "_armcheck_emptyrepo")
os.makedirs(_empty, exist_ok=True)
subprocess.run(["git","-C",_empty,"init","-q"], capture_output=True)
check("build dispatch at an EMPTY repo refused (preflight)",
      "PREFLIGHT REFUSED" in cur({"prompt":"build it","always_approve":True,"cwd":_empty,
                                  "model":"composer-2.5"})["content"][0]["text"])
shutil.rmtree(_empty, ignore_errors=True)
check("no lease left behind after a refused dispatch",
      not (json.load(io.open(RESV, encoding="utf-8")).get("jobs") if os.path.exists(RESV) else {}))
p.stdin.close(); p.wait(timeout=10)

# --- the Gemini seat, audited 2026-08-24. Every one of these was LEGAL before. ---
p, rpc = seat("wmw_gemini_mcp.py")
rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
def gm(tool,args):
    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":tool,"arguments":args}})["result"]
check("gemini: reply escalating with no cwd refused",
      gm("gemini-reply",{"conversationId":"01a02b9c-384b-72d0-9c6f-f5ab60147aba","prompt":"x","always_approve":True})["isError"])
check("gemini: write-capable INSIDE System32 refused",
      gm("gemini",{"prompt":"x","always_approve":True,"cwd":os.path.join(sysroot,"System32")})["isError"])
check("gemini: write-capable inside HOME profile refused",
      gm("gemini",{"prompt":"x","always_approve":True,"cwd":os.path.join(os.path.expanduser("~"),"Documents")})["isError"])
check("gemini: a REAL project dir is still allowed (no false positive)",
      not gm("gemini",{"prompt":"reply with only OK","always_approve":True,"cwd":PLAYPEN})["isError"])
p.stdin.close(); p.wait(timeout=10)

# --- the escalation route the Cursor seat still had open (audit 2026-08-24) ---
_cur = io.open(os.path.join(SEATS,"wmw_cursor_mcp.py"), encoding="utf-8").read()
# anchor on the CODE line, not the word — the word also appears in the comment above it
_apr = [i for i, l in enumerate(_cur.splitlines()) if 'cmd += ["--approve-mcps"]' in l]
_lines = _cur.splitlines()
check("cursor: --approve-mcps confined to the write-capable path",
      bool(_apr) and all("if always_approve:" in _lines[i - 1] for i in _apr))

p, rpc = seat("wmw_grok_mcp.py")
rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
def gk(tool,args):
    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":tool,"arguments":args}})["result"]
check("grok: crafted sessionId cannot smuggle flags", gk("grok-reply",{"sessionId":"--always-approve","prompt":"x"})["isError"])
check("grok: reply escalating with no cwd refused", gk("grok-reply",{"sessionId":"01a02b9c-384b-72d0-9c6f-f5ab60147aba","prompt":"x","always_approve":True})["isError"])
p.stdin.close(); p.wait(timeout=10)

print("\n=== 3. meters readable ===")
r = subprocess.run([sys.executable, os.path.join(SEATS,"read-meters.py"), "--json"],
                   capture_output=True, text=True, encoding="utf-8", timeout=120)
try:
    d = json.loads(r.stdout)
    check("grok meter readable", d.get("grok",{}).get("weekly_percent_used") is not None,
          f"{d.get('grok',{}).get('weekly_percent_used')}%")
    check("cursor meter readable", d.get("cursor",{}).get("cursor_models_percent_used") is not None,
          f"{d.get('cursor',{}).get('cursor_models_percent_used')}%")
except Exception as e:
    check("meters readable", False, str(e))

print("\n=== 4. playpen intact, no stray spill files ===")
check("playpen exists", os.path.isdir(PLAYPEN))
spill = glob.glob(os.path.join(PLAYPEN,"prompts","*"))
check("no leftover prompt handoffs", not spill, f"{len(spill)} found")

bad = [l for l,ok,_ in results if not ok]
print(f"\n{'='*46}\n{len(results)-len(bad)}/{len(results)} PASS" + (f"  — FAILED: {bad}" if bad else "  — ALL ARMED"))
