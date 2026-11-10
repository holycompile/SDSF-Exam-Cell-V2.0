# Database Architecture & Development Workflow Guide (TiDB Cloud + Flask)

This guide documents the design philosophy, step-by-step development process, and common questions and answers (Q&A) regarding database management for the **SDSF Exam Cell** project.

---

## 1. Directory Structure & File Roles

Inside your project, database files are organized cleanly in the `databases/` folder:

```text
SDSF-Exam-Cell-V2.0/
│
├── databases/
│   ├── schema.sql         <-- [Blueprint] Holds all CREATE TABLE IF NOT EXISTS queries.
│   ├── connections.py    <-- [Bridge] Manages SSL connection to TiDB Cloud using .env.
│   ├── init_db.py         <-- [Installer] Reads schema.sql & creates tables in TiDB. Run manually!
│   └── queries.py         <-- [Operations] Holds SELECT, INSERT, UPDATE queries used at runtime.
│
├── templates/             <-- HTML views (Jinja2) for the tables and UI.
├── app.py                 <-- Flask web server routing user requests.
├── .env                   <-- Sensitive credentials (TIDB_HOST, USERNAME, PASSWORD, etc.).
└── DATABASE_WORKFLOW_GUIDE.md
```

---

## 2. The 3-Step Lifecycle

```text
Step 1: DEFINE (In schema.sql)
        Write standard `CREATE TABLE IF NOT EXISTS` definitions.

Step 2: INITIALIZE (Run init_db.py once in terminal)
        Command: python databases/init_db.py
        Effect: Tables are created/verified in TiDB Cloud.

Step 3: RUN (Run Flask app.py)
        Command: python app.py
        Effect: Web app runs, using queries.py to read and write rows.
        (init_db.py and schema.sql are NEVER touched during app runtime!)
```

---

## 3. Frequently Asked Questions (Q&A)

### Q1: Why not just type the SQL queries directly into the TiDB Cloud Web Console?
**Answer:** 
Typing directly into a web console creates **"database drift"**—your codebase has no record of how the database was built.
* If your cluster ever resets, you switch databases, or a teammate clones your project, you would have to manually re-type everything from memory.
* Keeping `schema.sql` inside the project ensures **reproducibility and version control** in Git.

---

### Q2: When I run `python app.py`, will `init_db.py` execute every time?
**Answer: ZERO times.**
* `app.py` has no reference or import to `init_db.py`.
* `app.py` only starts the Flask web server.
* `init_db.py` runs **only when you explicitly type `python databases/init_db.py`** in your command prompt.

---

### Q3: Won't running `init_db.py` overwrite or wipe out existing data in TiDB Cloud?
**Answer: No, your data is 100% safe.**
There is a fundamental difference in SQL:
* ❌ **Destructive (Dangerous):**
  `DROP TABLE IF EXISTS teachers;` *(This deletes the table and wipes all rows)*
* 🛡️ **Safe (What we use):**
  `CREATE TABLE IF NOT EXISTS teachers (...);`

When using `IF NOT EXISTS`:
* If the table does not exist: TiDB creates it.
* If the table already exists: TiDB simply **ignores the command and does nothing**. Existing data rows are untouched.

---

### Q4: What if some tables are created and one fails due to a typo?
**Answer: No problem at all.**
1. Tables before the typo get created.
2. The script stops and displays the exact SQL error.
3. You fix the typo in `schema.sql`.
4. You run `python databases/init_db.py` again.
5. TiDB skips all the tables that already exist and creates the missing ones.

---

### Q5: How do I add a new table in the future without breaking anything?
**Answer:**
1. Open `databases/schema.sql` and append your new table:
   ```sql
   CREATE TABLE IF NOT EXISTS new_feature_table (
       id INT AUTO_INCREMENT PRIMARY KEY,
       ...
   );
   ```
2. Run `python databases/init_db.py` in your terminal.
3. TiDB sees the previous 6 tables already exist (skips them) and creates only `new_feature_table`.
4. Run `python app.py`—your app can immediately start inserting into the new table.

---

### Q6: Why did TiDB give the `(1105, 'Missing user name prefix')` error on Windows?
**Answer:**
* Windows has a built-in operating system variable named `USERNAME` (set to your Windows profile name, e.g., `User`).
* Standard `load_dotenv()` does not overwrite existing OS environment variables by default, so Python was sending `User` instead of your TiDB Cloud username (`<prefix>.root`).
* **Fix Applied:** In `databases/connections.py`, we added `load_dotenv(dotenv_path=env_path, override=True)`. This forces Python to prioritize the username specified in your `.env` file.

---

### Q7: What belongs in `schema.sql` vs. `queries.py`?
* **`schema.sql` (Data Definition - DDL):**
  * `CREATE TABLE IF NOT EXISTS ...`
  * Foreign key definitions and index creation.
  * Used only for database structure.
* **`queries.py` (Data Manipulation - DML):**
  * Python functions returning `SELECT` results to populate dropdowns and tables.
  * Functions running `INSERT` statements when a user submits an exam panel form.
  * Functions running `UPDATE` to change panel status (e.g., `Draft` to `Submitted`).

