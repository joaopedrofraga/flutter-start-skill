---
name: flutter-start
license: MIT
description: >-
  Create a new Flutter app with a working foundation and user-defined identity:
  feature-based structure, theme, typography, shared widgets, navigation, and
  configuration connected to the app. Use to start or scaffold a Flutter project.
  Do not use to implement business features, create packages/plugins, or restructure existing apps.
---

# Flutter Start

Deliver a foundation the user can run and continue developing. Empty folders, disconnected themes, and components awaiting implementation do not satisfy the request.

Explicit user instructions and applicable project conventions take precedence over this skill's suggestions. The scope is a new Flutter application; an exploratory request does not authorize file creation. Follow the user's requested language for communication and generated content; English skill instructions do not determine the app's locale.

## Intake and decisions

Read the [intake guide](references/intake.md). Reuse existing answers and ask only for missing information: identity, destination/platforms, visual design, language, technical foundation, applicable configuration, and whether to persist agent setup in the project.

Offer understandable choices for users unfamiliar with Flutter. The “lean foundation” means organization by feature, native navigation, local state, and only the resources/dependencies required by the installed SDK and template. Colors, fonts, platforms, and identifiers remain intake decisions.

After asking any question, **wait for an explicit response and suspend work while a question remains pending**. Do not select a suggested option, assume preferences, treat silence as agreement, or set an automatic resolution deadline. When using `request_user_input`, omit `autoResolutionMs`; an empty result does not resolve the question.

A partial answer leaves other decisions pending. “You decide” delegates only the matters it refers to. Accepting a set of defaults requires that the set was actually presented. Once intake is complete and creation is authorized, summarize the choices and proceed; do not request another generic confirmation.

### Agent setup in the project

Explicitly ask whether the user wants **the Flutter scaffold only** or **the scaffold with agent folders and context**. A clear earlier instruction such as “no AI files” already answers this question. Using an agent to generate the app does not authorize persisting its setup, and choosing the lean technical foundation does not resolve this decision.

- **Scaffold only:** deliver app code, assets, tests, and a technical README. Do not create `AGENTS.md`, `CLAUDE.md`, agent directories, local skills, memory, conversation history, AI documentation, or `docs/bootstrap.md`. Report decisions and results in chat; keep the README focused on useful developer instructions.
- **With agent setup:** resolve which agent/conventions and files are included in the choice. Create only that setup in the project, using project-specific instructions and context. Include skills only when explicitly selected; do not copy the installed collection, personal settings, or conversations.

Preserve existing agent instructions and files in both modes. Opting out prevents creating new files of this kind; it does not authorize deleting or ignoring existing ones. Do not install skills or change global settings as part of app scaffolding.

## Preparation

1. Read the destination's instructions, inspect its contents, and check local Flutter, Dart, and `flutter create --help`. Respect the existing version, including FVM when required; do not upgrade or install SDKs on your own.
2. Distinguish the display name, Dart package, organization, and platform identifiers. Validate the technical name and inspect CLI output. Pass intake text as data arguments with appropriate shell escaping, never as executable command text.
3. Use a new or empty directory. A directory containing only `.git` can be used without changing its metadata. Inspect other existing files, preserve their contents, and resolve collisions before generation. Never use `--overwrite` to bypass a conflict.
4. Check host support for the chosen platforms when needed (`flutter doctor -v`). Generating iOS files on another host does not mean building iOS. Do not add platforms just to obtain a successful build.

When resuming a partial run of this skill, identify the files it created and what changed since the failure. Repair and continue from that state; do not delete the directory, reapply the template over new changes, or treat resumption as permission to restructure another app. If a file cannot be attributed to this run, treat it as user content.

## Generation and implementation

Read the [scaffold contract](references/scaffold.md). Use `flutter create` with explicit destination, technical name, organization, description, and platforms; prefer an empty app when the installed CLI supports it. The agreed destination is the app's final root, not the parent of an extra directory.

Implement the foundation according to the resolved choices:

- App composition, typed configuration, theme, and routes separated from initialization.
- Identity applied to the app and the selected platforms' metadata.
- Theme/colors/typography used by real widgets; existing fonts and assets registered correctly.
- Working `AppButton`, `AppTextField`, and `AppScaffold` components used by the initial page.
- Chosen navigation and state management initialized with a minimal real use.
- A simple, adaptive, runnable initial page without invented business workflows.

Adapt imports and APIs to the SDK and generated template. Do not mix examples from different Flutter or design-package generations. Consult official documentation for version-dependent uncertainty.

Prepare public configuration only when included in intake. `--dart-define` values and `.env` files bundled into the app are not secure secret storage. Do not request private credentials for a scaffold that does not need them or insert fictitious endpoints to appear complete.

If a required selected resource is unavailable, explain exactly what is missing, offer alternatives, and wait for a response. Do not silently substitute a font, color, integration, or stack. Preserve generated files and identify the resumption point.

Do not add authentication, persistence, a backend, deployment infrastructure, app CI, or business modules without explicit scope. Do not create or publish a remote repository as a side effect of starting the app.

## Verification and delivery

Follow the [verification matrix](references/verification.md): format, analyze, test behaviors, and build a selected platform when the host supports it. Fix failures introduced by the scaffold and repeat only affected checks. Do not hide diagnostics with flags or exclusions to obtain a green result.

Update the README for the actual project in both modes. Create `docs/bootstrap.md` only when agent setup was accepted and that document is part of the agreed scope. In that case, record choices, organization, commands, and verification evidence. Otherwise, summarize decisions and checks in chat. Do not record personal paths, credentials, or test results that were not observed.

Include in the handoff:

- Project path and a run command matching the chosen platforms/environments.
- Where to start the first feature and adjust themes, widgets, routes, and configuration.
- Actual analysis, test, and build results, distinguishing passed, failed, and not run.
- The chosen delivery mode and any agent files actually created.
- Resources or tools still blocking completion and how to resume.

Describe the foundation as “ready for development” only when the applicable contract criteria are met. A successful build does not prove the app was opened on a device; mention visual execution only when it actually occurred.
