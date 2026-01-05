---
name: video-extraction-pipeline
description: Build automated pipelines to extract structured content (frameworks, tactics, examples) from video courses using Google Gemini API. Creates reusable extraction systems with configurable prompts, batch processing, and markdown output. Use this skill when the user needs to convert video content into searchable, structured knowledge bases.
---

# Video Extraction Pipeline

Build automated pipelines to extract structured knowledge from video content using Google Gemini's multimodal capabilities. Convert educational videos, training courses, or instructional content into searchable, LLM-optimized markdown files with frameworks, actionable tactics, and key insights.

**Supports both local video files and YouTube URLs** - process videos from your computer or directly from YouTube without downloading.

## When to Use This Skill

Use this skill when:

- Converting video courses into structured markdown knowledge bases
- Extracting frameworks, methodologies, and tactics from instructional videos
- Building searchable documentation from video training materials
- Creating LLM-optimized summaries of educational content
- Setting up reusable extraction pipelines for ongoing video processing
- Processing YouTube videos or playlists without downloading them first

## Core Capabilities

This skill provides:

1. **Automated Video Processing** - Batch upload and extract content from multiple videos
2. **Highly Customizable Extraction** - Extensive prompt library for 10+ content types (sales, technical, educational, fitness, etc.)
3. **Smart Rate Limiting** - Handle free tier API constraints with configurable delays
4. **Structured Output** - Generate markdown with consistent sections for easy navigation
5. **Reusable Pipeline** - One-time setup, reuse for any video content with prompt adjustments

## Important: Customization Required

**This skill provides the infrastructure and templates, but requires prompt customization for your specific content.**

Different video types need different extraction approaches:
- **Educational videos** → Concepts, examples, practice problems
- **Sales training** → Frameworks, tactics, objection handling, scripts
- **Technical tutorials** → Commands, procedures, code examples, troubleshooting
- **Fitness content** → Exercises, form cues, programming, modifications

See `references/prompt_library.md` for 10+ pre-built templates covering common content types. Start with the closest template and customize for your specific needs.

## How to Use This Skill

### Step 1: Initialize the Pipeline

To set up a new video extraction pipeline in a user's project:

1. Use `scripts/init_video_pipeline.py` to bootstrap the project structure:

```bash
python3 scripts/init_video_pipeline.py /path/to/user/project
```

This creates:
- `scripts/` - Contains video_extractor.py and config.yaml
- `videos/` - Directory for video files
- `extracted/` - Output directory for markdown files
- `README.md` - Quick start guide

**Optional custom videos path:**
```bash
python3 scripts/init_video_pipeline.py /path/to/project --videos-path /path/to/existing/videos
```

### Step 2: Configure API Access

Guide the user to set up their Gemini API key:

1. **Get API key**: Direct user to [AI Studio](https://aistudio.google.com/app/apikey)
2. **Create .env file**:
   ```bash
   cd scripts
   cp .env.example .env
   ```
3. **Add API key**: Edit `.env` and set `GEMINI_API_KEY=their_key_here`

### Step 3: Install Dependencies

Install required Python packages using `uv` (preferred) or `pip`:

```bash
uv pip install google-genai pyyaml python-dotenv
```

**Important**: Use `google-genai` (not the deprecated `google-generativeai`)

### Step 4: Customize Extraction Configuration

Edit `scripts/config.yaml` to match the user's content:

#### Model Selection

Choose based on quality vs cost tradeoff:
- `gemini-2.5-pro` - Best quality extraction
- `gemini-2.5-flash` - 40% cheaper, slightly lower quality

#### Rate Limiting

For free tier API keys, set 60-second delays between videos:
```yaml
rate_limit_delay: 60  # Prevents rate limit errors
```

#### Extraction Prompts

**This is the most important customization step.** The quality of extraction depends entirely on prompt design.

**Start with a template from `references/prompt_library.md`:**

Available templates for:
- Educational & Academic (online courses, math/science)
- Business & Sales (methodologies, leadership)
- Technical Training (coding, DevOps, infrastructure)
- Creative & Production (video editing, design/UX)
- Health & Fitness (workout training, nutrition)
- Marketing & Content (strategy, copywriting)

**Customization process:**
1. Find the closest template to your content type
2. Copy to `config.yaml`
3. Adjust the "Focus on" section for your specific needs
4. Modify the output_format to match your desired structure
5. Test with 1-2 pilot videos
6. Iterate based on what's missing or needs improvement

See `references/prompt_library.md` for complete templates with examples.

#### Video List

Add videos to process with metadata. You can use **local video files** (with `path`) or **YouTube URLs** (with `youtube_url`):

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
    title: "YouTube Lesson - Advanced Tactics"
    section: "Part 2"
```

**Best Practices**:
- Use relative paths from `scripts/` directory for local files
- YouTube URLs must be public videos (not private/unlisted)
- Mix local and YouTube videos in the same config

### Step 5: Run Pilot Test

Before processing all videos, test with 2-3 pilot videos to validate extraction quality:

```bash
cd scripts
python3 video_extractor.py --videos pilot-1 pilot-2
```

Review the output markdown files and adjust prompts if needed.

### Step 6: Process All Videos

Once prompts are validated, process the full video set:

```bash
python3 video_extractor.py
```

The pipeline will:
1. Upload each video to Gemini Files API
2. Wait for video processing (automatic)
3. Extract content using custom prompts
4. Save structured markdown to output path
5. Wait `rate_limit_delay` seconds before next video

### Step 7: Organize Output

Recommend organizing extracted markdown files to mirror video folder structure:

```
project/
├── videos/
│   ├── part1/
│   │   ├── lesson1.mp4
│   │   └── lesson1.md  ← extracted content
│   └── part2/
│       ├── lesson2.mp4
│       └── lesson2.md
```

This keeps videos and extracted content paired together.

## Customization Guidance

### Prompt Engineering for Different Content Types

#### Technical Training
```yaml
prompt_template: |
  Extract technical procedures, commands, and troubleshooting steps.
  Include specific code examples and configuration details.
```

#### Business/Sales Training
```yaml
prompt_template: |
  Extract frameworks, methodologies, and actionable tactics.
  Include transcript quotes that capture nuance and specific examples.
```

#### Academic/Educational
```yaml
prompt_template: |
  Extract key concepts, learning objectives, and practice problems.
  Include definitions, formulas, and summary points.
```

### Output Structure Customization

Modify `output_format` to match desired markdown structure:

```yaml
output_format: |
  1. **Summary** - 2-3 sentence overview
  2. **Key Points** - Bulleted main takeaways
  3. **Step-by-Step Guide** - Numbered procedures
  4. **Resources** - Tools, links, references mentioned
  5. **Quiz Questions** - Generated from content
```

### Handling Large Video Sets

For 10+ videos:
- Set higher `rate_limit_delay` (60-120s for free tier)
- Process in batches using `--videos` flag
- Monitor for API quota limits
- Consider upgrading to paid tier for faster processing

## Troubleshooting Common Issues

### "ragStoreName" Error
**Cause**: User has old `google-generativeai` library installed
**Fix**: Uninstall old library and install new one:
```bash
uv pip uninstall google-generativeai
uv pip install google-genai
```

### Rate Limiting Errors
**Cause**: Free tier API limits exceeded
**Fix**: Increase `rate_limit_delay` to 60+ seconds in config.yaml

### Empty or Low-Quality Extractions
**Cause**: Prompts not tailored to content type
**Fix**: Review pilot output, adjust `prompt_template` to be more specific

### Video Processing Timeout
**Cause**: Very large video files (>500MB)
**Fix**: Split large videos into smaller segments or use shorter clips for testing

### YouTube Video Not Accessible
**Cause**: Video is private, unlisted, or age-restricted
**Fix**: Only public YouTube videos are supported. Check video accessibility in incognito mode

### YouTube Daily Limit Exceeded
**Cause**: Gemini API has an 8-hour daily limit for YouTube video processing per account
**Fix**: Wait 24 hours or use local video files instead for large batches

## Technical Details

### File Size Limits
- **Max per file**: 2GB (Gemini API limit)
- **Storage quota**: 20GB per project
- **File retention**: 48 hours (automatic cleanup)

### Supported Video Formats
MP4, MOV, AVI, WEBM, MPG, MPEG, FLV, WMV, 3GPP

### Token/Cost Estimates
- **Per video**: ~$0.50-2.00 (varies by length)
- **Model choice**: Flash is 40% cheaper than Pro
- **Context window**: 1-2M tokens (handles very long videos)

## Example Workflows

### Workflow 1: Educational Course Extraction

```bash
# Initialize pipeline
python3 scripts/init_video_pipeline.py ~/courses/python101

# Configure for educational content
cd ~/courses/python101/scripts
# Edit config.yaml to focus on concepts, examples, exercises

# Test with one lesson
python3 video_extractor.py --videos lesson1

# Process full course
python3 video_extractor.py
```

### Workflow 2: Sales Training Pipeline

```bash
# Initialize with existing video directory
python3 scripts/init_video_pipeline.py ~/sales-training \
  --videos-path ~/sales-training/recorded-sessions

# Configure for sales frameworks
cd ~/sales-training/scripts
# Edit config.yaml to extract tactics, objection handling, scripts

# Run extraction
python3 video_extractor.py
```

### Workflow 3: YouTube Course Extraction

```bash
# Initialize pipeline
python3 scripts/init_video_pipeline.py ~/youtube-course

# Configure for YouTube videos
cd ~/youtube-course/scripts
# Edit config.yaml and add YouTube URLs:
# videos:
#   - youtube_url: "https://youtube.com/watch?v=abc123"
#     output: "../extracted/lesson1.md"
#     title: "Lesson 1"

# Process YouTube videos (no download needed!)
python3 video_extractor.py
```

## References

- **Prompt Library**: See `references/prompt_library.md` for 10+ pre-built extraction templates (START HERE for customization)
- **Setup Guide**: See `references/setup_guide.md` for detailed installation and configuration
- **Config Template**: See `references/config_template.yaml` for complete configuration example
- **Core Script**: `scripts/video_extractor.py` - Main processing engine
- **Init Script**: `scripts/init_video_pipeline.py` - Project bootstrapper

## Key Reference: Prompt Library

The `references/prompt_library.md` file contains ready-to-use templates for:

1. **Educational & Academic**: Online courses, lectures, math/science tutorials
2. **Business & Sales**: Sales methodologies, frameworks, leadership training
3. **Technical Training**: Software development, DevOps, infrastructure
4. **Creative & Production**: Video editing, design, UX workflows
5. **Health & Fitness**: Workout programming, exercise technique
6. **Marketing & Content**: Marketing strategy, campaign tactics

Each template includes:
- Customized `prompt_template` for that content type
- Matching `output_format` structure
- Specific guidance on what to extract
- Examples of the expected output format

**Always start by reviewing the prompt library before configuring your pipeline.**

## Best Practices

1. **Start with pilot videos** - Always test on 2-3 videos before full batch
2. **Iterate on prompts** - Review output quality and refine extraction prompts
3. **Use consistent naming** - Match output filenames to video names for easy navigation
4. **Mirror folder structure** - Keep extracted markdown alongside videos
5. **Version control prompts** - Track prompt changes to understand quality improvements
6. **Respect rate limits** - Use 60s delays for free tier to avoid throttling
7. **Monitor costs** - Track API usage, consider Flash model for large batches

## Success Criteria

A successful pipeline setup delivers:
- ✅ Structured markdown with consistent sections (frameworks, tactics, examples)
- ✅ Transcript snippets that capture nuance and context
- ✅ Actionable checklists and implementation steps
- ✅ No API rate limit errors during processing
- ✅ Output organized in logical folder structure
- ✅ Reusable configuration for future video batches
