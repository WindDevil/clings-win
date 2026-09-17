# Vendored components

Third-party code that ships inside the package, kept as-is so the built-in
editor works with no network and no npm. Each one keeps its licence next to
it, and each is pinned to an exact version.

| Component | Version | Licence | Source | Used for |
| --- | --- | --- | --- | --- |
| CodeMirror | 5.65.16 | MIT | <https://codemirror.net/5/> | the editor, C syntax highlighting, lint gutter, hint popup, search, folding, themes |
| marked | 4.3.0 | MIT | <https://marked.js.org/> | rendering the topic `README.md` next to the exercise |

Only the files the editor actually loads are vendored - `lib/codemirror.js` and
`lib/codemirror.css`, the `clike` mode (which covers C), the addons listed in
`index.html`, and two themes (`eclipse` for light, `material-darker` for dark).
The npm packages carry many more modes, addons and themes; they are not here.

To update: download the same paths from a newer release, replace the files,
update the version numbers above, and change the pin in `docs/portability.md`
if it is mentioned there. Nothing in the studio reads a version number at
runtime, so a mismatch shows up as a missing file or a JavaScript error, not as
a subtle wrong answer.
