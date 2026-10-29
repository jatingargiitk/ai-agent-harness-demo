# WITH HARNESS: same model + tools + a loop.
import json, re, urllib.request
MODEL = "qwen2.5:3b"   # free, runs locally via Ollama
TASK = "Read orders.txt, add up all the orders, then add 8% sales tax. What is the final total?"

def read_file(path):                       # TOOL 1: eyes
    return open(path).read()
def calculator(expression):                # TOOL 2: hands (only digits and + - * / ( ) .)
    if not re.fullmatch(r"[\d\s+\-*/().]+", expression): return "error: only numbers and + - * / ( ) allowed"
    return str(round(eval(expression), 2))
TOOLS = {"read_file": read_file, "calculator": calculator}
SPECS = [{"type": "function", "function": {"name": n, "description": d,
          "parameters": {"type": "object", "properties": {a: {"type": "string"}}, "required": [a]}}}
         for n, d, a in [("read_file", "Read a text file", "path"),
                         ("calculator", "Evaluate a math expression", "expression")]]

def chat(messages):
    req = urllib.request.Request("http://localhost:11434/api/chat",
        data=json.dumps({"model": MODEL, "messages": messages, "tools": SPECS, "stream": False,
                         "options": {"temperature": 0}}).encode())
    return json.load(urllib.request.urlopen(req))["message"]

print(f"👤 TASK: {TASK}\n")
messages = [{"role": "system", "content": "Use tools for every file read and every calculation, even simple sums. "
             "Never type a number a tool didn't give you. When fully done, reply: FINAL: <answer>"},
            {"role": "user", "content": TASK}]
for step in range(1, 9):                    # THE LOOP (max 8 steps = guardrail)
    reply = chat(messages); messages.append(reply)
    if not reply.get("tool_calls"):
        final = reply["content"].split("FINAL:")[-1].strip(" $\n")
        if "FINAL:" in reply["content"] and any(final == m["content"] for m in messages if m["role"] == "tool"):
            print(f"✅ {reply['content'].strip()}"); break   # done + answer came from a tool -> exit loop
        if "FINAL:" in reply["content"]:     # GUARDRAIL: answer must come from a tool
            print(f"🛡️ STEP {step}  guardrail: '{final}' didn't come from a tool, check again")
            messages.append({"role": "user", "content": "That number didn't come from a tool. Recheck each step with tools."}); continue
        print(f"🔁 STEP {step}  ⚠️  not done yet, harness says: keep going")
        messages.append({"role": "user", "content": "Not done. Do the next step with a tool."}); continue
    for call in reply["tool_calls"]:         # model asks, harness acts
        name, args = call["function"]["name"], call["function"]["arguments"]
        try: result = TOOLS[name](**args)
        except Exception as e: result = f"error: {e}"   # errors go back to the model
        print(f"🔁 STEP {step}  🔧 {name}({json.dumps(args)})\n   📄 {result.strip()}")
        messages.append({"role": "tool", "tool_name": name, "content": result})  # memory
