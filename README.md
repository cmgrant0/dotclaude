# dotclaude

Custom commands and skills for Claude Code.

## Commands

| Command | Description |
|---------|-------------|
| `/copy` | Copy Claude's last response to clipboard with proper markdown formatting |

## Skills

| Skill | Description |
|-------|-------------|
| `gemini-image-gen` | Generate images using Google's Gemini API with style presets and reference images |
| `video-extraction-pipeline` | Extract structured content from video courses into markdown knowledge bases |

## Usage

### Commands

Copy commands to your `~/.claude/commands/` directory:

```bash
cp commands/copy.md ~/.claude/commands/
```

### Skills

Copy skills to your `~/.claude/skills/` directory:

```bash
cp -r skills/gemini-image-gen ~/.claude/skills/
cp -r skills/video-extraction-pipeline ~/.claude/skills/
```

## License

MIT
