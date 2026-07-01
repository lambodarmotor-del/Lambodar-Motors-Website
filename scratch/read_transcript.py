import os
import json

def read_user_messages():
    path = r'C:\Users\Harshil\.gemini\antigravity\brain\2f3d1a84-c834-40f4-9f14-81b3340a3ed6\.system_generated\logs\transcript.jsonl'
    if not os.path.exists(path):
        print("Transcript file not found.")
        return
        
    messages = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    messages.append((data.get('step_index'), data.get('content')))
            except Exception as e:
                pass
                
    print(f"Total user messages found: {len(messages)}")
    print("\n--- Recent User Messages ---")
    for step_idx, content in messages[-15:]:
        print(f"Step {step_idx}:")
        print(content.encode('ascii', errors='replace').decode('ascii'))
        print("-" * 50)

if __name__ == '__main__':
    read_user_messages()
