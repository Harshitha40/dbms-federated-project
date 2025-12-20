# Migration to Groq API

## Summary
Successfully migrated from OpenAI GPT-3.5-turbo to **Groq Qwen3-32B** for natural language query processing.

---

## What Changed

### ✅ Updated Files:
1. **backend/config.py**
   - Changed: `OPENAI_API_KEY` → `GROQ_API_KEY`
   - Updated comment with Groq console URL

2. **backend/llm_query.py**
   - Imports: `from openai import OpenAI` → `from groq import Groq`
   - Client: `OpenAI(api_key)` → `Groq(api_key)`
   - Model: `gpt-3.5-turbo` → `qwen/qwen3-32b`
   - API call: Updated to use streaming with Groq parameters
   - Temperature: 0.3 → 0.6
   - Max tokens: 500 → 4096
   - Added: `top_p=0.95`, `reasoning_effort="default"`, `stream=True`

3. **backend/requirements.txt**
   - Removed: `openai==1.12.0`
   - Added: `groq==0.11.0`

4. **LLM_SETUP.md**
   - Completely updated for Groq
   - New URL: https://console.groq.com/keys
   - Updated pricing info (FREE!)
   - New rate limits: 30/min, 14,400/day

---

## Key Benefits

### 🆓 Cost Savings
- **Before**: $0.001-$0.003 per query with OpenAI
- **After**: FREE with Groq's generous free tier

### ⚡ Performance
- **Streaming responses**: Real-time generation
- **Larger context**: 4096 max tokens vs 500
- **Optimized model**: Qwen3-32B specialized for coding tasks

### 🔧 API Differences
| Feature | OpenAI | Groq |
|---------|--------|------|
| API Key Prefix | `sk-proj-...` | `gsk_...` |
| Console URL | platform.openai.com | console.groq.com |
| Model | gpt-3.5-turbo | qwen/qwen3-32b |
| Streaming | Optional | Built-in |
| Free Tier | $5 credits | Unlimited (with rate limits) |
| Temperature Range | 0-2 | 0-2 |
| Max Tokens | Limited | 4096 |

---

## Setup Instructions

### For New Users:
1. Get free API key: https://console.groq.com/keys
2. Set environment variable:
   ```powershell
   $env:GROQ_API_KEY = "gsk_YOUR_KEY_HERE"
   ```
3. Restart Flask server
4. Test natural language queries

### For Existing OpenAI Users:
Your old pattern matching still works! Simply:
1. Get free Groq key (no credit card needed)
2. Replace `OPENAI_API_KEY` with `GROQ_API_KEY`
3. Restart server

---

## Technical Details

### Groq Streaming Implementation:
```python
completion = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[...],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=0.95,
    reasoning_effort="default",
    stream=True,
    stop=None
)

# Collect streaming response
content = ""
for chunk in completion:
    if chunk.choices[0].delta.content:
        content += chunk.choices[0].delta.content
```

### Parameters Explained:
- **temperature**: 0.6 - Balanced between deterministic and creative
- **max_completion_tokens**: 4096 - Large enough for complex queries
- **top_p**: 0.95 - Nucleus sampling for quality
- **reasoning_effort**: "default" - Standard reasoning depth
- **stream**: True - Real-time response generation

---

## Verification

To verify the migration worked:

1. **Check installed package**:
   ```powershell
   pip list | Select-String groq
   ```
   Should show: `groq 0.11.0`

2. **Test without API key**:
   - Should fall back to pattern matching
   - Response shows: `"method": "pattern"`

3. **Test with API key**:
   - Should use Groq LLM
   - Response shows: `"method": "llm"`
   - Higher confidence scores (95%)

---

## Troubleshooting

### Import Error: "No module named 'groq'"
```powershell
pip install groq==0.11.0
```

### Still using OpenAI
Check that:
- [ ] `config.py` imports `GROQ_API_KEY` (not `OPENAI_API_KEY`)
- [ ] `llm_query.py` imports `from groq import Groq`
- [ ] Flask server was restarted after changes

### Rate Limiting
Free tier limits:
- 30 requests per minute
- 14,400 requests per day
- Wait 60 seconds if rate limited

---

## Alternative Models

Groq supports multiple models. To switch, edit `llm_query.py`:

```python
# Fast and balanced (current)
model="qwen/qwen3-32b"

# Largest, most capable
model="llama-3.3-70b-versatile"

# Very fast
model="llama-3.1-8b-instant"

# Good for general tasks
model="mixtral-8x7b-32768"
```

---

## Rollback Instructions

If needed, to rollback to OpenAI:

1. **Install OpenAI**:
   ```powershell
   pip uninstall -y groq
   pip install openai==1.12.0
   ```

2. **Restore config.py**:
   ```python
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)
   ```

3. **Restore llm_query.py**:
   ```python
   from openai import OpenAI
   from config import OPENAI_API_KEY
   
   self.client = OpenAI(api_key=self.api_key)
   
   # In _convert_with_llm:
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[...],
       temperature=0.3,
       max_tokens=500
   )
   ```

---

## Status: ✅ Complete

All files updated, package installed, server running successfully with Groq integration.

**Next Steps**:
1. Get free Groq API key: https://console.groq.com/keys
2. Set `GROQ_API_KEY` environment variable
3. Test natural language queries
4. Enjoy FREE, fast LLM-powered queries!
