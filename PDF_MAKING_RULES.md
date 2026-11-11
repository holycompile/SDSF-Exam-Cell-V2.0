# PDF & Handbook Authoring Rules Reference
**Project:** SDSF Exam Cell Automation System V2.0  
**Lead Developer & Reference:** Joyobrata Das  
**Institution:** School of Data Science and Forecasting (SDSF), DAVV, Indore  
**Document Targets:** `handbook.html` & `FLASK_BACKEND_DEVELOPER_GUIDE.pdf`

---

## 1. Zero-Deletion / Cumulative Growth Rule
* **Never Delete Existing Content:** Under no circumstances should existing modules, explanations, code blocks, or tables be removed or shortened during updates.
* **Continuous Expansion:** Each update must append, enrich, or refine. New concepts must increase document depth and page count (e.g., from 12 $\rightarrow$ 13 $\rightarrow$ 17 $\rightarrow$ 19+ pages).
* **Historical Preservation:** Earlier architectural decisions and code patterns remain documented so the reader can compare legacy approaches against modern best practices.

---

## 2. Granular Hierarchical Structure (Submodules)
* **Numbered Submodules:** Structure every high-level module into granular submodules (e.g., under Module 7: `7.1`, `7.2`, `7.3`, `7.4`, `7.5`, `7.6`...).
* **Isolation of Small Details:** Even minor coding tips (e.g., SQL writing styles, comment tags like `--sql`, IDE extensions, cursor closing mechanics) must have their own designated submodule header (`h3` or `h4`) and anchor ID (e.g., `id="sub7-3"`).
* **Page Break Discipline:** Strategic use of `<div class="page-break"></div>` ensures major modules or large reference tables start on fresh pages without awkward half-table page splits.

---

## 3. Interactive Table of Contents (TOC) Mandate
* **Complete Indexing:** Every single submodule (e.g., `1.1`, `1.2`, `2.1`, `7.1`, `7.2`, `7.3`...) must be explicitly listed in the Table of Contents at the start of the document.
* **Direct Jump Links:** Every TOC entry must use anchor hyperlinks (`<a href="#sub7-3">`) mapped to corresponding element IDs (`<h3 id="sub7-3">`) so readers can click anywhere in the PDF/browser to jump straight to the needed topic.

---

## 4. Exhaustive Variations & Edge Case Coverage
* **No Half-Answers:** When introducing any function, method, or architectural technique (e.g., cursor fetch methods, query formatting, authentication checks), document **all related variations** and counterparts.
  * *Example:* If explaining `cursor.fetchone()`, must also document `cursor.fetchall()`, `cursor.fetchmany()`, `cursor.rowcount`, `cursor.lastrowid`, and `cursor.executemany()`.
* **Explicit Return Types:** For every method, explicitly table and describe:
  1. What it returns when matching data is found (e.g., single `dict`, `list` of `dict`s, integer).
  2. What it returns when no records match or an operation is empty (e.g., `None`, `[]`, `0`).
* **Writing Styles & Syntax Variants:** Document all stylistic patterns used in the industry (e.g., Pattern A: Separate variable, Pattern B: Inline multi-line, Pattern C: `--sql` IDE tag, Pattern D: `f"""--sql"""` injection hazards).

---

## 5. Autonomous & Proactive Inclusion (Zero-Hesitation Mandate)
* **Proactive Option Expansion:** Whenever documenting a topic or answering a query, the assistant is **explicitly authorized and required to add all relevant variations, alternative patterns, edge cases, and industry options without any hesitation**.
* **Do Not Wait for Explicit Requests:** If a concept has multiple valid approaches (e.g., connection pooling vs direct connection, raw SQL vs ORM, session cookies vs JWT, different cursor types like `DictCursor` vs `SSCursor`), proactively add them under the corresponding submodule.
* **No Artificial Brevity in Documentation:** Never withhold technical depth or avoid adding useful sections out of concern for PDF length. The handbook is intended to be a thorough, exhaustive, master-level engineering reference.
* **Structured Comparison:** When adding multiple variations, always explain:
  1. What each variation is and how it works.
  2. When to choose one over another (pros & cons).
  3. Real code snippets illustrating each variant clearly.

---

## 6. Security & Defensive Programming Focus
* **Vulnerability Warnings:** Always contrast clean practices against security vulnerabilities (e.g., highlighting why Python f-string interpolation leads to SQL Injection, while parameterized queries `%s` guarantee safety).
* **Visual Callout Boxes:** Use distinct callouts:
  * `.callout-danger`: Critical security alerts (SQL injection, credential leaks).
  * `.callout-warning`: Architecture traps (package name collisions, missing `override=True`).
  * `.callout-success`: Production-grade patterns and recommended solutions.

---

## 7. Proactive Update & Notification Lifecycle
* **Automatic Detection:** Whenever a new concept, pattern, question, or architectural solution is discussed or finalized in the development session, proactively incorporate it into `handbook.html`.
* **Immediate Re-compilation:** Immediately compile the HTML into `FLASK_BACKEND_DEVELOPER_GUIDE.pdf` using headless Microsoft Edge:
  ```powershell
  $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
  $out = (Resolve-Path .).Path + "\FLASK_BACKEND_DEVELOPER_GUIDE.pdf"
  $in = (Resolve-Path "handbook.html").Path
  Start-Process -FilePath $edge -ArgumentList "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf=`"$out`"", "`"$in`"" -Wait
  ```
* **User Notification:** Always inform the user upon updating, stating clearly what was added, which submodule it lives under, and the current page count.

---

## 8. Scope Boundaries & Technical Purity
* **Backend Focus Only:** Keep the handbook strictly focused on Flask backend architecture, WSGI lifecycles, Jinja2 inheritance, Blueprints, Form handling, DB CRUD, authentication, and security. Avoid unrelated CSS/Tailwind bloat.
* **Formal Attribution & Notice:** Preserve the legal notice referencing the Information Technology Act, 2000, university disciplinary regulations, and lead developer credit (Joyobrata Das, SDSF DAVV).
* **Strict Project Constraints:** Never execute unprompted remote commands (`git push`, `git commit`, or direct database alterations) during the documentation workflow.

