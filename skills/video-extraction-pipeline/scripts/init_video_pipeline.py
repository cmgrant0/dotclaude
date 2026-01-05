#!/usr/bin/env python3
"""
Initialize a new video extraction pipeline in a project directory.
Creates the necessary directory structure and config files.
"""

import argparse
import sys
from pathlib import Path
import shutil


def init_pipeline(project_path: Path, videos_path: Path = None):
    """Initialize video extraction pipeline in project directory."""

    # Create project directory if it doesn't exist
    project_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    scripts_dir = project_path / "scripts"
    videos_dir = videos_path or (project_path / "videos")
    output_dir = project_path / "extracted"

    scripts_dir.mkdir(exist_ok=True)
    videos_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    print(f"✓ Created directory structure:")
    print(f"  - {scripts_dir}")
    print(f"  - {videos_dir}")
    print(f"  - {output_dir}")

    # Copy core files (these should be in the same directory as this script)
    skill_dir = Path(__file__).parent.parent

    # Copy video_extractor.py
    src_extractor = skill_dir / "scripts" / "video_extractor.py"
    dst_extractor = scripts_dir / "video_extractor.py"
    if src_extractor.exists():
        shutil.copy2(src_extractor, dst_extractor)
        print(f"✓ Copied video_extractor.py to {dst_extractor}")

    # Copy config template
    src_config = skill_dir / "references" / "config_template.yaml"
    dst_config = scripts_dir / "config.yaml"
    if src_config.exists():
        shutil.copy2(src_config, dst_config)
        print(f"✓ Copied config.yaml to {dst_config}")

    # Copy .env.example
    src_env = skill_dir / "assets" / ".env.example"
    dst_env = scripts_dir / ".env.example"
    if src_env.exists():
        shutil.copy2(src_env, dst_env)
        print(f"✓ Copied .env.example to {dst_env}")

    # Create README
    readme_content = f"""# Video Extraction Pipeline

Extract structured content from videos using Google Gemini API.
**Supports both local video files and YouTube URLs!**

## Quick Start

1. **Install dependencies:**
   ```bash
   uv pip install google-genai pyyaml python-dotenv
   ```

2. **Set up API key:**
   ```bash
   cd scripts
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Configure videos:**
   Edit `scripts/config.yaml` and add your video paths or YouTube URLs

4. **Run extraction:**
   ```bash
   cd scripts
   python3 video_extractor.py
   ```

## Directory Structure

```
.
├── scripts/
│   ├── video_extractor.py  # Main extraction script
│   ├── config.yaml         # Pipeline configuration
│   └── .env               # API key (create from .env.example)
├── videos/                 # Place your video files here
└── extracted/             # Extracted markdown outputs
```

## Configuration

Edit `scripts/config.yaml` to:
- Set model (gemini-2.5-pro or gemini-2.5-flash)
- Adjust rate limiting for free tier (60s delay recommended)
- Customize extraction prompts
- Define video list with local paths OR YouTube URLs
  - Local files: use `path` field
  - YouTube videos: use `youtube_url` field (no download needed!)
  - Mix both types in the same config

## Usage

Process all videos:
```bash
cd scripts
python3 video_extractor.py
```

Process specific videos:
```bash
python3 video_extractor.py --videos video-id-1 video-id-2
```

Custom config:
```bash
python3 video_extractor.py --config custom_config.yaml
```

## Next Steps

1. Update `scripts/config.yaml` with your video list:
   - For local files: Place videos in `videos/` directory and use `path` field
   - For YouTube: Add URLs with `youtube_url` field (public videos only)
2. Customize extraction prompts for your content type
3. Run pilot test on 2-3 videos to validate quality
4. Process remaining videos after prompt tuning

**YouTube Limitations:**
- Only public videos supported (not private/unlisted)
- 8-hour daily limit per Gemini API account

For detailed setup and customization, see the skill documentation.
"""

    readme_path = project_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"✓ Created README.md at {readme_path}")

    print(f"\n{'='*70}")
    print(f"✓ Video extraction pipeline initialized at: {project_path}")
    print(f"{'='*70}")
    print(f"\nNext steps:")
    print(f"1. cd {scripts_dir}")
    print(f"2. cp .env.example .env && edit .env with your GEMINI_API_KEY")
    print(f"3. Edit config.yaml to add your video list")
    print(f"4. python3 video_extractor.py")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a video extraction pipeline"
    )
    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to project directory"
    )
    parser.add_argument(
        "--videos-path",
        type=Path,
        help="Custom path for videos directory (default: <project_path>/videos)"
    )

    args = parser.parse_args()

    try:
        init_pipeline(args.project_path, args.videos_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
