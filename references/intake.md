# App intake

Use this reference before generating files. Resolve decisions that affect the foundation without requiring the user to know tool names.

## Conducting intake

1. Extract what the conversation already answers and identify pending or explicitly delegated decisions.
2. Group missing points into a short message. If many choices remain, start with identity/destination/visual design and use a second technical round only when necessary.
3. Offer options with practical consequences and allow free-form answers. Do not automatically turn a suggestion into a decision.
4. After asking a question, wait for the answer and do not continue other work. Optional questions also remain pending until answered or explicitly withdrawn by the user.
5. Once intake is complete, announce the choices and begin the already authorized generation. Reopen decisions only if a conflict or new information appears.

Track each decision in context or the plan as answered, delegated, or pending. This is execution state for the agent, not a technical form the user must complete.

## Decisions to resolve

| Item | How to obtain or propose it |
| --- | --- |
| Display name and purpose | The user-facing name and a sentence about the app. Do not invent features from that sentence. |
| Dart package | Propose `lowercase_with_underscores` derived from the name and validate it with the CLI. Make transformations of accented names explicit. |
| Destination directory | Resolve the absolute path before creation; clarify whether the given path is the app root or a parent directory. |
| Platforms | Ask where the app should run. Do not generate every platform for convenience. |
| Organization and IDs | Ask for existing organization/identifiers. If absent, offer clearly identified development identifiers and obtain acceptance. Do not invent a domain that appears to belong to the user. |
| Colors | Primary color and whether exact reproduction is required; existing additional palette or permission to derive remaining tones. Accept HEX values and visual references. Turn vague colors such as “blue” into a concrete proposal the user can answer. |
| Theme modes | Light, dark, or both. For both, propose following the system; add a selector and persistence only if part of the choice. |
| Typography | System font or a custom family. For custom fonts, obtain the actual source/files and weights used; do not request files for a system-font choice. |
| Languages | Initial language, supported languages, and selection policy when there is more than one. Do not infer locale from the conversation's language alone. |
| Technical foundation | Use supplied choices; offer the lean foundation when no stack is specified. Explain Riverpod/Bloc/GoRouter only when relevant. |
| Agent setup | Ask whether the user wants only the Flutter scaffold or also agent folders/context. Without setup: app, assets, tests, and a technical README only, with no skills, memory, or AI documentation. With setup: resolve the agent/conventions and included files; do not copy skills automatically. |
| Configuration and integrations | Ask whether any need preparation. “None for now” resolves the item. Request environments and public URLs only when applicable. |
| Logo and app icon | Ask whether to apply them now. “No custom logo/icon” is a complete decision; retain template resources and record that choice. Do not promise a publication-ready icon from an unsuitable image. |

Present technical name, organization, and destination as derived proposals when useful, so users need not invent technical terms. Still obtain an answer for proposals not already authorized.

## Example first intake

Adapt this example and remove everything already answered:

> To prepare the foundation, I need:
>
> - App name and a one-sentence purpose.
> - Destination directory and target platforms.
> - Primary color/palette and light, dark, or both theme modes.
> - Font and language; a system font is an option.
> - Existing organization/identifiers, if any.
> - Any navigation/state preferences, integrations, logo, or icon to prepare now? For the technical foundation, I can use the lean option: separate features, native navigation, and local state.
> - Do you want only the Flutter scaffold, or also agent folders and context in the project? If you want agent setup, specify the agent and what to include.
>
> From the app name, I will propose a Dart package name for you to validate. If you want me to decide any of these points, specify which ones.

This example opens a question. Stop and wait for the answer before inspecting the environment or generating files.

## Answers requiring care

- **“Use the defaults.”** Apply only defaults actually presented and within the answer's scope. “Lean foundation” does not choose a color, organization, or platform.
- **“Only the scaffold, no AI files.”** Treat the no-agent-setup choice as resolved; do not insist or create agent folders, skills, instructions, or AI documentation. A technical README remains part of the app.
- **“I also want agent folders.”** If the agent/conventions and files are undefined, resolve them before creating the setup. Accepting setup does not authorize installing every existing skill or saving context outside the project.
- **“Choose the visual design.”** Choose and record palette and typography; do not extend delegation to the stack, destination, or identifiers.
- **“I want Inter but do not have the files.”** Check an official source and its license. If required resources can be obtained within existing authorization, integrate them. Otherwise, present alternatives and wait. Do not claim Inter is installed by setting `fontFamily` alone.
- **“Create it in a directory that already has files.”** Inspect only when no question is pending. Explain concrete collisions and obtain the necessary decision; do not replace existing content.
- **“I only want the architecture.”** Respond to the exploratory scope; do not create the app.
- **Complete intake.** Do not repeat the questionnaire or request generic approval. Check the environment and carry out the already requested creation.
