from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct",
    dtype=torch.float16,
    device_map="auto"
)

def generateEmail(relevantInfo):
    messages = [
        {"role": "user", "content": f"Write ONLY a short cold outreach email, no preamble or reasoning. \
            To: {relevantInfo['name']} at {relevantInfo['company']}. \
            Property in {relevantInfo['county']}, {relevantInfo['state']}. \
            Selling elise.ai, a SaaS product to help manage rental properties. \
            Area stats: {json.dumps(relevantInfo['county_stats'])}. \
            News: {json.dumps(relevantInfo['news'])}. \
            Under 100 words. Sign off as 'The elise.ai Team'. Start with 'Hello'."},
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    decoded = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

    if "Hello" in decoded:
        decoded = decoded[decoded.index("Hello"):]

    return decoded