# Starlight Cloud Server

This is the cloud reasoning module for the Starlight Hybrid AI.

It exposes:
- `/health` — check status
- `/embed` — embeddings (USB Starlight calls this)
- `/reason` — reasoning + memory awareness

## Deploy on Hugging Face Spaces

1. Create a new Space  
2. Set Space type: **Container** or **FastAPI**  
3. Connect to this GitHub repository  
4. Add environment variable:

   ```
   OPENAI_API_KEY=sk-...
   ```

5. Done! Your USB Starlight can now call:
   ```
   https://YOUR_SPACE.hf.space/embed
   https://YOUR_SPACE.hf.space/reason
   ```

## Local Development

```bash
cd starlight_cloud
pip install -r requirements.txt
python server.py
```

Server runs on `http://localhost:7860`

Test with:
```bash
curl http://localhost:7860/health
```
