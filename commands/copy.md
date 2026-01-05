---
description: Copy Claude's last response to clipboard with proper markdown formatting
---

# Copy to Clipboard

Copy your most recent response (the one immediately before this command was invoked) to the macOS clipboard using pbcopy.
   
## Instructions

1. **Extract the content**: Identify your last response before this /copy command was executed
2. **Clean the output**:
   - Remove all tool calls, tool results, and system messages
   - Remove thinking blocks
   - Remove "Insight" boxes (they're conversational aids, not deliverable content)
   - Keep only the main text response that was visible to the user
   - Preserve ALL markdown formatting (headers, lists, bold, italic, code blocks, links, etc.)
3. **Copy to clipboard**: Use the Bash tool with a heredoc to pipe the cleaned content to pbcopy:
   ```bash
   cat << 'EOF' | pbcopy
   [cleaned content here]
   EOF
   ```
4. **Confirm**: After copying, tell the user:
   - What type of content was copied (e.g., "proposal", "email draft", "explanation")
   - Approximate word count or line count
   - That it's ready to paste

## Important Notes

- Do NOT re-execute any commands or tools from the previous response
- Do NOT regenerate content - copy what was already written
- If the last response was very short (like "Done" or "OK"), ask the user if they meant to copy a different response
- If unsure which response to copy, ask for clarification
