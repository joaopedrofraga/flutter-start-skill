# Local validation record

Date: November 24, 2026. This record describes checks observed during development; it does not guarantee universal compatibility.

## Repository and distribution

Environment: Windows, Python 3.13.7, and PyYAML 6.0.3.

| Check | Result |
| --- | --- |
| Portable metadata, resource, and local-reference validator | Passed. |
| Official `quick_validate.py` from skill-creator | Passed. |
| `python -m unittest discover -s tests -v` | 18 tests passed, with no skips. |
| Actual ZIP creation and extraction | Passed; the extracted package passed validation. |
| Updated local installation | Passed; files compared with the source using SHA-256. |
| `git diff --check` | Passed. |
| GitHub workflow | YAML and matrix checked locally; remote execution has not occurred. |

Distribution tests exercise empty/invalid metadata, duplicate YAML keys, incorrect invocation, missing references, path escapes, excluded files, missing/absolute icons, personal paths, external symlinks, CLI validation, maintenance-file exclusion, checksums, extraction, and repeatable packaging. They also verify that an invalid source does not replace an existing ZIP.

## Flutter verification

A temporary application outside the repository exercised the scaffold contract. This verification was performed directly during development; it is not part of the Python tests or public workflow.

Environment: Flutter 3.47.5 stable and Dart 3.13.4 on Windows. Selected fixture platform: web.

Configuration exercised: native navigation, local state, typed configuration, exact light-mode primary color, light/dark themes following the system, pt-BR/en-US with fallback resources, and a bundled Roboto font in the used weights. The font license was preserved in the fixture.

| Check | Result |
| --- | --- |
| Dependency resolution | Passed. |
| Localization generation | Passed; base resources required by the SDK were added. |
| Formatting | Applied. |
| `flutter analyze` | No issues found. |
| `flutter test` | 10 tests passed. |
| `flutter build web` | Completed, including the Wasm dry run. |
| Visual execution in a browser/device | Not performed. |

The ten tests check initial route/identity/locale in light and dark modes, form validation and feedback, narrow layout with enlarged text, enabled/disabled buttons, blocking during loading, ownership of external controllers, system brightness changes, language switching for application/Material messages, and bundled font loading/application.

The previous foundation's first build reported a missing `CupertinoIcons` family. During refinement, the font was integrated through its corresponding dependency, also included in the SDK's standard template. The final build included Cupertino and Material assets without the missing-family diagnostic; no flags were used to hide it.

## Evidence limits

- The GitHub workflow still needs to run remotely to verify its configured Linux and Python 3.10 targets.
- Android, iOS, Windows, macOS, and Linux were not built, and no dedicated `--wasm` build was run.
- Alternative stacks, other SDK versions, and third-party integrations were outside the fixture.
- Conversational intake, delegation, conflict, and resumption cases are listed in `tests/behavior.md`; they were not executed in an independent agent evaluation.
- Optional agent-setup scenarios were added to the evaluation guide but not executed in an independent agent evaluation. These changes affect instructions and documentation, not the fixture's Flutter code.

## Distribution updates

The user selected MIT. `LICENSE` and the manifest license field were added; the copyright holder is João Fraga, matching the Git author configuration. Third-party resource licenses remain separate from the skill license.

The repository is now named `flutter-start-skill`. Instructions, references, UI metadata, examples, and evaluation documentation are maintained in English. The installed skill ID and invocation remain `flutter-start` and `$flutter-start`. Translating the repository did not rerun or change the previously verified Flutter fixture; the Flutter results above describe that earlier execution.
