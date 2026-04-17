# Confluence KB Sync

> Hello, brave reader.
>
> You have just discovered a still-slightly-chaotic but already usable MVP.
> It is not fully polished, not deeply battle-tested, and was originally built on Windows — so if you are trying it on macOS, you are also helping science.
>
> That said, the tool is already available for early testing and experimentation, and I genuinely hope it can be useful in your daily work.
>
> If something looks strange, breaks unexpectedly, or behaves like it was coded late at night... first, please accept my apologies. Second, feel free to investigate it yourself like a true engineer. That was a joke. Mostly.
>
> If you have feedback, ideas, questions, or improvements, please reach out — I would be very happy to hear from you.
>
> — Pavel Dorojchin 


Confluence KB Sync is a lightweight Python tool that synchronizes selected Confluence Cloud pages into local 
Markdown files and turns them into an AI-friendly knowledge layer inside your project.

The main goal is not only to reduce context switching between the IDE and Confluence, but also to make internal 
documentation part of the working project context, so AI assistants inside JetBrains IDEs such as RubyMine, 
IntelliJ IDEA, WebStorm, and PyCharm can use it when answering questions, writing tests, suggesting fixes, 
and helping with implementation work.

---

# Overview

This tool:

- pulls selected Confluence pages via REST API
- converts them into structured AI-friendly Markdown
- builds a shared local knowledge base
- generates category and root index files
- copies the refreshed knowledge base into a selected project's `kb/` directory
- turns internal documentation into usable project context for IDE AI assistants
- helps AI tools rely not only on code, but also on documented flows, rules, constraints, and internal behavior

---

# Problem It Solves

Working inside the IDE often means switching between code, tests, AI chat, wiki pages, and Confluence documentation.

This becomes especially painful when AI assistants can see the codebase, but cannot reliably use the internal documentation 
that explains business flows, API behavior, constraints, and environment-specific rules.

This tool helps when:

- Confluence search is inconvenient or unreliable
- documentation is spread across multiple pages
- frequent browser switching interrupts the workflow
- AI assistants inside the IDE cannot directly access Confluence
- internal documentation needs to become part of project context
- engineering work depends not only on code, but also on documented internal behavior

---

# How It Works

1. Confluence page URLs are defined in `config/pages.yaml`
2. The script retrieves page content through the Confluence REST API
3. HTML content is converted into AI-friendly Markdown
4. A shared local knowledge base is rebuilt from scratch
5. Root and category `_index.md` files are generated
6. The selected project's `kb/` directory is recreated from the shared knowledge base
7. The IDE indexes the updated files automatically
8. AI assistants can then use the synced documentation as part of the working project context

---

# Current Approach

This project uses a **shared KB + project cache** model.

Instead of storing documentation separately inside every project or relying on symlinks, the tool works like this:

- all synced Confluence pages are stored in one shared local directory
- on sync, the target project's `kb/` directory is recreated from that shared directory
- the IDE sees a normal physical `kb` folder inside the project
- AI tools can use it as a stable project context source more reliably than symlink-based setups

This approach was chosen because symlink-based integration turned out to be inconsistent for AI tooling in IDE environments. 
In practice, having real local files inside the project works more reliably for indexing, context usage, and day-to-day 
AI-assisted development.

---

# Requirements

- Python 3.10 or newer
- access to Confluence Cloud
- a Confluence API token
- a JetBrains IDE with AI assistant support (recommended)

---

# Key Features

Current MVP includes:

- manual synchronization
- selected Confluence page download via API
- HTML to Markdown conversion
- AI-friendly Markdown preparation
- category-based documentation organization
- root and category index generation
- full refresh of the shared knowledge base on each run
- project-level `kb/` cache recreation
- local project context preparation for IDE AI assistants

Not included yet:

- scheduled auto-sync
- multi-project sync in one command
- smart change detection
- section-based chunking for large documents
- richer AI-friendly summaries
- semantic search

---

# Project Structure

```text
confluence-kb-sync/
├── config/
│   ├── config.example.yaml
│   ├── config.yaml
│   └── pages.yaml
├── src/
│   ├── main.py
│   ├── config_loader.py
│   ├── confluence_client.py
│   ├── page_parser.py
│   ├── markdown_builder.py
│   ├── file_writer.py
│   └── index_builder.py
├── README.md
├── requirements.txt
└── .gitignore
```

Main components:

- `config/config.example.yaml` — example local configuration
- `config/config.yaml` — local Confluence credentials and output path
- `config/pages.yaml` — selected Confluence page URLs grouped by category
- `src/main.py` — main sync flow and project cache refresh
- `src/config_loader.py` — YAML config loading and validation
- `src/confluence_client.py` — Confluence API access
- `src/page_parser.py` — page ID extraction from Confluence URLs
- `src/markdown_builder.py` — AI-friendly Markdown generation
- `src/file_writer.py` — category-based file output
- `src/index_builder.py` — root and category index generation

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd confluence-kb-sync
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

## 1. Create local config

Copy `config/config.example.yaml` to `config/config.yaml` and fill in your Confluence credentials.

Example:

```yaml
confluence:
  base_url: https://your-company.atlassian.net/wiki
  email: your.email@company.com
  api_token: YOUR_API_TOKEN

output:
  path: C:/Users/Your.Name/kb/confluence_docs
```

## 2. Define pages to sync

Edit `config/pages.yaml` and group Confluence page URLs by category.

Example:

```yaml
api:
  - https://your-company.atlassian.net/wiki/spaces/TEAM/pages/123456789/API+Overview
  - https://your-company.atlassian.net/wiki/spaces/TEAM/pages/123456790/Auth+Flow

deployment_and_env:
  - https://your-company.atlassian.net/wiki/spaces/TEAM/pages/123456791/Deployment+Guide

business_flows:
  - https://your-company.atlassian.net/wiki/spaces/TEAM/pages/123456792/Order+Lifecycle
```

---

# Output Directory

The shared knowledge base is stored outside of any specific project.

This allows multiple projects to reuse the same synced documentation source.

Recommended examples:

## Windows

```yaml
output:
  path: C:/Users/Your.Name/kb/confluence_docs
```

## macOS / Linux

```yaml
output:
  path: /Users/your.name/kb/confluence_docs
```

Using an absolute path is recommended to avoid platform-specific path issues.

---

# Usage

## Sync only shared knowledge base

```bash
python src/main.py
```

This will rebuild the shared KB in the configured output directory.

## Sync shared knowledge base and refresh project cache

### Windows

```bash
python src/main.py --project-path C:/vst/vst-ui-tests
```

### macOS / Linux

```bash
python src/main.py --project-path /Users/your.name/projects/vst-ui-tests
```

This will:

- rebuild the shared KB
- generate `_index.md` files
- recreate the project's `kb/` directory from the shared KB

---

# Generated Output

After a successful sync, the shared KB may look like this:

```text
confluence_docs/
├── _index.md
├── api/
│   ├── _index.md
│   ├── API_Overview.md
│   └── Auth_Flow.md
├── deployment_and_env/
│   ├── _index.md
│   └── Deployment_Guide.md
└── business_flows/
    ├── _index.md
    └── Order_Lifecycle.md
```

The selected project will then receive:

```text
your-project/
└── kb/
    ├── _index.md
    ├── api/
    ├── deployment_and_env/
    └── business_flows/
```

---

# Using the Knowledge Base in JetBrains IDEs

Open the target project in your IDE after the `kb/` folder has been created or refreshed.

If your AI assistant is configured to use project files as context, it can use the synced documentation together 
with the codebase as part of the working project context.

This is useful not only for answering documentation-related questions, but also for everyday engineering tasks such as:

- understanding internal API behavior
- following documented business flows
- checking deployment requirements
- clarifying environment-specific rules
- writing tests based on documented logic
- suggesting fixes with documented constraints in mind
- helping with implementation work based on internal documentation

For best results, use prompts that ask for:

- step-by-step explanations
- documented constraints
- prerequisites
- exceptions
- edge cases
- implementation-relevant details

Example prompts:

- `Based on the Enhanced Price Controls documentation in this project, give me a detailed explanation of the feature, including backend, frontend, calculation logic, UI behavior, and key constraints.`
- `Based on the Enhanced Price Controls documentation in project, what UI test scenarios should be covered in Cypress for this feature, including key user flows, validations, and edge cases?`
- `Based on the API v4 Products Search documentation in this project, what documented rules, constraints, and edge cases should be reviewed before changing this logic?`
- `Based on the v4/purchase and Split Payment documentation in this project, explain what v4/purchase needs to support Split Payment for Virtual Bookstore and Cashier, including key constraints and edge cases.`

---

# AI Assistant Guidance

To get the best results, the IDE AI assistant should be explicitly instructed to treat the project's `kb/` directory 
as the primary internal documentation source when it exists.

The goal is not only to improve documentation-based Q&A, but also to make internal documentation part of the working 
project context, so the assistant can use it during everyday engineering tasks such as understanding flows, 
writing tests, reviewing changes, suggesting fixes, and helping with implementation work.

A typical guidance rule for GLOBAL config may look like this:

```text
If the current project contains a directory named "kb" at the project root,
treat it as the official internal documentation for that project.

For any questions related to APIs, business logic, flows, deployment, or system behavior:

1. Actively analyze relevant files inside the "kb" directory.
2. Base answers strictly on those files when they exist.
3. Prefer documentation content over general knowledge.
4. Provide comprehensive, structured, and detailed explanations.
5. Do not provide generic summaries when specific documented rules or constraints are available.
6. Use the documentation not only for answering questions, but also for helping with tests, fixes, and code changes.
7. Do NOT explicitly mention the "kb" directory or reference file paths in the response unless the user asks for sources.

If no "kb" directory exists, ignore these rules.
```

And for WORKSPACE config like this:

```text
In this project, if documentation relevant to the question exists in the root "kb" directory, prioritize it before relying on 
general codebase context.

When multiple documentation files are relevant, combine them into one detailed answer.
Prefer specific documented rules, constraints, examples, and implementation details over generic summaries.

If a relevant documentation file is already open or explicitly attached in chat context, use it as the primary source before 
searching more broadly.
```

For more reliable results, it is recommended to use both **Global** and **Workspace** Copilot instructions.

- **Global instructions** define the general behavior for treating `kb/` as internal project documentation.
- **Workspace instructions** reinforce that behavior for the current project and help the assistant prioritize relevant local documentation more consistently.

In practice, this combination may improve how Copilot uses project documentation as context.


---

# Security Notes

- never commit `config/config.yaml` with real credentials
- never commit API tokens
- keep the shared KB directory out of Git
- keep project-level generated `kb/` folders out of Git unless there is a specific reason to version them
- use `.gitignore` for all local-only and generated files

Recommended exclusions:

```gitignore
config/config.yaml
kb/
```

If the shared KB directory is stored outside the repository, it does not need to be tracked by Git.

---

# Limitations

Current limitations of the MVP:

- manual run only
- no partial sync
- no change tracking between runs
- no advanced summarization of document sections
- converted Markdown may not fully preserve complex Confluence formatting
- very large pages may still be less effective for AI tools than smaller, topic-specific documents
- the quality of AI responses still depends on the quality and structure of the source documentation

---

# Roadmap

Possible future improvements:

- scheduled synchronization
- multi-project update support
- document chunking by sections
- smarter extraction of key facts and constraints
- better normalization of Confluence content
- richer AI-friendly summary files
- semantic or local search over synced documentation

---

# Status

This project is currently in active development.

Current state: **MVP v0.1**

- manual sync works
- shared KB refresh works
- project cache generation works
- index generation works
- suitable for early internal usage and further iteration
- already useful as an AI-friendly documentation context layer inside the IDE
