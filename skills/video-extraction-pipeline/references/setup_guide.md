# Video Extraction Pipeline Setup Guide

This guide provides detailed instructions for setting up and using the video extraction pipeline.

**Supports both local video files and YouTube URLs** - process videos from your computer or directly from YouTube.

## Prerequisites

- Python 3.11+
- `uv` package manager (or `pip`)
- Google Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)

## Installation Steps

### 1. Install Dependencies

```bash
uv pip install google-genai pyyaml python-dotenv
```

Or with pip:
```bash
pip install google-genai pyyaml python-dotenv
```

### 2. Set Up API Key

Create a `.env` file in your project directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Configuration

The pipeline is controlled by `config.yaml`. Key sections:

### Model Selection

```yaml
model: "gemini-2.5-pro"  # Best quality
# or
model: "gemini-2.5-flash"  # Faster, cheaper
```

### Rate Limiting

For free tier API keys, use 60-second delays:
```yaml
rate_limit_delay: 60  # seconds between videos
```

### Extraction Prompts

The `prompt_template` controls what content is extracted. Customize for your use case:

```yaml
prompt_template: |
  Extract all frameworks, tactics, and key insights from this video.

  Focus on:
  - Step-by-step processes
  - Actionable recommendations
  - Specific examples with metrics

  Format as structured markdown with clear sections.
```

### Output Format

The `output_format` defines the markdown structure:

```yaml
output_format: |
  Structure output with these sections:
  1. **Overview** - Main purpose
  2. **Key Frameworks** - Structured processes
  3. **Actionable Tactics** - Implementation steps
  4. **Examples** - Real examples with transcript quotes
  5. **Common Pitfalls** - Mistakes to avoid
  6. **Checklist** - Step-by-step application guide
```

### Video List

Define videos to process. You can use **local files** or **YouTube URLs**:

```yaml
videos:
  # Local video file
  - path: "../videos/lesson1.mp4"
    output: "../extracted/lesson1.md"
    title: "Lesson 1 - Introduction"
    section: "Part 1"
    filename: "lesson1.mp4"

  # YouTube video (no download needed!)
  - youtube_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output: "../extracted/youtube-lesson.md"
    title: "YouTube Lesson - Advanced Topics"
    section: "Part 2"
```

## Usage

### Process All Videos

```bash
python3 video_extractor.py
```

### Process Specific Videos

```bash
python3 video_extractor.py --videos video-id-1 video-id-2
```

### Custom Config

```bash
python3 video_extractor.py --config custom_config.yaml
```

## Customization Tips

### For Educational Content

Focus on:
- Learning objectives
- Key concepts
- Practice exercises
- Summary points

### For Training Videos

Focus on:
- Step-by-step procedures
- Tools and resources
- Common mistakes
- Troubleshooting tips

### For Marketing/Sales Content

Focus on:
- Frameworks and methodologies
- Tactics and strategies
- Templates and scripts
- Real-world examples

## Troubleshooting

### "GEMINI_API_KEY not found"
Set API key in `.env` file or export as environment variable

### "ragStoreName" Error
Update to latest `google-genai` library (not `google-generativeai`)

### Rate Limiting
Increase `rate_limit_delay` in config.yaml (60+ seconds for free tier)

### Empty Responses
Video may be too short or extraction failed - try different prompt

### YouTube Video Not Accessible
Only public YouTube videos work (not private/unlisted). Test in incognito mode.

### YouTube Daily Limit
Gemini has an 8-hour daily limit for YouTube videos per account

## Cost Estimates

Based on Gemini API pricing:
- **Per video**: $0.50-2.00 (depends on length/complexity)
- **Model choice**: Use `gemini-2.5-flash` for 40% cost reduction
- **Free tier**: Includes rate limits, use 60s delays

## Best Practices

1. **Test with pilot videos** - Process 2-3 videos first to validate quality
2. **Iterate on prompts** - Adjust extraction prompts based on output quality
3. **Use consistent naming** - Match output filenames to video structure
4. **Organize by folders** - Mirror video folder structure for easy navigation
5. **Version control** - Track prompt changes and output iterations
