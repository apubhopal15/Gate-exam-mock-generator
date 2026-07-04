High level system flow

Client (Student)
        ↓
API Routes
        ↓
Controller Layer
        ↓
Service Layer
        ↓
-----------------------------
| Domain Engines            |
| - Mock Generation Engine  |
| - Analytics Engine        |
-----------------------------
        ↓
Data Layer
(Database + Question Bank + Knowledge Base)


Mock generation flow (system level)

User Request → /generate-mock
        ↓
Mock Controller
        ↓
Mock Generation Service
        ↓
[Decision Layer]
    → Use Prebuilt Mock (fast)
    → Generate New Mock (slow)


User selects paper (CSE / DA)
        ↓
Load blueprint rules
        ↓
Allocate marks to topics
        ↓
Convert marks into question slots
        ↓
Assign difficulty levels
        ↓
Assign question types
        ↓
Assign mark values
        ↓
Generate questions
        ↓
Assemble mock test
        ↓
Validate paper


Generation engine pipeline (core logic)

Exam Blueprint (input)
      ↓
Concept Selection Engine
      ↓
Template Selection Engine
      ↓
Parameter Generator
      ↓
Difficulty Calibration Engine
      ↓
Solver Engine
      ↓
Validation Engine
      ↓
Paper Assembly Engine
      ↓
Generated Mock Test (output)


Attempt + Analysis flow 

Student submits answers
        ↓
Store attempt (raw answers)
        ↓
Evaluation Engine:
    → calculate score
    → map answers to concepts
        ↓
Analytics Engine:
    → topic accuracy
    → weak concept detection
    → time analysis
        ↓
Store analytics
        ↓
Return performance report


Cache Layer
- Frequently generated mocks
- Popular questionss

Detailed mock generation steps (refined)

Input:
- exam_type
- blueprint
- difficulty rules

Steps:
1. Load blueprint rules
2. Allocate marks to topics
3. Convert marks → question slots
4. Assign difficulty per slot
5. Assign question type
6. Fetch/generate question:
      → From Question Bank
      → From Template Generator
      → From AI Generator
7. Validate:
      → No duplicates
      → Correct difficulty distribution
8. Assemble paper
9. Store in DB
10. Return mock_id

