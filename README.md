# Confluence KB Sync

Confluence KB Sync is a lightweight tool that synchronizes selected
Confluence Cloud pages into a local, AI-friendly knowledge base.

The generated knowledge base can be used directly by JetBrains IDEs
(RubyMine, IntelliJ IDEA, WebStorm, PyCharm) together with AI Copilot
to answer questions about internal documentation without opening Confluence.

---

## Why this tool exists

In many teams, important technical documentation lives in Confluence:
- API contracts
- user flows
- feature descriptions
- environment details

However:
- Confluence search is often slow or inconvenient
- switching between IDE and browser breaks focus
- AI Copilot cannot access Confluence directly

This tool solves the problem by converting Confluence pages into
local Markdown files that are automatically indexed by the IDE
and used as context by AI Copilot.

---

## Key features (MVP v0.1)

- Manual synchronization of Confluence Cloud pages
- Category-based structure (API, flows, features, misc)
- Clean Markdown output
- AI-friendly document wrapper (title, source, timestamp)
- Shared knowledge base for multiple projects
- Works for QA engineers and developers
- Language-independent:
  - documentation in English
  - questions and answers in English or Russian

---

## How it works

1. You specify Confluence page URLs grouped by categories
2. The tool downloads page content via Confluence REST API
3. HTML content is converted to Markdown
4. Each page is saved into a shared local knowledge base
5. Projects link to this knowledge base via a symlink
6. AI Copilot automatically uses the documentation as context

---

## Project structure

confluence-kb-sync/
├── src/ # Source code
├── config/ # User configuration
├── scripts/ # Helper scripts (symlinks)
├── README.md
├── README_RU.md
└── requirements.txt

---

## Requirements

- Python 3.9 or newer
- Access to Confluence Cloud
- Confluence API token
- JetBrains IDE with AI Copilot (recommended)

---

## Installation

1. Clone the repository: 

	git clone <repository-url>
	
2. Install dependencies: 

	pip install -r requirements.txt
	
3. Configure Confluence access:
- edit `config/config.yaml`
- provide your email and API token

4. Specify pages to sync:
- edit `config/pages.yaml`
- group page URLs by category

### Output directory configuration

The documentation is stored in a shared local directory outside of any project.
This allows multiple projects to reuse the same knowledge base.

It is recommended to use an **absolute path** in `config/config.yaml`
to avoid platform-specific issues.

#### Example (Windows)

yaml >> output:
  path: C:/Users/Your.Name/kb/confluence_docs
  
#### Example (Mac OS/Linux)

yaml >>	output:
  path: /Users/your.name/kb/confluence_docs

---

## Usage

Run the synchronization manually:

	python src/main.py
	
After successful execution, Markdown files will be generated
in the configured output directory.

---

## Using the knowledge base with AI Copilot

1. Create a symlink named `.kb` in your project root
   pointing to the knowledge base directory
2. Open the project in a JetBrains IDE
3. Ask questions in AI Copilot chat, for example:
   - "According to our API documentation, how does authentication work?"
   - "What login flows are described in our docs?"

AI Copilot will automatically use the synced documentation
as part of the project context.

---

## Security notes

- Never commit `config/config.yaml` with API tokens
- The knowledge base directory should not be committed to Git
- Use `.gitignore` to exclude local files

---

## Roadmap

Future versions may include:
- Automatic scheduled synchronization
- AI-generated summaries
- Content cleanup and normalization
- Local search or chat over documentation

---

## Status

This project is in active development.
Current version: **MVP v0.1 (manual sync)**.
	



