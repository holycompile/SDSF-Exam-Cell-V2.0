# SDSF Exam Cell - Panel of Examiners Database Schema & Architecture

This document outlines the database tables, schema design, field descriptions, parent-child relationships, and data flow required to generate and manage the **Panel of Examiners** form.

---

## Table Hierarchy: Parent vs. Child Classification

In relational database design, **Parent Tables** store independent entities that can exist on their own, while **Child Tables** depend on one or more parent tables through Foreign Keys.

```text
[ ROOT PARENT TABLES ]
├── programs (Independent Master Table)
└── teachers (Independent Master Table)
         │
         ▼
[ INTERMEDIATE / CURRICULUM LEVEL ]
└── subjects (Child of `programs`, Parent to `exam_panel_subjects`)
         │
         ▼
[ TRANSACTION LEVEL ]
└── exam_panels (Child of `programs`, MAIN PARENT of the Exam Sheet)
         ├── exam_panel_subjects  (Child of `exam_panels`, `subjects`, and `teachers`)
         └── exam_panel_committee (Child of `exam_panels` and `teachers`)
```

### Summary Matrix

| Table Name | Classification | Parent Table(s) It Depends On | Child Table(s) That Depend On It | Cascade Delete Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **`programs`** | **Root Parent** | *None* | `subjects`, `exam_panels` | Deleting a program deletes its subjects (`CASCADE`) |
| **`teachers`** | **Root Parent** | *None* | `exam_panel_subjects`, `exam_panel_committee` | Deleting a teacher sets references to `NULL` (`SET NULL`) |
| **`subjects`** | **Child & Parent** | Parent: `programs` | Child: `exam_panel_subjects` | Deleting a subject sets panel row reference to `NULL` |
| **`exam_panels`** | **Transaction Parent** | Parent: `programs` | Children: `exam_panel_subjects`, `exam_panel_committee` | **Main Parent**: Deleting a panel removes all its subjects and committee rows (`CASCADE`) |
| **`exam_panel_subjects`** | **Child Table** | Parents: `exam_panels`, `subjects`, `teachers` | *None (Leaf Table)* | Cannot exist without parent `exam_panels` |
| **`exam_panel_committee`** | **Child Table** | Parents: `exam_panels`, `teachers` | *None (Leaf Table)* | Cannot exist without parent `exam_panels` |

---

## 1. Master Tables (Static / Pre-configured Data)

### Master Table 1: `programs` [ROOT PARENT TABLE]
Stores the academic programs or degree courses offered. Does not depend on any other table.

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `program_name` | VARCHAR(150) | NOT NULL | e.g., `"M.Tech. (AI & DS)"` |
| `program_code` | VARCHAR(50) | NOT NULL, UNIQUE | e.g., `"MTECH-AIDS"` |
| `total_semesters` | INTEGER | NOT NULL | e.g., `6` |

---

### Master Table 2: `teachers` [ROOT PARENT TABLE]
Stores faculty members who can be assigned as examiners or committee members. Does not depend on any other table.

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `employee_code` | VARCHAR(50) | NULLABLE | e.g., `"SDSF1000"`, `"SDSF1011"` |
| `full_name` | VARCHAR(150) | NOT NULL | e.g., `"Mr. Rajat Yadav"`, `"Dr. Govind Maheshwari"` |
| `contact_no` | VARCHAR(20) | NULLABLE | e.g., `"9826705696"` |

---

### Master Table 3: `subjects` [CHILD TABLE of `programs`]
Stores the curriculum mapping each subject/paper to its respective program and semester.
* **Parent Table**: `programs` (via `program_id`)

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `program_id` | INTEGER | FOREIGN KEY -> `programs(id)` | Parent program reference |
| `semester` | INTEGER | NOT NULL | Semester number (e.g., `5`) |
| `subject_code` | VARCHAR(50) | NOT NULL | e.g., `"DS6A-301"` |
| `subject_name` | VARCHAR(255) | NOT NULL | e.g., `"Datamining and Data Warehousing"` |

---

## 2. Transaction Tables (Exam Panel Submission Data)

### Transaction Table 4: `exam_panels` [TRANSACTION PARENT TABLE]
Parent record representing one panel document instance for a given session.
* **Parent Table**: `programs` (via `program_id`)
* **Child Tables that depend on it**: `exam_panel_subjects`, `exam_panel_committee`

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the panel |
| `panel_code` | VARCHAR(50) | NULLABLE | Form reference / template code |
| `program_id` | INTEGER | FOREIGN KEY -> `programs(id)` | Selected course/program |
| `semester` | INTEGER | NOT NULL | Selected semester (e.g., `5`) |
| `academic_session` | VARCHAR(50) | NOT NULL | e.g., `"2025-2026"` or `"DEC-2025"` |
| `exam_title` | VARCHAR(100) | DEFAULT 'Theory / Comprehensive Viva' | Exam header title |
| `status` | VARCHAR(30) | DEFAULT 'Draft' | `"Draft"`, `"Submitted"`, `"Approved"` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of creation |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of last modification |

---

### Transaction Table 5: `exam_panel_subjects` [CHILD TABLE]
Stores each subject row in the panel table along with the chosen examiners.
* **Parent Tables**:
  * `exam_panels` (via `panel_id` — `ON DELETE CASCADE`)
  * `subjects` (via `subject_id` — `ON DELETE SET NULL`)
  * `teachers` (via `examiner_1_id` & `internal_examiner_id` — `ON DELETE SET NULL`)

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the row |
| `panel_id` | INTEGER | FOREIGN KEY -> `exam_panels(id)` ON DELETE CASCADE | Parent panel reference |
| `serial_no` | INTEGER | NOT NULL | Row order (1, 2, 3...) |
| `subject_id` | INTEGER | FOREIGN KEY -> `subjects(id)` (NULLABLE) | Master subject ID (if picked from syllabus) |
| `custom_subject_code` | VARCHAR(50) | NULLABLE | Fallback for ad-hoc `+ Add Subject` rows |
| `custom_subject_name` | VARCHAR(255) | NULLABLE | Fallback for ad-hoc `+ Add Subject` rows |
| `student_category` | VARCHAR(10) | NOT NULL DEFAULT 'RE' | `"RE"` (Regular) or `"EX"` (Ex-student) |
| `examiner_1_id` | INTEGER | FOREIGN KEY -> `teachers(id)` | Dropdown selected Examiner-I |
| `internal_examiner_id` | INTEGER | FOREIGN KEY -> `teachers(id)` | Dropdown selected Internal Examiner |

---

### Transaction Table 6: `exam_panel_committee` [CHILD TABLE]
Stores the examination committee members and administrative signatories displayed at the bottom of the form.
* **Parent Tables**:
  * `exam_panels` (via `panel_id` — `ON DELETE CASCADE`)
  * `teachers` (via `teacher_id` — `ON DELETE SET NULL`)

| Column Name | Data Type | Constraints | Description / Example |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `panel_id` | INTEGER | FOREIGN KEY -> `exam_panels(id)` ON DELETE CASCADE | Parent panel reference |
| `teacher_id` | INTEGER | FOREIGN KEY -> `teachers(id)` | Dropdown selected faculty member |
| `role` | VARCHAR(100) | NOT NULL | e.g., `"Member 1"`, `"Member 2"`, `"Member 3"`, `"Chairman BOS"`, `"Coordinator"`, `"Head"`, `"Vice Chancellor"` |
| `display_order` | INTEGER | NOT NULL | Display order sequence (1 to 7) |

---

## 3. End-to-End Operational Workflow

### Step 1: Input Course & Semester
* User selects the **Program** (e.g., `M.Tech. (AI & DS)`) and the **Semester** (e.g., `5`) along with the **Academic Session**.
* All active teachers from `teachers` table are pre-loaded to populate dropdown options.

### Step 2: Auto-Fetch Subjects
* A backend query runs:
  * Filter: `program_id = :selected_program AND semester = :selected_semester` from `subjects`.
* The system automatically generates pre-filled rows with `subject_code` and `subject_name`.

### Step 3: Assign Examiners & Committee Members
* For each subject row:
  * User selects **Examiner-I** from teacher dropdown.
  * User selects **Internal Examiner** from teacher dropdown (same teacher can be selected for both if required).
  * Contact number auto-populates beneath the name from the `teachers` master data.
* For the bottom committee grid:
  * User selects Member 1, Member 2, Member 3, Chairman BOS, Coordinator, Head, and Vice Chancellor from the teacher dropdowns.

### Step 4: Submission & Database Storage
When "Submit" is clicked:
1. One record is inserted into `exam_panels`.
2. Multiple records are inserted into `exam_panel_subjects` (one per table row).
3. Seven records are inserted into `exam_panel_committee` (one per signatory).

---

## 4. How to Retrieve the Complete Panel (Joining Tables)

To display or print the saved panel:

1. **Header & Program details**:
   * Join `exam_panels` with `programs` on `exam_panels.program_id = programs.id`.

2. **Table Rows (Subject Code, Name, Examiners)**:
   * Query `exam_panel_subjects` where `panel_id = :target_panel_id`:
     * Left Join `subjects` on `exam_panel_subjects.subject_id = subjects.id`
     * Left Join `teachers` as `ex1` on `exam_panel_subjects.examiner_1_id = ex1.id`
     * Left Join `teachers` as `inte` on `exam_panel_subjects.internal_examiner_id = inte.id`
     * Order by `serial_no ASC`

3. **Exam Committee Members**:
   * Query `exam_panel_committee` where `panel_id = :target_panel_id`:
     * Join `teachers` on `exam_panel_committee.teacher_id = teachers.id`
     * Order by `display_order ASC`

