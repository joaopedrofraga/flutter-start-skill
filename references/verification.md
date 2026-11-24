# Verification and delivery evidence

Read after implementing the foundation. Verify the generated project; validating the skill's Markdown does not prove an application works.

## Basic sequence

Use the Flutter/Dart executable matching the chosen version, including the project's wrapper when applicable. Run from the app directory:

```text
flutter pub get
dart format lib test
flutter analyze
flutter test
```

When localization files are generated, also run the SDK-compatible generator and check imports. Keep the application's `pubspec.lock`. Do not require dependency updates simply because the resolver reports newer versions.

## Behaviors requiring evidence

| Area | Useful verification |
| --- | --- |
| Entry point | Mount the root widget, resolve the initial route, and check the display name. |
| Theme | Render selected modes and check brightness and brand colors that must be exact. When following the system, verify response to system brightness changes. |
| Form | An invalid field displays a message and prevents the action; a valid value allows the demonstrated local interaction. |
| Button | The enabled callback works; disabled/loading states do not fire it; progress has an accessibility label. |
| Field | Validator and controller work; unmounting the wrapper does not dispose of a caller-owned controller. |
| Layout | A narrow screen and enlarged text do not overflow. Check focus/keyboard behavior when introduced by a custom widget. |
| Languages | Delegates and locales match the choice. For multiple languages, change locale and observe application text changing as well as SDK components. |
| Configuration | The default mode starts without an API when none was chosen. Invalid required configuration produces a clear error before use. |
| Resources | Every declared asset/font exists; weights and styles match actual files. Check licenses of third-party resources. |
| Platform identity | Check selected platforms' metadata and CLI-generated identifiers. |
| Agent setup | Compare created files with the selected mode. Without setup: no new AI files/folders, skills, memory, or `docs/bootstrap.md`. With setup: agreed artifacts only. Do not require preexisting agent files to be absent or delete them to pass the check. |

Filenames and directory existence do not replace behavior tests. Do not add tests for business features outside the request.

## Builds

Choose at least one requested target supported by the environment. Examples must be confirmed with `flutter build <target> --help`:

| Platform | Example check | Requirement |
| --- | --- | --- |
| Android | `flutter build apk --debug` | Available Android SDK and compatible tools. |
| iOS | `flutter build ios --no-codesign` | macOS and compatible Xcode; does not prove signing/distribution. |
| Web | `flutter build web` | Web included in intake. |
| Windows | `flutter build windows` | Windows and the toolchain required by the SDK. |
| macOS | `flutter build macos` | macOS and compatible Xcode. |
| Linux | `flutter build linux` | Linux and native dependencies required by the SDK. |

Do not install a platform toolchain, add a target, or change the SDK version merely to obtain a build. Distinguish scaffold failures from environment limitations and report the actual diagnosis. An infrastructure failure does not authorize omitting that target from the report.

Investigate font/asset/import warnings: determine whether they originate in generated code, dependencies, or resources used by the app. Do not claim a missing resource is integrated merely because compilation succeeded. Do not remove checks or use flags to hide the problem.

A successful build does not prove visual execution. If a device/browser is available and running the app is within the request/authorization, open it and check the initial screen. Otherwise, state that visual execution was not performed.

## Records and handoff

In both modes, update the technical README with concrete commands and guidance for starting development. If `docs/bootstrap.md` was included in the accepted agent setup, record the following there. Otherwise, present the summary in chat without creating a context file for convenience:

1. Resolved intake and delegated decisions.
2. Actual Flutter and Dart versions used.
3. Organization and locations for changing themes, widgets, configuration, and routes.
4. Run command with the target and required public definitions.
5. Verification commands with actual results: passed, failed, or not run with a reason.
6. Generated platforms and which ones were built or run.
7. First extension point for implementing an actual feature.
8. Chosen delivery mode and any agent files created.

The README must let someone run the foundation without reading conversation history. Remove template instructions that contradict the generated project.

If blocked, deliver the partial state with files preserved and a precise next step. Describe the foundation as ready only when no required infrastructure implementation remains and applicable checks have passed.
