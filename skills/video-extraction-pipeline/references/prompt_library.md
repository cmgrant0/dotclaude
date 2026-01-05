# Video Extraction Prompt Library

Pre-built prompt templates for different content types. Copy and adapt these to `config.yaml` for your specific use case.

**Note**: All prompts work with both local video files and YouTube URLs - no changes needed!

## Educational & Academic Content

### Online Courses / Lectures

```yaml
prompt_template: |
  You are extracting content from an educational video lesson.

  **Lesson:** {title}
  **Section:** {section}

  Extract and structure the following:

  1. **Learning Objectives** - What students should know/be able to do after this lesson
  2. **Key Concepts** - Main ideas, definitions, theories presented
  3. **Step-by-Step Explanations** - How concepts are broken down and taught
  4. **Examples & Demonstrations** - Specific examples used to illustrate concepts
  5. **Practice Problems** - Any exercises or problems presented
  6. **Common Mistakes** - Pitfalls or misconceptions addressed
  7. **Summary & Review** - Key takeaways at lesson end

  Include specific quotes that capture important explanations or clarifications.

output_format: |
  # {title}

  ## Learning Objectives
  - [Bulleted list of what students will learn]

  ## Key Concepts
  ### Concept 1: [Name]
  - Definition: [Clear definition]
  - Why it matters: [Context/importance]
  - Example: [Specific example from video]

  ## Step-by-Step Walkthrough
  [Numbered steps with explanations]

  ## Practice Problems
  [List problems/exercises mentioned]

  ## Common Mistakes to Avoid
  [Bulleted warnings or misconceptions]

  ## Summary
  [2-3 sentence recap]
```

### Math/Science Tutorials

```yaml
prompt_template: |
  Extract mathematical or scientific content with precision.

  Focus on:
  - **Formulas & Equations** - Extract exactly as presented
  - **Problem-Solving Steps** - Numbered procedure for each type of problem
  - **Variable Definitions** - What each symbol/variable represents
  - **Worked Examples** - Complete solutions shown in video
  - **Theorem/Rule Statements** - Precise wording of rules or theorems
  - **Visual Diagrams** - Describe any diagrams or graphs shown

output_format: |
  ## Topic Overview
  [Brief description]

  ## Formulas
  - **[Formula Name]**: `equation here`
    - Where: [define each variable]
    - Used for: [when to apply]

  ## Problem-Solving Procedure
  1. Step 1: [Action]
     - Why: [Reasoning]
  2. Step 2: [Action]

  ## Worked Examples
  ### Example 1
  **Problem**: [State problem]
  **Solution**:
  [Step-by-step solution]
```

## Business & Sales Training

### Sales Methodology & Frameworks

```yaml
prompt_template: |
  Extract sales frameworks, tactics, and methodologies from this training video.

  **Focus on actionable content:**

  1. **Frameworks** - Structured processes, methodologies (e.g., "5-step process")
  2. **Tactics** - Specific techniques and strategies
  3. **Scripts & Templates** - Exact wording for emails, calls, pitches
  4. **Objection Handling** - Common objections and proven responses
  5. **Real Examples** - Actual scenarios or case studies
  6. **Metrics & Benchmarks** - Numbers, conversion rates, targets mentioned
  7. **Common Pitfalls** - What NOT to do

  Use direct quotes from the instructor for key tactics or scripts.
  Include specific numbers and metrics whenever mentioned.

output_format: |
  ## Overview
  [What this lesson teaches]

  ## Core Framework
  [Name and structure of main methodology]

  ### Step 1: [Name]
  - **What to do**: [Action]
  - **How to do it**: [Details]
  - **Why it works**: [Reasoning]
  - **Example**: > "Quote from instructor"

  ## Scripts & Templates
  ```
  [Copy-paste ready scripts]
  ```

  ## Objection Handling
  | Objection | Response Tactic |
  |-----------|----------------|
  | [Objection] | [How to handle] |

  ## Key Metrics
  - [Metric]: [Benchmark]

  ## Pitfalls to Avoid
  - ❌ [Don't do this]
  - ✅ [Do this instead]
```

### Leadership & Management

```yaml
prompt_template: |
  Extract leadership principles, management techniques, and decision-making frameworks.

  Focus on:
  - **Leadership Principles** - Core philosophies and mindsets
  - **Management Techniques** - Specific practices for managing teams
  - **Decision Frameworks** - How to make difficult decisions
  - **Communication Strategies** - How to communicate effectively
  - **Real Scenarios** - Case studies or examples from experience
  - **Templates & Tools** - Meeting structures, 1-on-1 frameworks, etc.

output_format: |
  ## Leadership Principle: [Name]

  **Definition**: [What it means]

  **Why It Matters**: [Impact/importance]

  **How to Apply**:
  1. [Practical step]
  2. [Practical step]

  **Real Example**:
  > "[Quote from video showing application]"

  ## Management Techniques

  ### Technique: [Name]
  - **Situation**: [When to use]
  - **Steps**: [How to implement]
  - **Expected Outcome**: [What happens]
```

## Technical Training

### Software Development / Coding

```yaml
prompt_template: |
  Extract technical content from this programming tutorial.

  Focus on:
  - **Concepts & Terminology** - Technical definitions
  - **Code Examples** - Extract code exactly as shown
  - **Step-by-Step Procedures** - Setup, configuration, implementation steps
  - **Best Practices** - Recommended approaches and patterns
  - **Common Errors** - Bugs, mistakes, and how to fix them
  - **Tools & Commands** - Exact commands and tool usage
  - **Architecture Patterns** - Design patterns or system architecture

  Preserve code formatting and command syntax exactly.

output_format: |
  ## Concept: [Technical Concept]

  **Definition**: [Clear explanation]

  **Why It's Used**: [Purpose/benefit]

  ## Implementation Steps

  1. **[Step Name]**
     ```language
     // Code example
     ```
     - What this does: [Explanation]

  ## Best Practices
  - ✅ **Do**: [Recommendation]
  - ❌ **Don't**: [Anti-pattern]

  ## Troubleshooting
  | Error | Cause | Solution |
  |-------|-------|----------|
  | [Error] | [Why] | [Fix] |

  ## Commands Reference
  ```bash
  command --flag argument  # What it does
  ```
```

### DevOps / Infrastructure

```yaml
prompt_template: |
  Extract infrastructure setup, deployment procedures, and operational knowledge.

  Focus on:
  - **Architecture Diagrams** - Describe system architecture
  - **Configuration Steps** - Exact procedures for setup
  - **Commands & Scripts** - Extract all commands verbatim
  - **Security Considerations** - Security best practices mentioned
  - **Monitoring & Debugging** - How to troubleshoot issues
  - **Dependencies** - Required tools, versions, prerequisites

output_format: |
  ## System Architecture
  [Description of infrastructure/system design]

  ## Prerequisites
  - Tool/Service: Version
  - [List all dependencies]

  ## Setup Procedure

  ### Step 1: [Phase Name]
  ```bash
  # Commands in order
  command1
  command2
  ```
  **Expected Output**: [What you should see]

  ## Configuration
  ```yaml
  # config.yml
  [Configuration file contents]
  ```

  ## Troubleshooting
  **Issue**: [Problem]
  **Diagnosis**: [How to identify]
  **Fix**: [Solution]
```

## Creative & Production

### Video Editing / Production

```yaml
prompt_template: |
  Extract video production techniques, editing workflows, and creative decisions.

  Focus on:
  - **Techniques** - Specific editing or shooting techniques
  - **Software Tools** - Tools used and how to use them
  - **Workflow Steps** - Production or post-production procedures
  - **Creative Decisions** - Why certain choices were made
  - **Settings & Parameters** - Exact settings, shortcuts, configurations
  - **Examples** - Visual examples shown in the video

output_format: |
  ## Technique: [Name]

  **What It Is**: [Description]

  **When to Use**: [Situations/purposes]

  **How to Execute**:
  1. [Step with specific settings]
     - Tool: [Software/hardware]
     - Settings: [Exact parameters]

  ## Workflow: [Process Name]

  ### Phase 1: [Name]
  - Action: [What to do]
  - Tools: [Software/plugins]
  - Tips: > "[Quote from creator]"

  ## Shortcuts & Settings
  | Action | Shortcut | Setting Value |
  |--------|----------|---------------|
  | [Action] | [Key] | [Value] |
```

### Design / UX

```yaml
prompt_template: |
  Extract design principles, UX patterns, and design decision-making processes.

  Focus on:
  - **Design Principles** - Core philosophies and rules
  - **UX Patterns** - Specific interface patterns and when to use them
  - **Design Process** - Steps in the design workflow
  - **Tool Techniques** - How to use design tools (Figma, Sketch, etc.)
  - **Case Studies** - Real examples with before/after
  - **User Research** - Methods and findings mentioned

output_format: |
  ## Design Principle: [Name]

  **Definition**: [What it means]

  **Application**: [How to apply in practice]

  **Example**: [Real example from video]

  ## UX Pattern: [Pattern Name]

  **Problem It Solves**: [User need]

  **When to Use**: [Situations]

  **Implementation**:
  - Component: [UI element]
  - Behavior: [Interaction]
  - Accessibility: [Considerations]

  ## Design Process

  ### 1. [Phase]
  - **Goal**: [What to achieve]
  - **Methods**: [Techniques used]
  - **Deliverables**: [Outputs]
```

## Health & Fitness

### Workout Training

```yaml
prompt_template: |
  Extract exercise techniques, programming principles, and training methodologies.

  Focus on:
  - **Exercises** - Name, muscle groups, technique cues
  - **Form & Technique** - Detailed movement instructions
  - **Programming** - Sets, reps, rest periods, progression
  - **Common Mistakes** - Errors in form and how to correct
  - **Modifications** - Easier/harder variations
  - **Safety Considerations** - Injury prevention notes

output_format: |
  ## Exercise: [Name]

  **Target Muscles**: [Primary, Secondary]

  **Setup**:
  - Position: [Starting position]
  - Grip/Stance: [Details]

  **Execution**:
  1. [Step-by-step movement]
  2. [Breathing cue]
  3. [End position]

  **Form Cues**:
  - ✅ [Correct form point]
  - ❌ [Common mistake]

  **Programming**:
  - Beginner: [Sets × Reps]
  - Intermediate: [Sets × Reps]
  - Advanced: [Sets × Reps]

  **Modifications**:
  - Easier: [Variation]
  - Harder: [Progression]
```

## Marketing & Content

### Marketing Strategy

```yaml
prompt_template: |
  Extract marketing frameworks, campaign strategies, and content tactics.

  Focus on:
  - **Frameworks** - Strategic approaches and methodologies
  - **Messaging** - Key value propositions and positioning
  - **Tactics** - Specific campaign or content tactics
  - **Metrics** - KPIs and success metrics mentioned
  - **Examples** - Real campaign examples or case studies
  - **Templates** - Copy templates, ad structures, content formats

output_format: |
  ## Framework: [Name]

  **Purpose**: [What it's for]

  **Components**:
  1. [Element]: [Description]
  2. [Element]: [Description]

  ## Messaging Strategy

  **Target Audience**: [Who]

  **Value Proposition**: "[Quote from video]"

  **Key Messages**:
  - Primary: [Main message]
  - Supporting: [Secondary points]

  ## Campaign Tactics

  ### Tactic: [Name]
  - **Channel**: [Where to deploy]
  - **Format**: [Content type]
  - **Key Metrics**: [What to measure]
  - **Template**:
    ```
    [Copy-paste template]
    ```

  ## Case Study: [Example]
  - **Challenge**: [Problem]
  - **Solution**: [Approach]
  - **Results**: [Metrics/outcomes]
```

## Usage Instructions

1. **Identify your content type** from the categories above
2. **Copy the relevant template** to your `config.yaml`
3. **Customize** the prompt and output format for your specific needs
4. **Test** with 1-2 pilot videos
5. **Iterate** based on output quality

## Mixing Templates

You can combine elements from multiple templates. For example:

- **Sales + Technical**: Extract sales methodologies for selling technical products
- **Educational + Fitness**: Teaching exercise science concepts
- **Business + Creative**: Marketing creative production workflows

## Creating Custom Templates

If none of these fit, use this structure:

```yaml
prompt_template: |
  You are extracting [TYPE OF CONTENT] from this video.

  Focus on:
  - [Key element 1]
  - [Key element 2]
  - [Key element 3]

  Include:
  - Specific quotes that [CRITERIA]
  - [Any special formatting needs]
  - [Any domain-specific requirements]

output_format: |
  ## [Section Name]
  [What to include in this section]

  ## [Section Name]
  [Structure for this content]
```

**Pro Tip**: Look at existing high-quality content in your domain and reverse-engineer the structure you want the AI to produce.
