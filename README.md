# flutter-start-skill

A skill for turning the start of a Flutter app into a working foundation with visual identity, organization by feature, and components ready for development.

The repository is named `flutter-start-skill`. The installed skill remains `flutter-start`, invoked with `$flutter-start`.

The skill collects missing decisions, waits for your answers, and creates the project using the installed SDK. It delivers an applied theme, shared widgets, navigation, typed configuration, an initial screen, tests, and instructions for continuing development.

## What it prepares

- Display name, Dart package name, and platform identifiers.
- Selected platforms and organization into `app/`, `shared/`, and `features/`.
- Color palette, typography, spacing, and theme modes.
- A button with a loading state, a field with validation, and a shared page scaffold.
- Navigation and state management according to intake; a lean foundation is available if you have no preferred stack.
- Public configuration and environments when requested.
- An app README with commands and guidance for starting development.
- Agent folders/context, selected skills, and `docs/bootstrap.md` only when explicitly included in intake.

The goal is to prepare the chosen infrastructure. Authentication, databases, backends, and product features are included only when requested. The skill does not require a paid service or an MCP connection.

## Choosing agent setup

Intake asks whether you want **the Flutter scaffold only** or **the scaffold with agent setup**. This decision is independent of colors, architecture, and state management.

- **Scaffold only:** app code, assets, tests, and a technical README. No new agent folders, skills, files such as `AGENTS.md`/`CLAUDE.md`, memory, or AI documentation. Decisions and verification results are delivered in chat.
- **With agent setup:** prepare only the agreed agent/conventions and files. Skills must be explicitly selected; the personal collection is not copied automatically.

Existing agent files are preserved in both modes. Installing Flutter Start itself, as described below, is separate from choosing to include agent setup in the generated application.

## Requirements

To use the skill: an agent that supports Markdown skills, terminal/file access, and Flutter and Dart available in the environment. Each platform requires its own build toolchain. Dependencies and fonts may require network access when not cached.

Python and PyYAML are needed only to validate or package this repository; they are not dependencies of the generated app or normal skill execution.

## Installation

The distribution ZIP contains a `flutter-start/` directory. Place it in a skills directory recognized by your agent, preserving `SKILL.md`, `LICENSE`, `agents/`, and `references/`.

For current Codex installations, documented locations include `.agents/skills/` in the project and `~/.agents/skills/` for the user. Environments that already provide another skills directory should receive the same folder there. Consult the [official skills documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and installation in your environment.

Example project installation:

```text
.agents/
  skills/
    flutter-start/
      SKILL.md
      LICENSE
      agents/openai.yaml
      references/
        intake.md
        scaffold.md
        verification.md
```

Avoid installing two copies with the same skill name in different locations. To update, preserve local customizations and deliberately replace the previous installation. If the skill does not appear, restart the agent session.

You can also ask Codex's `$skill-installer` to install from [joaopedrofraga/flutter-start-skill](https://github.com/joaopedrofraga/flutter-start-skill). `SKILL.md` is at the repository root; use `flutter-start` as the installation name:

```text
Use $skill-installer to install https://github.com/joaopedrofraga/flutter-start-skill
from the repository root, with the installation name flutter-start.
```

The repository name and installed skill name serve different purposes: keep the installation directory named `flutter-start`.

## Usage

```text
Use $flutter-start to start a new Flutter application.
```

You can provide intake details upfront:

```text
Use $flutter-start to create My Garden in ./my_garden.
Purpose: track plant care.
Dart package: my_garden. Development organization: com.example.
Platforms: Android and web. Language: en-US, with no additional languages.
Exact primary color: #166534; derive the remaining palette.
Light and dark themes following the system; system font.
Use the lean foundation, with no integrations, extra environments, custom logo, or app icon.
I want the Flutter scaffold only, with no agent folders or AI documentation.
```

Once decisions are resolved, the agent creates the foundation without another generic approval. If information is missing or files conflict, it asks and waits for an explicit response. The app's name and purpose do not authorize implementing business features.

The repository documentation is in English. The language of generated app text and documentation follows the user's choices; using this skill does not force an English app locale.

## Skill organization

| File | Responsibility |
| --- | --- |
| [SKILL.md](SKILL.md) | Scope, interaction rules, and main workflow. |
| [intake.md](references/intake.md) | Progressive intake, proposals, and partial answers. |
| [scaffold.md](references/scaffold.md) | Organization, widget contracts, and visual identity. |
| [verification.md](references/verification.md) | App tests, builds, and delivery evidence. |
| [openai.yaml](agents/openai.yaml) | Presentation and invocation metadata. |

## Validate and package

From the repository root, with Python 3.10 or later:

```text
python -m pip install -r requirements-dev.txt
python tools/validate_skill.py
python -m unittest discover -s tests -v
python tools/package_skill.py
```

The packager produces `dist/flutter-start.zip` and `dist/flutter-start.zip.sha256`. The ZIP contains only installable files and the license; `.git`, maintenance tools, tests, and environment files are excluded. Entry order, paths, permissions, and timestamps are normalized.

The validator checks YAML metadata, duplicate keys, local references, packaged resources, and common personal machine paths. It does not check external links over the network or replace agent behavior evaluation.

The [Validate skill workflow](.github/workflows/validate.yml) configures these checks on Windows/Linux and Python 3.10/3.13. It does not run an agent or guarantee Flutter builds on every platform. The artifact becomes available in the GitHub Actions run when the workflow passes.

See the [local validation record](tests/VALIDATION.md) for observed results, Flutter verification, and coverage limits.

## Evaluation and contribution

Before changing the workflow, run the checks above and relevant [behavior evaluation scenarios](tests/behavior.md) in an isolated destination. Distinguish executed scenarios from those only reviewed. Changes should preserve user choices and the boundary between scaffolding and product implementation.

The skill is instruction-based; it is not a deterministic code generator and does not promise universal compatibility with every SDK or stack. Readiness evidence belongs to each generated project.

## License

Distributed under the [MIT License](LICENSE). Copyright (c) 2026 João Fraga.

This skill's license does not automatically determine the license of generated applications. Third-party resources, such as fonts, retain their own licenses.
