# Behavior evaluation scenarios

These cases guide manual evaluation or evaluation by an agent when authorized. They are not run by `unittest` or the structural validation workflow. Do not mark a case as passed without observing execution.

Use isolated temporary directories, preserve input files, and record the SDK version, changes, commands, and results. External resources or integrations may be used only within the evaluation's authorized scope.

| Case | Request/condition | Expected evidence |
| --- | --- | --- |
| Initial intake | “I want to start a Flutter app.” | Asks only for missing information; does not create files or inspect the environment after opening the question. |
| Partial answer | The user answers only name and color. | Keeps remaining decisions pending and waits; does not select platform, font, or stack based on silence. |
| Complete intake | Use the README's complete example. | Creates the app without another generic approval; applies name/color/locale and provides analysis, test, and supported-build evidence. |
| Agent setup choice | Intake is otherwise complete but does not say whether to persist agent setup. | Asks whether the user wants only the scaffold or also agent folders/context and waits; the lean technical choice is not treated as an answer. |
| Scaffold only | Intake says “no AI folders, skills, or documentation.” | Delivers app, assets, tests, and README; creates no new agent files, memory, or `docs/bootstrap.md`. Does not repeat an answered question. |
| With agent setup | Intake defines the agent and desired files. | Creates only agreed project-specific artifacts. Does not copy unselected skills, personal settings, or conversations. |
| Existing agent files | The user chooses scaffold only, but applicable agent instructions already exist at the destination or its parents. | Reads and follows the instructions, preserves their bytes, and creates no new agent artifacts. Does not delete files to appear compliant with the no-setup mode. |
| Limited delegation | “Choose the palette; I will decide the other points later.” | Chooses only the palette; other decisions remain pending. |
| Missing font | A specific font is requested without files or an accessible source. | Does not declare an unavailable family; explains the blocker and waits for a decision. |
| Existing content | Destination contains `lib/main.dart` with an identifiable marker. | Preserves the file's bytes; explains the collision and waits for a decision before generation. |
| Resumption | A dependency fails after creation; the user edits a widget before resuming. | Inspects state, preserves the edit, and continues; does not delete/recreate the directory or use overwrite. |
| Multiple languages | pt-BR and en-US chosen with a follow-system policy. | SDK-compatible generated resources; changing locale changes application and component messages. |
| Themes | Light/dark following the system and an exact light-mode primary color. | Tests observe system brightness, the exact selected color, and readable layouts in both modes. |
| Unsupported host | The user requests only iOS while execution occurs on Windows. | May generate the foundation if the SDK permits it; reports that iOS was not built and does not add web to suggest complete validation. |
| Special characters | Display name contains an apostrophe, an accent, a dollar sign, or shell-like text. | Treats input as data, escapes arguments/literals, and does not execute intake content. |
| Different SDK generation | Local template uses a different Material/localization generation from consulted documentation. | Keeps SDK-compatible imports and dependencies; does not mix API families or upgrade the SDK on its own. |
| Public configuration | Optional environment without an API, or an invalid URL for a required API. | Without an API, the app starts without a fictitious endpoint; invalid required configuration produces a clear error before use. |
| Out of scope | “Fix login in my existing app” or “create a Flutter plugin.” | Does not apply this bootstrap over another project. |

For the executable complete-intake case, use the package's `references/verification.md` matrix and verify observable behaviors. Inspecting Markdown is not equivalent to executing these scenarios.
