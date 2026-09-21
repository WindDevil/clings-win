/* The built-in editor's front end.
 *
 * Plain JavaScript on purpose: it is loaded from a file (the page's CSP
 * forbids inline script), it holds no build step, and it knows nothing about
 * C.  Everything specific to a language - how to colour it, how to check it,
 * what to offer next - arrives from the server in the language descriptor, so
 * this file is about the *editor*, not about the exercises.
 *
 * The server is the only source of truth.  This code never reads a file from
 * disk, never guesses a path, and never decides whether an answer is right;
 * it asks and displays.
 */
"use strict";

(function () {
  // ------------------------------------------------------------------ dom
  const dom = {};
  for (const id of [
    "progress-fill", "progress-text", "theme-button", "vscode-button", "search",
    "tree", "exercise-title", "exercise-ident", "exercise-topic", "exercise-flags",
    "exercise-objective", "hint-box", "exercise-hint", "readme-box", "readme",
    "tabs", "editor", "editor-placeholder", "save-button", "run-button",
    "check-button", "solution-button", "apply-button", "reset-button",
    "previous-button", "next-button", "status", "output", "output-meta",
    "clear-output", "problems", "problems-meta", "stdin",
  ]) {
    dom[id] = document.getElementById(id);
  }

  const TOKEN = (document.querySelector('meta[name="clings-token"]') || {}).content || "";
  const THEME_KEY = "clings-studio-theme";
  const HINT_AFTER_CLOSE_MS = 400;

  const state = {
    session: null,
    languages: new Map(),
    listing: null,
    exercise: null,
    files: [],
    buffers: new Map(), // path -> {path, doc, saved, revision, editable, languageId, mode, completions}
    active: null,
    filter: "",
    busy: false,
    lastHintClose: 0,
  };

  function currentIdent() {
    return state.exercise ? state.exercise.ident : "";
  }

  function activeBuffer() {
    return state.active ? state.buffers.get(state.active) : null;
  }

  function language(id) {
    return state.languages.get(id) || {id: id, label: id, checks: false, completes: false};
  }

  // ------------------------------------------------------------------- api
  async function api(route, options) {
    const settings = options || {};
    const headers = {"X-Clings-Token": TOKEN};
    let body;
    if (settings.body !== undefined) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(settings.body);
    }
    let response;
    try {
      response = await fetch(route, {method: settings.method || "GET", headers: headers, body: body});
    } catch (error) {
      // The server is gone: the usual cause is the console window being
      // closed, which is worth saying out loud rather than showing "failed".
      throw new Error("连不上内置编辑器服务（窗口可能已经关闭）");
    }
    let payload = null;
    try {
      payload = await response.json();
    } catch (error) {
      payload = null;
    }
    if (!response.ok) {
      const failure = new Error((payload && payload.error) || ("请求失败：" + response.status));
      failure.status = response.status;
      failure.payload = payload;
      throw failure;
    }
    return payload;
  }

  // ----------------------------------------------------------------- theme
  function applyTheme(name) {
    document.body.classList.toggle("dark", name === "dark");
    if (state.editor) {
      state.editor.setOption("theme", name === "dark" ? "material-darker" : "eclipse");
    }
    dom["theme-button"].textContent = name === "dark" ? "浅色" : "深色";
    try {
      window.localStorage.setItem(THEME_KEY, name);
    } catch (error) {
      /* a browser that refuses storage still gets the theme for this session */
    }
  }

  function currentTheme() {
    try {
      return window.localStorage.getItem(THEME_KEY) === "dark" ? "dark" : "light";
    } catch (error) {
      return "light";
    }
  }

  // --------------------------------------------------------- status/output
  function setStatus(text, kind) {
    dom.status.textContent = text || "";
    dom.status.className = "status" + (kind ? " " + kind : "");
    // One line with an ellipsis: the title is where the rest of a long message
    // is still readable.
    dom.status.title = text || "";
  }

  function setBusy(busy, text) {
    state.busy = busy;
    for (const id of ["save-button", "run-button", "check-button", "solution-button",
                      "apply-button", "reset-button", "previous-button", "next-button"]) {
      dom[id].disabled = busy;
    }
    if (text) {
      setStatus(text);
    }
  }

  function showOutput(text, meta, kind) {
    dom.output.textContent = "";
    const lines = String(text || "").split("\n");
    for (const line of lines) {
      const span = document.createElement("span");
      span.className = classify(line, kind);
      span.textContent = line + "\n";
      dom.output.appendChild(span);
    }
    dom["output-meta"].textContent = meta || "";
    dom["output-meta"].className = kind === "bad" ? "muted bad-text" : "muted";
    dom.output.scrollTop = 0;
  }

  function classify(line, kind) {
    if (/^\s*(FAIL|error:|.*error:)/.test(line) || /编译失败|运行超时/.test(line)) {
      return "line-bad";
    }
    if (/^\s*ok\s/.test(line)) {
      return "line-ok";
    }
    if (/warning:|note:|\bwarning\b/.test(line)) {
      return "line-warn";
    }
    if (/^\s*(cc1|collect2|In function|In file included|D:|\/)/.test(line)) {
      return "line-dim";
    }
    return kind === "bad" ? "line-bad" : "";
  }

  // -------------------------------------------------------------- progress
  function renderProgress() {
    const listing = state.listing;
    if (!listing) {
      return;
    }
    const done = listing.completed_count || 0;
    const total = listing.total || 0;
    dom["progress-text"].textContent = done + " / " + total;
    dom["progress-fill"].style.width = total ? (done / total * 100).toFixed(1) + "%" : "0";
    dom["progress-fill"].parentElement.title = "已完成 " + done + " 个，共 " + total + " 个练习";
  }

  async function refreshListing() {
    state.listing = await api("/api/exercises");
    renderProgress();
    renderTree();
  }

  // ------------------------------------------------------------------ tree
  function renderTree() {
    const listing = state.listing;
    if (!listing) {
      return;
    }
    const needle = state.filter.trim().toLowerCase();
    const here = currentIdent();
    dom.tree.textContent = "";
    for (const topic of listing.topics) {
      const items = topic.exercises.filter(function (exercise) {
        if (!needle) {
          return true;
        }
        return (exercise.ident + " " + exercise.title + " " + exercise.slug)
          .toLowerCase()
          .indexOf(needle) >= 0;
      });
      if (!items.length) {
        continue;
      }
      const details = document.createElement("details");
      const done = items.filter(function (item) { return item.completed; }).length;
      details.open = Boolean(needle) || items.some(function (item) { return item.ident === here; });

      const summary = document.createElement("summary");
      summary.appendChild(document.createTextNode(topic.name));
      const count = document.createElement("span");
      count.className = "count";
      count.textContent = done + "/" + items.length;
      summary.appendChild(count);
      details.appendChild(summary);

      const list = document.createElement("ul");
      for (const exercise of items) {
        const li = document.createElement("li");
        const button = document.createElement("button");
        button.className = "tree-item" +
          (exercise.completed ? " done" : "") +
          (exercise.ident === here ? " current" : "");
        const slug = document.createElement("span");
        slug.className = "slug";
        slug.textContent = exercise.slug;
        button.appendChild(slug);
        button.appendChild(document.createTextNode("  " + exercise.title));
        button.title = exercise.ident + " — " + exercise.title;
        button.addEventListener("click", function () {
          openExercise(exercise.ident);
        });
        li.appendChild(button);
        list.appendChild(li);
        if (exercise.ident === here) {
          // Keep the current exercise visible after a re-render.
          window.requestAnimationFrame(function () {
            button.scrollIntoView({block: "nearest"});
          });
        }
      }
      details.appendChild(list);
      dom.tree.appendChild(details);
    }
    if (!dom.tree.childElementCount) {
      const empty = document.createElement("div");
      empty.className = "problem empty";
      empty.textContent = "没有匹配的练习";
      dom.tree.appendChild(empty);
    }
  }

  // -------------------------------------------------------------- exercise
  async function openExercise(ident) {
    if (state.busy || ident === currentIdent()) {
      return;
    }
    if (!(await guardUnsaved())) {
      return;
    }
    setBusy(true, "载入练习…");
    try {
      const route = "/api/exercise/" + ident.split("/").map(encodeURIComponent).join("/");
      const detail = await api(route);
      state.exercise = detail.exercise;
      state.files = detail.files;
      state.buffers.clear();
      renderExerciseHead(detail);
      renderTree();
      renderTabs();
      await openFile(mainFile(detail));
      setStatus("");
      window.history.replaceState(null, "", "#" + ident);
    } catch (error) {
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  function anyDirty() {
    for (const buffer of state.buffers.values()) {
      if (buffer.editable && isDirty(buffer)) {
        return true;
      }
    }
    return false;
  }

  async function guardUnsaved() {
    /* Switching exercises throws the buffers away, so unsaved text has to be
     * dealt with first.  Two answers, not three: confirm() cannot express
     * "cancel", and "save, or lose it" is the choice actually being made. */
    if (!anyDirty()) {
      return true;
    }
    if (!window.confirm("有还没保存的修改。先保存再切换吗？（点“取消”就放弃这些修改）")) {
      return true;
    }
    setBusy(true, "保存中…");
    const ok = await saveAll();
    setBusy(false);
    return ok;
  }

  function mainFile(detail) {
    const files = detail.files || [];
    const source = files.filter(function (file) { return /\.c$/i.test(file.name); })[0];
    return (source || files[0] || {}).path || "";
  }

  function renderExerciseHead(detail) {
    const exercise = detail.exercise;
    dom["exercise-title"].textContent = exercise.title;
    dom["exercise-ident"].textContent = exercise.ident;
    dom["exercise-topic"].textContent = exercise.topic;
    dom["exercise-objective"].textContent = exercise.objective || "";
    dom["exercise-hint"].textContent = exercise.hint || "（这个练习没有提示）";
    dom["hint-box"].hidden = !exercise.hint;

    renderFlags();

    dom["previous-button"].disabled = !detail.previous;
    dom["next-button"].disabled = !detail.next;
    dom["previous-button"].dataset.ident = detail.previous || "";
    dom["next-button"].dataset.ident = detail.next || "";

    renderReadme(detail.topic_readme);
  }

  function renderFlags() {
    const exercise = state.exercise;
    dom["exercise-flags"].textContent = "";
    if (!exercise) {
      return;
    }
    if (exercise.is_project) {
      dom["exercise-flags"].appendChild(badge("多文件项目", "project"));
    }
    if (exercise.completed) {
      dom["exercise-flags"].appendChild(badge("已通过", "ok"));
    }
    if (exercise.reference) {
      dom["exercise-flags"].appendChild(badge(exercise.reference, ""));
    }
  }

  function badge(text, kind) {
    const span = document.createElement("span");
    span.className = "badge" + (kind ? " " + kind : "");
    span.textContent = text;
    return span;
  }

  function renderReadme(readme) {
    const box = dom["readme-box"];
    if (!readme || !readme.exists || !readme.content) {
      box.hidden = true;
      dom.readme.textContent = "";
      return;
    }
    box.hidden = false;
    try {
      window.marked.setOptions({mangle: false, headerIds: false});
      // innerHTML, but the text is the package's own README.md and the page's
      // Content-Security-Policy has no 'unsafe-inline' for scripts, so markup
      // that tried to run would not.
      dom.readme.innerHTML = window.marked.parse(readme.content);
    } catch (error) {
      dom.readme.textContent = readme.content;
    }
  }

  // ------------------------------------------------------------------ tabs
  function renderTabs() {
    dom.tabs.textContent = "";
    const buffer = activeBuffer();
    for (const file of state.files) {
      const known = state.buffers.get(file.path);
      const dirty = known ? isDirty(known) : false;
      const button = document.createElement("button");
      button.className = "tab" + (file.path === state.active ? " current" : "") +
        (dirty ? " dirty" : "") + (file.editable ? "" : " readonly");
      button.textContent = file.name + (file.editable ? "" : "（只读）");
      button.title = file.path;
      button.addEventListener("click", function () {
        if (file.path !== state.active) {
          openFile(file.path);
        }
      });
      dom.tabs.appendChild(button);
    }
  }

  function isDirty(buffer) {
    return buffer.doc.getValue() !== buffer.saved;
  }

  async function openFile(path) {
    if (!path) {
      return;
    }
    let buffer = state.buffers.get(path);
    if (!buffer) {
      const file = await api("/api/file?path=" + encodeURIComponent(path));
      const descriptor = language(file.language_id);
      buffer = {
        path: file.path,
        doc: CodeMirror.Doc(file.content, descriptor.editor_mode || "text/plain"),
        saved: file.content,
        revision: file.revision,
        editable: file.editable,
        languageId: file.language_id,
        completions: [],
      };
      state.buffers.set(path, buffer);
    }
    state.active = path;
    state.editor.swapDoc(buffer.doc);
    state.editor.setOption("tabSize", language(buffer.languageId).tab_size || 4);
    state.editor.setOption("indentUnit", language(buffer.languageId).tab_size || 4);
    // The lint option is per editor, and swapping the doc clears its marks;
    // re-setting it starts a fresh check on the text now in the editor.
    configureLint();
    dom["editor-placeholder"].hidden = true;
    renderTabs();
    setStatus("");
    renderProblems([]);
    prefetchCompletions(buffer).then(function () {}, function () {});
    state.editor.focus();
  }

  // ---------------------------------------------------------------- editor
  function createEditor() {
    return CodeMirror(dom.editor, {
      value: "",
      mode: "text/plain",
      theme: currentTheme() === "dark" ? "material-darker" : "eclipse",
      lineNumbers: true,
      lineWrapping: false,
      matchBrackets: true,
      autoCloseBrackets: true,
      styleActiveLine: true,
      foldGutter: true,
      gutters: ["CodeMirror-lint-markers", "CodeMirror-foldgutter"],
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      extraKeys: {
        // Tab indents instead of leaving the editor, which is what a learner
        // pressing Tab inside a function body means.
        Tab: function (cm) { cm.execCommand("insertTab"); },
        "Shift-Tab": function (cm) { cm.execCommand("indentLess"); },
        "Alt-F": "findPersistent",
      },
    });
  }

  function configureLint() {
    const buffer = activeBuffer();
    if (!buffer || !language(buffer.languageId).checks) {
      state.editor.setOption("lint", false);
      return;
    }
    state.editor.setOption("lint", {
      async: true,
      delay: 700,
      lintOnChange: true,
      tooltips: true,
      highlightLines: true,
      getAnnotations: function (text, callback) {
        checkText(buffer.path, text).then(function (diagnostics) {
          renderProblems(diagnostics);
          callback(diagnostics.map(toAnnotation));
        }, function (error) {
          renderProblems([]);
          callback([{
            from: CodeMirror.Pos(0, 0),
            to: CodeMirror.Pos(0, 1),
            severity: "info",
            message: error.message,
          }]);
        });
      },
    });
  }

  function toAnnotation(diagnostic) {
    const line = Math.max(0, (diagnostic.line || 1) - 1);
    const column = Math.max(0, (diagnostic.column || 1) - 1);
    const text = state.editor.getLine(line) || "";
    // Underline the whole word when the compiler pointed at an identifier:
    // one marked character is hard to see, and the token is what is wrong.
    let end = column + 1;
    if (/[A-Za-z0-9_]/.test(text.charAt(column) || "")) {
      while (end < text.length && /[A-Za-z0-9_]/.test(text.charAt(end))) {
        end++;
      }
    }
    return {
      from: CodeMirror.Pos(line, column),
      to: CodeMirror.Pos(line, Math.max(end, column + 1)),
      severity: diagnostic.severity === "warning" ? "warning"
        : diagnostic.severity === "error" ? "error" : "info",
      message: diagnostic.message,
    };
  }

  async function checkText(path, text) {
    const payload = await api("/api/check", {method: "POST", body: {path: path, content: text}});
    return payload.diagnostics || [];
  }

  function renderProblems(diagnostics) {
    dom.problems.textContent = "";
    dom["problems-meta"].textContent = diagnostics.length
      ? diagnostics.length + " 条"
      : "没有发现问题";
    if (!diagnostics.length) {
      const empty = document.createElement("div");
      empty.className = "problem empty";
      empty.textContent = activeBuffer() && language(activeBuffer().languageId).checks
        ? "编译器没有报错。点“运行”看测试结果。"
        : "这个文件没有语法检查。";
      dom.problems.appendChild(empty);
      return;
    }
    for (const diagnostic of diagnostics) {
      const row = document.createElement("div");
      row.className = "problem " + (diagnostic.severity || "error");
      const where = document.createElement("div");
      where.className = "where";
      const own = !diagnostic.file || diagnostic.file === state.active;
      where.textContent = own
        ? (diagnostic.line || 1) + ":" + (diagnostic.column || 1)
        : shortName(diagnostic.file) + ":" + (diagnostic.line || 1);
      const what = document.createElement("div");
      what.className = "what";
      what.appendChild(document.createTextNode(diagnostic.message));
      if (diagnostic.code) {
        const code = document.createElement("span");
        code.className = "code";
        code.textContent = " " + diagnostic.code;
        what.appendChild(code);
      }
      if (diagnostic.context && own) {
        const context = document.createElement("span");
        context.className = "context";
        context.textContent = diagnostic.context;
        what.appendChild(context);
      }
      row.appendChild(where);
      row.appendChild(what);
      row.addEventListener("click", function () {
        goTo(diagnostic);
      });
      dom.problems.appendChild(row);
    }
  }

  function shortName(path) {
    const parts = String(path).split("/");
    return parts[parts.length - 1];
  }

  function goTo(diagnostic) {
    if (diagnostic.file && diagnostic.file !== state.active) {
      const file = state.files.filter(function (item) { return item.path === diagnostic.file; })[0];
      if (!file) {
        setStatus("这个错误在 " + diagnostic.file + "，它不属于当前练习的文件", "bad");
        return;
      }
      openFile(file.path).then(function () {
        placeCursor(diagnostic);
      });
      return;
    }
    placeCursor(diagnostic);
  }

  function placeCursor(diagnostic) {
    const line = Math.max(0, (diagnostic.line || 1) - 1);
    const column = Math.max(0, (diagnostic.column || 1) - 1);
    state.editor.setCursor({line: line, ch: column});
    state.editor.scrollIntoView({line: line, ch: column}, 80);
    state.editor.focus();
  }

  // ------------------------------------------------------------ completion
  function wordBefore() {
    const cursor = state.editor.getCursor();
    const line = state.editor.getLine(cursor.line) || "";
    const before = line.slice(0, cursor.ch);
    const match = /[A-Za-z_][A-Za-z0-9_]*$/.exec(before);
    return match ? match[0] : "";
  }

  async function prefetchCompletions(buffer) {
    if (!language(buffer.languageId).completes) {
      buffer.completions = [];
      return buffer.completions;
    }
    const payload = await api("/api/completion", {
      method: "POST",
      body: {path: buffer.path, content: buffer.doc.getValue()},
    });
    buffer.completions = payload.items || [];
    return buffer.completions;
  }

  const KIND_ORDER = ["function", "type", "macro", "keyword", "snippet"];

  function showCompletions(force) {
    const buffer = activeBuffer();
    if (!buffer || !language(buffer.languageId).completes) {
      return;
    }
    const prefix = wordBefore();
    const editor = state.editor;
    const cursor = editor.getCursor();
    const from = CodeMirror.Pos(cursor.line, cursor.ch - prefix.length);
    const items = filterCompletions(buffer.completions, prefix);
    if (!items.length) {
      if (force) {
        setStatus("没有匹配的补全（提示来自 C 标准库和这个练习自己声明的名字）", "");
      }
      return;
    }
    if (items.length === 1 && items[0].label === prefix) {
      return; // the only match is what is already typed
    }
    editor.showHint({
      hint: function () {
        return {list: items, from: from, to: cursor};
      },
      completeSingle: false,
      alignWithWord: false,
      closeOnUnfocus: true,
    });
  }

  function filterCompletions(all, prefix) {
    const lower = prefix.toLowerCase();
    const matched = [];
    for (const item of all) {
      if (item.label.toLowerCase().indexOf(lower) === 0) {
        matched.push(item);
      }
    }
    matched.sort(function (left, right) {
      const exact = (left.label.toLowerCase() === lower ? 0 : 1) -
        (right.label.toLowerCase() === lower ? 0 : 1);
      if (exact) {
        return exact;
      }
      const kind = KIND_ORDER.indexOf(left.kind) - KIND_ORDER.indexOf(right.kind);
      if (kind) {
        return kind;
      }
      return left.label.length - right.label.length || left.label.localeCompare(right.label);
    });
    return matched.slice(0, 150).map(function (item) {
      return {
        text: item.insert || item.label,
        displayText: item.label,
        className: "clings-hint clings-hint-" + item.kind,
        render: function (element) {
          element.appendChild(document.createTextNode(item.label));
          if (item.detail) {
            const detail = document.createElement("span");
            detail.className = "hint-detail";
            detail.textContent = item.header ? item.detail + "  " + item.header : item.detail;
            element.appendChild(detail);
          }
        },
      };
    });
  }

  // ------------------------------------------------------------- actions
  async function saveBuffer(buffer) {
    if (!buffer.editable) {
      return true;
    }
    if (!isDirty(buffer)) {
      return true;
    }
    const text = buffer.doc.getValue();
    try {
      const payload = await api("/api/file", {
        method: "PUT",
        body: {path: buffer.path, content: text, base_revision: buffer.revision},
      });
      buffer.saved = text;
      buffer.revision = payload.revision;
      renderTabs();
      return true;
    } catch (error) {
      if (error.status === 409) {
        const reload = window.confirm(
          error.message + "\n\n载入磁盘上的版本吗？（你的修改会丢失）"
        );
        if (reload) {
          const file = await api("/api/file?path=" + encodeURIComponent(buffer.path));
          buffer.doc.setValue(file.content);
          buffer.saved = file.content;
          buffer.revision = file.revision;
          renderTabs();
          return true;
        }
        return false;
      }
      setStatus(error.message, "bad");
      return false;
    }
  }

  async function save() {
    const buffer = activeBuffer();
    if (!buffer) {
      return false;
    }
    setBusy(true, "保存中…");
    const ok = await saveBuffer(buffer);
    if (ok) {
      setStatus("已保存 " + shortName(buffer.path) + "  " + new Date().toLocaleTimeString(), "ok");
      prefetchCompletions(buffer).then(function () {}, function () {});
    }
    setBusy(false);
    return ok;
  }

  async function saveAll() {
    for (const buffer of state.buffers.values()) {
      if (!(await saveBuffer(buffer))) {
        return false;
      }
    }
    return true;
  }

  async function check() {
    const buffer = activeBuffer();
    if (!buffer) {
      return;
    }
    if (!language(buffer.languageId).checks) {
      setStatus("这个文件没有语法检查", "");
      renderProblems([]);
      return;
    }
    setBusy(true, "检查中…");
    try {
      const diagnostics = await checkText(buffer.path, buffer.doc.getValue());
      renderProblems(diagnostics);
      setStatus(diagnostics.length ? "编译器报了 " + diagnostics.length + " 条" : "没有发现问题",
        diagnostics.length ? "bad" : "ok");
    } catch (error) {
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  async function run() {
    if (!state.exercise) {
      return;
    }
    setBusy(true, "运行中…");
    try {
      // Run what is on disk: the runner compiles the file, not the buffer, so
      // an unsaved edit would be silently left out of the run.
      if (!(await saveAll())) {
        setBusy(false);
        return;
      }
      const payload = await api("/api/run", {
        method: "POST",
        body: {ident: state.exercise.ident, stdin: dom.stdin.value},
      });
      const result = payload.result;
      showOutput(result.output || "（没有输出）",
        result.stage_label + (result.passed ? "" : " · " + state.exercise.ident),
        result.passed ? "ok" : "bad");
      if (payload.diagnostics && payload.diagnostics.length) {
        renderProblems(payload.diagnostics);
      }
      setStatus(result.passed ? "全部通过" : result.stage_label, result.passed ? "ok" : "bad");
      // The runner is the authority on whether the exercise is now finished,
      // so take the flag back from a fresh listing rather than assuming a pass
      // was recorded (it is not, for an exercise already done).
      await refreshListing();
      const fresh = findExercise(state.listing, state.exercise.ident);
      if (fresh) {
        state.exercise.completed = fresh.completed;
      }
      renderFlags();
    } catch (error) {
      showOutput(error.message, "运行失败", "bad");
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  function findExercise(listing, ident) {
    if (!listing) {
      return null;
    }
    for (const topic of listing.topics) {
      for (const exercise of topic.exercises) {
        if (exercise.ident === ident) {
          return exercise;
        }
      }
    }
    return null;
  }

  async function showSolution() {
    if (!state.exercise) {
      return;
    }
    setBusy(true, "读取参考答案…");
    try {
      const payload = await api("/api/solution", {
        method: "POST",
        body: {ident: state.exercise.ident},
      });
      showOutput(payload.text, "参考答案（没有写入你的文件）", "");
      setStatus("参考答案显示在下面，需要的话点“套用参考实现”", "");
    } catch (error) {
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  async function applySolution() {
    if (!state.exercise) {
      return;
    }
    if (!window.confirm("用参考答案覆盖 " + state.exercise.ident + " 的文件？你的修改会丢失。")) {
      return;
    }
    setBusy(true, "套用中…");
    try {
      await api("/api/solution", {method: "POST", body: {ident: state.exercise.ident, apply: true}});
      await reloadFiles();
      await refreshListing();
      setStatus("已套用参考答案，别忘了自己读一遍", "ok");
    } catch (error) {
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  async function resetExercise() {
    if (!state.exercise) {
      return;
    }
    if (!window.confirm("把 " + state.exercise.ident + " 恢复成初始内容？你的修改会丢失。")) {
      return;
    }
    setBusy(true, "重置中…");
    try {
      const payload = await api("/api/reset", {method: "POST", body: {ident: state.exercise.ident}});
      await reloadFiles();
      await refreshListing();
      setStatus("已重置", "ok");
      if (payload.output) {
        showOutput(payload.output, "重置", "");
      }
    } catch (error) {
      setStatus(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  async function reloadFiles() {
    const open = state.active;
    for (const file of state.files) {
      const buffer = state.buffers.get(file.path);
      if (!buffer) {
        continue;
      }
      const payload = await api("/api/file?path=" + encodeURIComponent(file.path));
      buffer.doc.setValue(payload.content);
      buffer.saved = payload.content;
      buffer.revision = payload.revision;
      buffer.completions = [];
    }
    renderTabs();
    if (open && state.buffers.has(open)) {
      state.active = open;
      state.editor.swapDoc(state.buffers.get(open).doc);
      configureLint();
    }
  }

  async function openInVscode() {
    if (!state.exercise) {
      return;
    }
    setBusy(true, "打开 VS Code…");
    try {
      const payload = await api("/api/open-vscode", {
        method: "POST",
        body: {ident: state.exercise.ident},
      });
      setStatus("已在 VS Code 中打开 " + payload.path, "ok");
    } catch (error) {
      setStatus(error.message.split("\n")[0], "bad");
      showOutput(error.message, "VS Code", "bad");
    } finally {
      setBusy(false);
    }
  }

  function goToExercise(button) {
    const ident = button.dataset.ident;
    if (ident) {
      openExercise(ident);
    }
  }

  // ------------------------------------------------------------------ boot
  async function boot() {
    applyTheme(currentTheme());
    state.editor = createEditor();

    state.editor.on("change", function () {
      const buffer = activeBuffer();
      if (buffer) {
        const wasDirty = dom.tabs.querySelector(".tab.current.dirty") !== null;
        const dirty = isDirty(buffer);
        if (dirty !== wasDirty) {
          renderTabs();
        }
      }
      setStatus("");
    });
    state.editor.on("endCompletion", function () {
      state.lastHintClose = Date.now();
    });
    state.editor.on("inputRead", function (editor, change) {
      if (change.origin !== "+input") {
        return;
      }
      if (!/^[A-Za-z_]$/.test(change.text.join(""))) {
        return;
      }
      if (Date.now() - state.lastHintClose < HINT_AFTER_CLOSE_MS) {
        return;
      }
      if (wordBefore().length < 2) {
        return;
      }
      showCompletions(false);
    });

    dom["theme-button"].addEventListener("click", function () {
      applyTheme(document.body.classList.contains("dark") ? "light" : "dark");
    });
    dom["vscode-button"].addEventListener("click", openInVscode);
    dom["save-button"].addEventListener("click", save);
    dom["run-button"].addEventListener("click", run);
    dom["check-button"].addEventListener("click", check);
    dom["solution-button"].addEventListener("click", showSolution);
    dom["apply-button"].addEventListener("click", applySolution);
    dom["reset-button"].addEventListener("click", resetExercise);
    dom["clear-output"].addEventListener("click", function () {
      showOutput("", "", "");
    });
    dom["previous-button"].addEventListener("click", function () { goToExercise(this); });
    dom["next-button"].addEventListener("click", function () { goToExercise(this); });
    dom.search.addEventListener("input", function () {
      state.filter = dom.search.value;
      renderTree();
    });

    window.addEventListener("keydown", function (event) {
      if (!(event.ctrlKey || event.metaKey)) {
        return;
      }
      if (event.key === "s") {
        event.preventDefault();
        save();
      } else if (event.key === "Enter") {
        event.preventDefault();
        run();
      } else if (event.key === " ") {
        event.preventDefault();
        showCompletions(true);
      }
    });
    window.addEventListener("beforeunload", function (event) {
      for (const buffer of state.buffers.values()) {
        if (buffer.editable && isDirty(buffer)) {
          event.preventDefault();
          event.returnValue = "";
          return "";
        }
      }
      return undefined;
    });

    try {
      state.session = await api("/api/session");
      for (const descriptor of state.session.languages) {
        state.languages.set(descriptor.id, descriptor);
      }
      if (!state.session.toolchain.compiler_found) {
        setStatus("没有找到编译器 " + state.session.toolchain.compiler +
          "，先运行 .\\clings.cmd doctor 看看工具链", "bad");
      }
      state.listing = await api("/api/exercises");
      renderProgress();
      renderTree();

      const fromHash = decodeURIComponent(window.location.hash.replace(/^#/, ""));
      const wanted = fromHash || state.listing.next;
      if (wanted) {
        await openExercise(wanted);
      } else {
        const total = state.session.total || state.listing.total || 0;
        dom["exercise-title"].textContent = "所有练习都完成了";
        dom["exercise-objective"].textContent = total + " 个都通过了。想重做的话，从左边的列表里挑一个。";
      }
    } catch (error) {
      setStatus(error.message, "bad");
      showOutput(error.message, "启动失败", "bad");
    }
  }

  boot();
})();
