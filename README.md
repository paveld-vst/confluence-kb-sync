# Confluence KB Sync

Confluence KB Sync is a lightweight Python utility that synchronizes selected Confluence Cloud pages into 
local Markdown files and makes them available inside your project as an AI-friendly knowledge base.

The main goal is to reduce context switching between IDE and Confluence, improve documentation discoverability, 
and make internal documentation usable by AI assistants inside JetBrains IDEs such as RubyMine, IntelliJ IDEA, 
WebStorm, and PyCharm.

---

# Overview

This tool:

- pulls selected Confluence pages via REST API
- converts them into structured Markdown
- builds a shared local knowledge base
- generates category and root index files
- copies the refreshed knowledge base into a selected project's `kb/` directory
- allows IDE AI assistants to use internal documentation as part of project context

---

# Problem It Solves

Working inside the IDE often means switching between code, tests, AI chat, wiki pages, and Confluence documentation.

This tool helps when:

- Confluence search is inconvenient or unreliable
- documentation is spread across multiple pages
- frequent browser switching interrupts the workflow
- AI assistants inside the IDE cannot directly access Confluence
- internal documentation needs to become part of project context

---

# How It Works

1. Confluence page URLs are defined in `config/pages.yaml`
2. The script retrieves page content through the Confluence REST API
3. HTML content is converted into AI-friendly Markdown
4. A shared local knowledge base is rebuilt from scratch
5. Root and category `_index.md` files are generated
6. The selected project's `kb/` directory is recreated from the shared knowledge base
7. The IDE indexes the updated files automatically

---

# Current Approach

This project uses a **shared KB + project cache** model.

Instead of storing documentation separately inside every project or relying on symlinks, the tool works like this:

- all synced Confluence pages are stored in one shared local directory
- on sync, the target project's `kb/` directory is recreated from that shared directory
- the IDE sees a normal physical `kb/` folder inside the project
- AI tools can use it as part of project context more reliably than symlink-based setups

This approach was chosen because symlink-based integration turned out to be inconsistent for AI tooling in IDE environments.

---

# Requirements

- Python 3.10 or newer
- access to Confluence Cloud
- Confluence API token
- JetBrains IDE with AI assistant support (recommended)

---

# Key Features

Current MVP includes:

- manual synchronization
- Confluence page download via API
- HTML to Markdown conversion
- AI-friendly Markdown structure
- category-based organization
- root and category index generation
- full refresh of shared KB on each run
- project-level `kb/` cache recreation

Not included yet:

- scheduled auto-sync
- multi-project sync in one command
- smart change detection
- section-based chunking for large documents
- AI-generated summaries
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

## 3. Configure credentials and pages

- create `config/config.yaml`
- fill in Confluence access settings
- edit `config/pages.yaml`
- add page URLs grouped by category

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

If your AI assistant is configured to use project files as context, it can use the synced documentation together with the codebase.

Typical use cases:

- asking about internal API behavior
- checking deployment requirements
- understanding business flows
- clarifying environment-specific rules
- answering questions based on internal documentation without opening Confluence manually

For best results, use prompts that ask for:

- step-by-step explanations
- documented constraints
- prerequisites
- exceptions
- edge cases
- implementation-relevant details

Example prompts:

- `How does authentication work according to our internal API documentation?`
- `Explain the documented login flow step by step, including constraints and exceptions.`
- `What environment-specific deployment requirements are described in our docs?`

---

# AI Assistant Guidance

This tool works best when the IDE AI assistant is explicitly instructed to treat the project's `kb/` directory as the primary internal documentation source when it exists.

A typical guidance rule may look like this:

```text
If the current project contains a directory named "kb" at the project root,
treat it as the primary source of truth for internal documentation.

For any question related to APIs, flows, deployment, business logic, environments, permissions, or system behavior:

1. First inspect the most relevant files in the "kb" directory before answering.
2. Use documentation details as the main basis for the answer.
3. Provide a thorough and structured response, not a brief summary.
4. Include concrete rules, constraints, edge cases, and exceptions when they are documented.
5. Synthesize information from multiple documentation files when needed.
6. Do not stop at a high-level overview if the documentation contains implementation details.
7. Only omit details when the user explicitly asks for a short answer.
8. Do not mention the "kb" directory or file paths unless the user asks for sources.

If documentation is incomplete or conflicting, clearly say so.
If no "kb" directory exists, ignore these rules.
```

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

If the shared KB directory is inside your user profile and outside the repository, it does not need to be tracked by Git.

---

# Limitations

Current limitations of the MVP:

- manual run only
- no partial sync
- no change tracking between runs
- no automatic summarization of document sections
- converted Markdown may not fully preserve complex Confluence formatting
- very large pages may still be less effective for AI tools than smaller, topic-specific documents

---

# Roadmap

Possible future improvements:

- scheduled synchronization
- multi-project update support
- document chunking by sections
- smarter extraction of key facts and constraints
- better normalization of Confluence content
- AI-friendly summary files
- semantic or local search over synced documentation

---

# Status

This project is currently in active development.

Current state: **MVP v0.1**

- manual sync works
- project cache generation works
- index generation works
- suitable for early internal usage and further iteration
