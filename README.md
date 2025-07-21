# TechSpark⚡-- 🎓 University Event Management System 

A full-stack event management platform built for universities to manage their internal events, student registrations, and department workflows — complete with Razorpay integration and a multi-role approval system.

---

## 🚀 Features

- ✅ University onboarding with payment verification
- ✅ Role-based dashboard for 4 levels of staff
- ✅ Event creation and approval workflows
- ✅ Student registration and multi-step verification
- ✅ Razorpay test-mode integration for payment
- ✅ Real-time access control for students and staff

---

## 🏗️ User Roles & Workflow

### 👨‍🏫 1. University
- Registers on the platform and completes payment.
- Only after payment, marked as `verified`.

### 🧑‍💼 2. University Event Head
- Assigned **1 per university**.
- Approves/rejects:
  - Proposed events from departments.
  - Coordinator applications.
  - Student verification requests.

### 🏛️ 3. Department
- Can verify students’ fee slips and course selection.
- Assigns **1 unique coordinator per department**.

### 🧑‍🔧 4. Department Event Coordinator
- Can propose new events.
- Await university head approval before publishing events.

### 🎓 5. Students
- Register to their university.
- Must be:
  1. Approved by University Head
  2. Verified by Department staff (fee slips, course docs)
- After approval, can log in and register for approved events.

---

## 🔁 Workflow Diagram

```mermaid
graph TD
  A[University Registers & Pays] --> B[Marked Verified]
  B --> C[Event Head Assigned]
  B --> Q[Department Created]
  Q --> D[Coordinator Applications]
  C --> D[Coordinator Applications]
  D --> E[Department Event Coordinator Assigned]
  E --> F[Proposes Events]
  F --> G[Head Approves]
  G --> H[Event Published]

  C --> I[Student Registers]
  I --> J[Head Approves Student]
  J --> K[Student Uploads Docs]
  K --> L[Department Verifies]
  L --> M[Student Gets Dashboard Access]
