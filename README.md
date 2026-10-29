# ai-agent-harness-demo

Same AI model, same question. Without a harness it fails. With a ~40-line Python harness it gets the right answer.

This is the demo code from the YouTube episode **ChatGPT vs AI Agent: Harness Explained**.

- `no_harness.py`: just the model. No tools, no loop.
- `harness.py`: the same model plus a harness:
  - **Loop**: the model keeps going, one step at a time.
  - **2 tools**: `read_file` (eyes) and `calculator` (hands, digits and `+ - * / ( )` only).
  - **Memory**: every tool result goes back into the conversation.
  - **Guardrails**: an 8-step limit, and a final answer must match a number a tool actually returned.
- `orders.txt`: the five orders the task adds up.

The task: *"Read orders.txt, add up all the orders, then add 8% sales tax. What is the final total?"*

## Run it (free, offline)

You need Python 3 (standard library only) and [Ollama](https://ollama.com).

```bash
ollama pull qwen2.5:3b
python3 no_harness.py   # the model only describes the steps
python3 harness.py      # the model uses the tools and answers
```

## What you'll see

Without the harness, the model explains how you *would* solve it and never gives a number.

With the harness:

```
🔁 STEP 1  🔧 read_file({"path": "orders.txt"})
🔁 STEP 2  🔧 calculator({"expression": "(49+120+15+89+35)*1.08"})
   📄 332.64
✅ FINAL: 332.64
```

Small local models aren't deterministic across machines, so your exact steps may differ.

## Try this

Add a third tool (a web search, a currency converter, anything): write a function, add it to `TOOLS`, and add its entry to `SPECS`.

## License

[MIT](LICENSE)
