# dotclaude

Custom commands and skills for Claude Code.

## Commands

| Command | Description |
|---------|-------------|
| `/copy` | Copy Claude's last response to clipboard with proper markdown formatting |

## Usage

Copy commands to your `~/.claude/commands/` directory or symlink them.

```bash
# Copy a single command
cp commands/copy.md ~/.claude/commands/

# Or symlink the whole folder
ln -s $(pwd)/commands ~/.claude/commands
```
