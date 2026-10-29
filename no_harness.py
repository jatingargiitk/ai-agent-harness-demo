# NO HARNESS: just the model. No tools, no loop.
import json, urllib.request
MODEL = "qwen2.5:3b"   # free, runs locally via Ollama
TASK = "Read orders.txt, add up all the orders, then add 8% sales tax. What is the final total?"

def chat(messages):
    req = urllib.request.Request("http://localhost:11434/api/chat",
        data=json.dumps({"model": MODEL, "messages": messages, "stream": False,
                         "options": {"temperature": 0}}).encode())
    return json.load(urllib.request.urlopen(req))["message"]

print(f"👤 TASK: {TASK}\n")
reply = chat([{"role": "system", "content": "Be brief."}, {"role": "user", "content": TASK}])
print(f"🧠 MODEL: {reply['content']}")
