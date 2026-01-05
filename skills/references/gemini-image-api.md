# Gemini Image Generation API Reference

Comprehensive reference for generating images with Google's Gemini API using Python.

## Setup & Authentication

### Installation

```bash
# Using uv (recommended)
uv pip install google-genai

# Using pip
pip install google-genai
```

### Environment Variable

Set the API key before running:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get an API key from: https://aistudio.google.com/apikey

### Client Initialization

```python
import os
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
```

---

## Basic Image Generation

### Minimal Example

```python
import os
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents='A golden retriever playing in autumn leaves',
    config={
        'response_modalities': ['Text', 'Image']
    }
)

# Extract and save the image
# IMPORTANT: inline_data.data is already raw bytes, NOT base64-encoded
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        # Write bytes directly - do NOT use base64.b64decode()
        with open('generated_image.jpg', 'wb') as f:
            f.write(part.inline_data.data)
        print('Image saved to generated_image.jpg')
```

---

## Configuration Options

### Aspect Ratios

| Ratio | Description |
|-------|-------------|
| `1:1` | Square (default) |
| `16:9` | Landscape / Widescreen |
| `9:16` | Portrait / Mobile |
| `4:3` | Standard |
| `3:4` | Portrait Standard |
| `3:2` | Photo |
| `2:3` | Portrait Photo |
| `4:5` | Instagram |
| `5:4` | Large Format |
| `21:9` | Ultrawide |

### Image Sizes

| Size | Description |
|------|-------------|
| `1K` | Fast generation, lower resolution |
| `2K` | Balanced quality and speed (recommended) |
| `4K` | High quality, slower generation |

### Full Configuration Example

```python
response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents='A futuristic cityscape at night',
    config={
        'response_modalities': ['Text', 'Image'],
    }
)
```

> **Note**: The `imageConfig` options (`aspectRatio`, `imageSize`) may not be supported in the current API version. Test before relying on them.

---

## Style Presets

Apply style modifiers by appending them to the prompt:

```python
def apply_style(prompt: str, style: str) -> str:
    """Append style modifier to prompt."""
    style_modifiers = {
        'photorealistic': 'photorealistic, highly detailed, professional photography',
        'illustration': 'digital illustration, artistic, stylized',
        'anime': 'anime style, Japanese animation aesthetic',
        'painting': 'oil painting style, painterly, artistic brushstrokes',
        '3d': '3D render, CGI, realistic lighting and materials',
        'sketch': 'pencil sketch, hand-drawn, artistic linework',
        'watercolor': 'watercolor painting, soft colors, artistic',
        'vintage': 'vintage photography style, retro aesthetic, film grain',
    }

    modifier = style_modifiers.get(style)
    if modifier:
        return f"{prompt}, {modifier}"
    return prompt


# Usage
prompt = apply_style("A cat sitting on a windowsill", "watercolor")
# Result: "A cat sitting on a windowsill, watercolor painting, soft colors, artistic"
```

---

## Reference Images

Use reference images to provide visual context for generation.

### From Local File

```python
import base64
import os
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def load_image_as_base64(file_path: str) -> tuple[str, str]:
    """Load image file and return (base64_data, mime_type)."""
    import mimetypes

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'image/jpeg'  # Default fallback

    with open(file_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    return image_data, mime_type


# Load reference image
image_data, mime_type = load_image_as_base64('my_photo.jpg')

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=[
        {'text': 'Create a similar scene but during winter with snow'},
        {'inline_data': {'data': image_data, 'mime_type': mime_type}}
    ],
    config={
        'response_modalities': ['Text', 'Image'],
    }
)
```

### From URL

```python
import base64
import requests
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def load_image_from_url(url: str) -> tuple[str, str]:
    """Fetch image from URL and return (base64_data, mime_type)."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Get mime type from response headers or default
    mime_type = response.headers.get('content-type', 'image/jpeg')
    if ';' in mime_type:
        mime_type = mime_type.split(';')[0]

    image_data = base64.b64encode(response.content).decode('utf-8')
    return image_data, mime_type


# Fetch and use reference image from URL
image_data, mime_type = load_image_from_url('https://example.com/photo.jpg')

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=[
        {'text': 'Create an image inspired by this but with a sunset background'},
        {'inline_data': {'data': image_data, 'mime_type': mime_type}}
    ],
    config={
        'response_modalities': ['Text', 'Image'],
    }
)
```

### Multiple Reference Images

```python
# Load multiple reference images
contents = [{'text': 'Combine the style of the first image with the subject of the second'}]

for file_path in ['style_reference.jpg', 'subject_reference.jpg']:
    image_data, mime_type = load_image_as_base64(file_path)
    contents.append({
        'inline_data': {'data': image_data, 'mime_type': mime_type}
    })

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=contents,
    config={
        'response_modalities': ['Text', 'Image'],
    }
)
```

---

## Response Handling

> **CRITICAL**: `inline_data.data` is already **raw bytes**, NOT base64-encoded.
> Do NOT call `base64.b64decode()` on it - this will corrupt your images!

### Extracting Images

```python
def extract_images(response) -> list[bytes]:
    """Extract all generated images from response as bytes."""
    images = []

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                # Data is already bytes - use directly
                images.append(part.inline_data.data)

    return images


def extract_text(response) -> str:
    """Extract text response if present."""
    text_parts = []

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                text_parts.append(part.text)

    return '\n'.join(text_parts)
```

### Saving to File

```python
def get_extension_from_mime(mime_type: str) -> str:
    """Get file extension from mime type. Defaults to .jpg if unknown."""
    if not mime_type:
        return '.jpg'
    mime_type = mime_type.lower()
    if 'jpeg' in mime_type or 'jpg' in mime_type:
        return '.jpg'
    elif 'png' in mime_type:
        return '.png'
    elif 'webp' in mime_type:
        return '.webp'
    elif 'gif' in mime_type:
        return '.gif'
    return '.jpg'  # Default fallback


def save_images(response, output_dir: str = '.', prefix: str = 'image') -> list[str]:
    """Save all generated images to files with correct extensions. Returns list of saved file paths."""
    import os

    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []

    if response.candidates and response.candidates[0].content.parts:
        for i, part in enumerate(response.candidates[0].content.parts):
            if hasattr(part, 'inline_data') and part.inline_data:
                # Auto-detect format from mime_type
                mime_type = getattr(part.inline_data, 'mime_type', 'image/jpeg')
                ext = get_extension_from_mime(mime_type)
                file_path = os.path.join(output_dir, f'{prefix}_{i}{ext}')
                with open(file_path, 'wb') as f:
                    f.write(part.inline_data.data)
                saved_paths.append(file_path)
                print(f'Saved: {file_path}')

    return saved_paths
```

### Copy to Clipboard (Bonus)

Requires `pyperclip` package:

```bash
uv pip install pyperclip
```

```python
import pyperclip
import base64

def copy_image_to_clipboard_as_base64(response):
    """Copy first generated image as base64 string to clipboard."""
    images = extract_images(response)
    if images:
        base64_str = base64.b64encode(images[0]).decode('utf-8')
        pyperclip.copy(base64_str)
        print('Image copied to clipboard as base64')
```

---

## Error Handling

### Retry Logic for Overloaded Model

```python
import time

def generate_with_retry(client, prompt: str, config: dict, max_retries: int = 3):
    """Generate image with automatic retry for overloaded model."""
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-3-pro-image-preview',
                contents=prompt,
                config=config
            )
            return response
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()

            is_overloaded = (
                '503' in error_msg or
                'overloaded' in error_msg or
                'unavailable' in error_msg
            )

            if is_overloaded and attempt < max_retries:
                wait_time = 2 ** attempt  # 2s, 4s, 8s
                print(f'Model overloaded, retrying in {wait_time}s (attempt {attempt}/{max_retries})')
                time.sleep(wait_time)
                continue

            raise

    raise last_error
```

### Error Types

| Error | Detection | Recommended Action |
|-------|-----------|-------------------|
| Safety filter | `'SAFETY'` in error | Modify prompt to be less sensitive |
| Rate limit | `'quota'` or `'rate'` in error | Wait and retry later |
| Model overloaded | `'503'`, `'overloaded'`, `'UNAVAILABLE'` | Retry with exponential backoff |
| No images generated | Empty response parts | Try different prompt |

### Comprehensive Error Handler

```python
def handle_generation_error(error: Exception) -> str:
    """Return user-friendly error message."""
    error_msg = str(error).lower()

    if 'safety' in error_msg:
        return 'Prompt blocked for safety reasons. Try a different prompt.'
    elif 'quota' in error_msg or 'rate' in error_msg:
        return 'Rate limit reached. Wait a moment and try again.'
    elif '503' in error_msg or 'overloaded' in error_msg or 'unavailable' in error_msg:
        return 'Model is overloaded. Try again in a few minutes.'
    else:
        return f'Generation failed: {error}'
```

---

## Complete Examples

### Example 1: Basic Generation with File Save

```python
#!/usr/bin/env python3
"""Generate an image and save to file."""
import os
from google import genai

def main():
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    prompt = "A cozy coffee shop interior with warm lighting, photorealistic, highly detailed"

    response = client.models.generate_content(
        model='gemini-3-pro-image-preview',
        contents=prompt,
        config={
            'response_modalities': ['Text', 'Image'],
        }
    )

    # Save images - data is already bytes, write directly
    # Auto-detect format from mime_type to use correct extension
    for i, part in enumerate(response.candidates[0].content.parts):
        if hasattr(part, 'inline_data') and part.inline_data:
            mime = getattr(part.inline_data, 'mime_type', 'image/jpeg')
            ext = '.png' if 'png' in mime else '.webp' if 'webp' in mime else '.jpg'
            filename = f'coffee_shop_{i}{ext}'
            with open(filename, 'wb') as f:
                f.write(part.inline_data.data)
            print(f'Saved: {filename}')

if __name__ == '__main__':
    main()
```

### Example 2: Reference Image from File

```python
#!/usr/bin/env python3
"""Generate image using a local file as reference."""
import os
import base64
from google import genai

def main():
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    # Load reference image - INPUT images need base64 encoding
    with open('my_pet.jpg', 'rb') as f:
        ref_image = base64.b64encode(f.read()).decode('utf-8')

    response = client.models.generate_content(
        model='gemini-3-pro-image-preview',
        contents=[
            {'text': 'Draw this pet as a superhero, anime style, Japanese animation aesthetic'},
            {'inline_data': {'data': ref_image, 'mime_type': 'image/jpeg'}}
        ],
        config={
            'response_modalities': ['Text', 'Image'],
        }
    )

    # Save result - OUTPUT data is already bytes, write directly
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open('pet_superhero.jpg', 'wb') as f:
                f.write(part.inline_data.data)
            print('Saved: pet_superhero.jpg')

if __name__ == '__main__':
    main()
```

### Example 3: Reference Image from URL

```python
#!/usr/bin/env python3
"""Generate image using a URL as reference."""
import os
import base64
import requests
from google import genai

def main():
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    # Fetch reference image from URL - INPUT needs base64 encoding
    url = 'https://example.com/landscape.jpg'
    response = requests.get(url, timeout=30)
    ref_image = base64.b64encode(response.content).decode('utf-8')

    api_response = client.models.generate_content(
        model='gemini-3-pro-image-preview',
        contents=[
            {'text': 'Recreate this scene during a thunderstorm with dramatic lighting'},
            {'inline_data': {'data': ref_image, 'mime_type': 'image/jpeg'}}
        ],
        config={
            'response_modalities': ['Text', 'Image'],
        }
    )

    # Save result - OUTPUT is already bytes
    for part in api_response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open('thunderstorm_scene.jpg', 'wb') as f:
                f.write(part.inline_data.data)
            print('Saved: thunderstorm_scene.jpg')

if __name__ == '__main__':
    main()
```

### Example 4: Full-Featured Generation Function

```python
#!/usr/bin/env python3
"""Full-featured image generation with all options."""
import os
import base64
import time
import requests
from pathlib import Path
from google import genai

def generate_image(
    prompt: str,
    output_path: str = 'generated.jpg',
    style: str | None = None,
    reference_images: list[str] | None = None,
    max_retries: int = 3
) -> str:
    """
    Generate an image and save to file.

    Args:
        prompt: Text description of the image
        output_path: Where to save the generated image
        style: Style preset (photorealistic, anime, etc.)
        reference_images: List of file paths or URLs for reference
        max_retries: Number of retry attempts for overloaded model

    Returns:
        Path to the saved image file
    """
    client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

    # Apply style modifier
    style_modifiers = {
        'photorealistic': 'photorealistic, highly detailed, professional photography',
        'illustration': 'digital illustration, artistic, stylized',
        'anime': 'anime style, Japanese animation aesthetic',
        'painting': 'oil painting style, painterly, artistic brushstrokes',
        '3d': '3D render, CGI, realistic lighting and materials',
        'sketch': 'pencil sketch, hand-drawn, artistic linework',
        'watercolor': 'watercolor painting, soft colors, artistic',
        'vintage': 'vintage photography style, retro aesthetic, film grain',
    }

    final_prompt = prompt
    if style and style in style_modifiers:
        final_prompt = f"{prompt}, {style_modifiers[style]}"

    # Build contents
    # Note: INPUT reference images need base64 encoding
    if reference_images:
        contents = [{'text': final_prompt}]

        for ref in reference_images:
            if ref.startswith(('http://', 'https://')):
                # URL reference
                resp = requests.get(ref, timeout=30)
                image_data = base64.b64encode(resp.content).decode('utf-8')
                mime_type = resp.headers.get('content-type', 'image/jpeg').split(';')[0]
            else:
                # File reference
                with open(ref, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                import mimetypes
                mime_type, _ = mimetypes.guess_type(ref)
                mime_type = mime_type or 'image/jpeg'

            contents.append({'inline_data': {'data': image_data, 'mime_type': mime_type}})
    else:
        contents = final_prompt

    # Generate with retry
    config = {
        'response_modalities': ['Text', 'Image'],
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-3-pro-image-preview',
                contents=contents,
                config=config
            )
            break
        except Exception as e:
            error_msg = str(e).lower()
            is_overloaded = '503' in error_msg or 'overloaded' in error_msg

            if is_overloaded and attempt < max_retries:
                wait_time = 2 ** attempt
                print(f'Retrying in {wait_time}s...')
                time.sleep(wait_time)
                continue
            raise

    # Save image - OUTPUT data is already bytes, write directly
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open(output_path, 'wb') as f:
                f.write(part.inline_data.data)  # Already bytes!
            print(f'Saved: {output_path}')
            return output_path

    raise RuntimeError('No image generated')


# Usage examples:
if __name__ == '__main__':
    # Basic generation
    generate_image(
        prompt='A majestic mountain peak at sunrise',
        output_path='mountain.jpg',
        style='photorealistic'
    )

    # With reference image from file
    generate_image(
        prompt='Create a winter version of this scene',
        output_path='winter_scene.jpg',
        reference_images=['original_photo.jpg'],
        style='painting'
    )

    # With reference image from URL
    generate_image(
        prompt='Draw this in anime style',
        output_path='anime_version.jpg',
        reference_images=['https://example.com/photo.jpg'],
        style='anime'
    )
```

---

## Best Practices

1. **Prompt Engineering**: Be specific and descriptive. Include details about lighting, mood, composition.

2. **Style Modifiers**: Apply styles by appending modifiers rather than prepending, for best results.

3. **Reference Images**: Resize large images before sending to reduce latency and API payload size.

4. **Error Handling**: Always implement retry logic for production use.

5. **Rate Limiting**: Respect API quotas. Implement delays between requests if generating many images.

6. **File Naming**: Use descriptive filenames or timestamps to avoid overwriting previous generations.
