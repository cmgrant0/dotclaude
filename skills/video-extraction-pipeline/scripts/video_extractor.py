#!/usr/bin/env python3
"""
Video Content Extractor
Uses Google Gemini API to extract structured frameworks and actionable content from course videos.

Supports both local video files and YouTube URLs.
This is a reusable pipeline that can be configured via config.yaml for any video content extraction.
"""

import os
import sys
import time
import yaml
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from google import genai
from google.genai import types


class VideoExtractor:
    """Main class for extracting content from videos using Gemini API."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the video extractor with configuration."""
        self.config = self._load_config(config_path)
        self._setup_gemini()
        self.uploaded_files = {}  # Cache of uploaded file URIs

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        config_file = Path(__file__).parent / config_path
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def _setup_gemini(self):
        """Configure Gemini API with API key."""
        api_key = os.getenv('GEMINI_API_KEY') or self.config.get('api_key')
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it as environment variable or in config.yaml"
            )

        # Initialize client with the new API
        self.client = genai.Client(api_key=api_key)

        # Store model name for later use
        self.model_name = self.config.get('model', 'gemini-1.5-pro')
        print(f"✓ Using model: {self.model_name}")

    @staticmethod
    def _is_youtube_url(url: str) -> bool:
        """Check if the given string is a YouTube URL."""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
        ]
        return any(re.match(pattern, url) for pattern in youtube_patterns)

    def create_youtube_video_object(self, youtube_url: str, display_name: Optional[str] = None):
        """
        Create a video object for YouTube URL (no upload needed).
        Gemini API can process YouTube URLs directly.
        Returns a simple object with the YouTube URL.
        """
        # Check if already cached
        if youtube_url in self.uploaded_files:
            print(f"  Using cached YouTube URL: {youtube_url}")
            return self.uploaded_files[youtube_url]

        print(f"  Using YouTube URL: {youtube_url}")

        # Create a simple object to hold YouTube video info
        # Gemini processes YouTube URLs directly without uploading
        class YouTubeVideo:
            def __init__(self, url: str, display_name: str = None):
                self.uri = url
                self.mime_type = 'video/mp4'  # Standard for YouTube
                self.name = display_name or url
                self.is_youtube = True

        video_obj = YouTubeVideo(youtube_url, display_name)

        print(f"  ✓ YouTube video ready")

        # Cache the video object
        self.uploaded_files[youtube_url] = video_obj
        return video_obj

    def upload_video(self, video_path: str, display_name: Optional[str] = None) -> str:
        """
        Upload video to Gemini Files API.
        Returns the file object that can be reused for 48 hours.
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Check if already uploaded
        if video_path in self.uploaded_files:
            print(f"  Using cached upload for: {video_file.name}")
            return self.uploaded_files[video_path]

        # Upload file
        print(f"  Uploading: {video_file.name} ({self._format_size(video_file.stat().st_size)})")

        display_name = display_name or video_file.stem

        # Use new API: client.files.upload()
        with open(video_file, 'rb') as f:
            video_file_obj = self.client.files.upload(
                file=f,
                config={
                    'display_name': display_name,
                    'mime_type': 'video/mp4'
                }
            )

        print(f"  Upload complete. Processing video...")

        # Wait for processing to complete
        while video_file_obj.state == types.FileState.PROCESSING:
            print("  .", end="", flush=True)
            time.sleep(2)
            video_file_obj = self.client.files.get(name=video_file_obj.name)

        print()  # New line after dots

        if video_file_obj.state == types.FileState.FAILED:
            raise Exception(f"Video processing failed: {video_file_obj.state}")

        print(f"  ✓ Video ready: {video_file_obj.name}")

        # Cache the file object
        self.uploaded_files[video_path] = video_file_obj
        return video_file_obj

    def extract_content(self, video_file_obj, video_metadata: Dict) -> str:
        """
        Extract structured content from video using Gemini.
        Returns markdown-formatted content.
        """
        prompt = self._build_extraction_prompt(video_metadata)

        print(f"  Extracting content with Gemini...")

        try:
            # Use new API: client.models.generate_content()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_uri(
                        file_uri=video_file_obj.uri,
                        mime_type=video_file_obj.mime_type
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category='HARM_CATEGORY_HATE_SPEECH',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_HARASSMENT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_DANGEROUS_CONTENT',
                            threshold='BLOCK_NONE'
                        ),
                    ]
                )
            )

            if not response.text:
                raise Exception("Empty response from Gemini")

            print(f"  ✓ Content extracted ({len(response.text)} chars)")
            return response.text

        except Exception as e:
            print(f"  ✗ Extraction failed: {e}")
            raise

    def _build_extraction_prompt(self, video_metadata: Dict) -> str:
        """Build the extraction prompt based on video metadata and config."""
        template = self.config.get('prompt_template', '')

        # Replace placeholders in template
        prompt = template.format(
            title=video_metadata.get('title', 'Unknown'),
            section=video_metadata.get('section', 'Unknown'),
            course_context=self.config.get('course_context', ''),
            output_format=self.config.get('output_format', '')
        )

        return prompt

    def save_markdown(self, content: str, output_path: str, video_metadata: Dict):
        """Save extracted content as markdown file with metadata header."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Add metadata header
        header = self._generate_metadata_header(video_metadata)
        full_content = f"{header}\n\n{content}"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"  ✓ Saved to: {output_file}")

    def _generate_metadata_header(self, video_metadata: Dict) -> str:
        """Generate YAML frontmatter for markdown file."""
        # Determine if it's a YouTube video or local file
        source_info = video_metadata.get('youtube_url') or video_metadata.get('filename', 'Unknown')
        source_label = "YouTube URL" if video_metadata.get('youtube_url') else "Video File"

        header = f"""# {video_metadata.get('title', 'Untitled')}

**Section:** {video_metadata.get('section', 'Unknown Section')}
**Extracted:** {datetime.now().strftime('%Y-%m-%d')}
**{source_label}:** {source_info}

---
"""
        return header

    def process_video(self, video_config: Dict) -> bool:
        """
        Process a single video: upload/prepare, extract, save.
        Supports both local files (path) and YouTube URLs (youtube_url).
        Returns True if successful, False otherwise.
        """
        # Determine if it's a YouTube URL or local file
        youtube_url = video_config.get('youtube_url')
        video_path = video_config.get('path')
        output_path = video_config['output']

        # Validate that we have either youtube_url or path
        if not youtube_url and not video_path:
            raise ValueError("Video config must specify either 'youtube_url' or 'path'")

        video_source = youtube_url or video_path
        video_title = video_config.get('title', video_source)

        print(f"\n{'='*70}")
        print(f"Processing: {video_title}")
        print(f"{'='*70}")

        try:
            # Handle YouTube URL or local file
            if youtube_url:
                video_file_obj = self.create_youtube_video_object(
                    youtube_url,
                    display_name=video_config.get('title')
                )
            else:
                video_file_obj = self.upload_video(
                    video_path,
                    display_name=video_config.get('title')
                )

            # Extract content
            content = self.extract_content(video_file_obj, video_config)

            # Save markdown
            self.save_markdown(content, output_path, video_config)

            print(f"✓ Successfully processed: {video_title}")
            return True

        except Exception as e:
            print(f"✗ Failed to process {video_source}: {e}")
            return False

    def process_batch(self, video_list: Optional[List[str]] = None) -> Dict:
        """
        Process multiple videos from config.
        If video_list provided, only process those videos.
        Returns summary statistics.
        """
        videos = self.config.get('videos', [])

        if video_list:
            # Filter to only requested videos (by path, youtube_url, or id)
            videos = [v for v in videos if
                     v.get('path') in video_list or
                     v.get('youtube_url') in video_list or
                     v.get('id') in video_list]

        if not videos:
            print("No videos to process.")
            return {'total': 0, 'success': 0, 'failed': 0}

        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING: {len(videos)} videos")
        print(f"{'='*70}")

        results = {'total': len(videos), 'success': 0, 'failed': 0, 'errors': []}

        for i, video_config in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}]", end=" ")

            success = self.process_video(video_config)

            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                video_source = video_config.get('youtube_url') or video_config.get('path')
                results['errors'].append({
                    'video': video_config.get('title', video_source),
                    'source': video_source
                })

            # Respect rate limits
            if i < len(videos):
                time.sleep(self.config.get('rate_limit_delay', 2))

        self._print_summary(results)
        return results

    def _print_summary(self, results: Dict):
        """Print processing summary."""
        print(f"\n{'='*70}")
        print("PROCESSING SUMMARY")
        print(f"{'='*70}")
        print(f"Total videos: {results['total']}")
        print(f"✓ Successful: {results['success']}")
        print(f"✗ Failed: {results['failed']}")

        if results['errors']:
            print("\nFailed videos:")
            for error in results['errors']:
                print(f"  - {error['video']}")

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format bytes as human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract structured content from videos using Gemini API'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--videos',
        nargs='+',
        help='Specific video IDs or paths to process (default: all from config)'
    )
    parser.add_argument(
        '--api-key',
        help='Gemini API key (overrides config and env variable)'
    )

    args = parser.parse_args()

    # Set API key if provided
    if args.api_key:
        os.environ['GEMINI_API_KEY'] = args.api_key

    # Initialize extractor
    try:
        extractor = VideoExtractor(config_path=args.config)
    except Exception as e:
        print(f"Error initializing extractor: {e}")
        sys.exit(1)

    # Process videos
    results = extractor.process_batch(video_list=args.videos)

    # Exit with error code if any failed
    if results['failed'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
