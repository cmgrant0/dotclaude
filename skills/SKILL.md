---
name: gemini-image-gen
description: Generate images using Google's Gemini API. This skill should be used when the user asks to create, generate, or make images programmatically. Supports text-to-image generation with style presets, aspect ratios, and reference images for visual context. Triggers on requests like "generate an image of...", "create a picture of...", or "make me an image...".
---

# Gemini Image Generation

Generate images using Google's Gemini API (`gemini-3-pro-image-preview` model).

## Prerequisites

1. **API Key**: Set `GEMINI_API_KEY` environment variable
   - Get a key from https://aistudio.google.com/apikey
2. **Python Package**: Install with `uv pip install google-genai` or `pip install google-genai`

## Quick Start Workflow

1. **Initialize client** with API key from environment
2. **Build prompt** with optional style modifier appended
3. **Add reference images** (optional) as multimodal input
4. **Call API** with model `gemini-3-pro-image-preview`
5. **Extract and save** images from response

## Basic Generation Pattern

```python
import os
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents='A serene mountain landscape at sunset',
    config={
        'response_modalities': ['Text', 'Image'],
    }
)

# Save generated image
# NOTE: inline_data.data is already raw bytes, NOT base64-encoded
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        # Auto-detect format from mime_type (e.g., 'image/jpeg' -> '.jpg')
        mime_type = getattr(part.inline_data, 'mime_type', 'image/jpeg')
        ext = '.jpg' if 'jpeg' in mime_type else '.png' if 'png' in mime_type else '.webp' if 'webp' in mime_type else '.jpg'
        # Data is already bytes - write directly (do NOT base64.b64decode!)
        with open(f'output{ext}', 'wb') as f:
            f.write(part.inline_data.data)
```

## Style Presets

Append these modifiers to prompts for specific styles:

| Style | Append to Prompt |
|-------|-----------------|
| photorealistic | `, photorealistic, highly detailed, professional photography` |
| illustration | `, digital illustration, artistic, stylized` |
| anime | `, anime style, Japanese animation aesthetic` |
| painting | `, oil painting style, painterly, artistic brushstrokes` |
| 3d | `, 3D render, CGI, realistic lighting and materials` |
| sketch | `, pencil sketch, hand-drawn, artistic linework` |
| watercolor | `, watercolor painting, soft colors, artistic` |
| vintage | `, vintage photography style, retro aesthetic, film grain` |

## Adding Reference Images

To use reference images for visual context, pass multimodal contents:

```python
import base64

# Load reference image
with open('reference.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=[
        {'text': 'Create a similar landscape but at night'},
        {'inline_data': {'data': image_data, 'mime_type': 'image/jpeg'}}
    ],
    config={
        'responseModalities': ['TEXT', 'IMAGE'],
        'imageConfig': {'aspectRatio': '16:9', 'imageSize': '2K'}
    }
)
```

## Configuration Options

**Aspect Ratios**: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9`

**Image Sizes**: `1K` (fast), `2K` (balanced), `4K` (high quality)

## Error Handling

Implement retry logic for overloaded model (503 errors):

```python
import time

for attempt in range(3):
    try:
        response = client.models.generate_content(...)
        break
    except Exception as e:
        if '503' in str(e) or 'overloaded' in str(e):
            time.sleep(2 ** (attempt + 1))  # 2s, 4s, 8s backoff
            continue
        raise
```

## References

For comprehensive documentation including:
- Complete code examples with file and URL reference images
- Response handling patterns
- All error types and handling strategies
- Clipboard copy support

See `references/gemini-image-api.md`
