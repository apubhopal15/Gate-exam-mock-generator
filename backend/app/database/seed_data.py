import json
import yaml
from pathlib import Path
from sqlalchemy.orm import Session 
from app.database.db_connection import SessionLocal
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.subtopic import Subtopic
from app.models.concept import Concept

BACKEND_DIR = Path.cwd()
DATA_DIR = BACKEND_DIR.parent / "data"

KB_DIR = DATA_DIR / "knowledge_base"
QB_DIR = DATA_DIR / "question_bank"

GATE_CSE_QB_DIR=QB_DIR/"gate_cse"
GATE_DA_QB_DIR=QB_DIR/"gate_da"

GATE_CSE_KB_DIR=KB_DIR/"gate_cse"
GATE_DA_KB_DIR=KB_DIR/"gate_da"

def seed_question_bank():
    db: Session = SessionLocal()
    try:
        for exam_dir in QB_DIR.iterdir():
            if exam_dir.is_dir():
                print(f"Processing exam: {exam_dir.name}")
                # Loop through all JSON files
                for json_file in exam_dir.glob("*.json"):
                    print(f"Processing file: {json_file.name}")

                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    questions = data.get("question_bank", [])
                    exam_type = "CSE" if "cse" in exam_dir.name.lower() else "DA"
                    concepts = (
                        db.query(Concept)
                        .filter(Concept.exam_type == exam_type)
                        .all()
                    )

                    concept_map = {
                        concept.concept_code: concept.id
                        for concept in concepts
                    }

                    for q in questions:
                        concept_code = q.get("concept_code")

                        concept_id = concept_map.get(concept_code)

                        if not concept_id:
                            raise ValueError(
                                f"Concept not found for concept_code={concept_code}, exam_type={exam_type}"
                            )
                        
                        if q["question_type"] == "NAT":
                            correct_answer_value = float(q["correct_answer"])
                            correct_option = None
                        else:
                            correct_answer_value = None
                            correct_option = q["correct_answer"]
                        # Create Question object
                        question = Question(
                            question_code=q["question_code"],
                            concept_id=concept_id,
                            question_text=q["question_text"],
                            question_type=q["question_type"],
                            difficulty_level=q["difficulty"],
                            explaination=q.get("explanation"),
                            correct_answer_value=correct_answer_value,
                            answer_tolerance=q.get("answer_tolerance", 0),
                            correct_option=correct_option,
                            marks=q["marks"],
                            negative_marks=q.get("negative_marks", 0),
                            source="curated"
                        )

                        db.add(question)
                        db.flush()  

                        # Insert options if MCQ/MSQ
                        if q["question_type"] in ["MCQ", "MSQ"]:
                            for opt in q.get("options", []):
                                option = QuestionOption(
                                    question_id=question.id,
                                    option_label=opt["option_id"],
                                    option_text=opt["text"],
                                    is_correct=opt["is_correct"]
                                )
                                db.add(option)

                    db.commit()
                    print(f"Finished inserting from {json_file.name}")

                print("✅ All question banks seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f" Error:", e)

    finally:
        db.close()

# ------------------ HELPER ------------------

def get_or_create(db, model, defaults=None, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance

    params = dict(kwargs)
    if defaults:
        params.update(defaults)

    instance = model(**params)
    db.add(instance)
    db.flush()
    return instance


# ------------------ SEED FUNCTION ------------------

def seed_kb():
    db: Session = SessionLocal()

    try:
        for exam_dir in KB_DIR.iterdir():

            if not exam_dir.is_dir():
                continue

            exam_type = "CSE" if "cse" in exam_dir.name.lower() else "DA"
            print(f"Processing exam: {exam_dir.name}")

            for yaml_file in exam_dir.glob("*.yaml"):
                print(f"  Processing file: {yaml_file.name}")

                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                print(data["subject"])

                # ---------------- SUBJECT ----------------
                subject = get_or_create(
                    db,
                    Subject,
                    name=data["subject"]
                )

                # ---------------- TOPICS ----------------
                for topic_data in data.get("topics", []):

                    topic = get_or_create(
                        db,
                        Topic,
                        name=topic_data["name"],
                        topic_code=topic_data["topic_code"],
                        subject_id=subject.id,
                        defaults={
                            "weightage": topic_data.get("weightage", 0)
                        }
                    )

                    # ---------------- SUBTOPICS ----------------
                    for subtopic_data in topic_data.get("subtopics", []):

                        subtopic = get_or_create(
                            db,
                            Subtopic,
                            name=subtopic_data["name"],
                            topic_id=topic.id
                        )

                        # ---------------- CONCEPTS (FIXED LOGIC) ----------------
                        for concept_data in subtopic_data.get("concepts", []):

                            concept_code = concept_data["concept_code"]

                            # 🔥 IMPORTANT: match DB UNIQUE KEY
                            existing_concept = db.query(Concept).filter_by(
                                concept_code=concept_code,
                                exam_type=exam_type
                            ).first()

                            if not existing_concept:
                                concept = Concept(
                                    concept_code=concept_code,
                                    exam_type=exam_type,
                                    subtopic_id=subtopic.id,
                                    name=concept_data["name"],
                                    weightage=concept_data.get("weightage", 0)
                                )
                                db.add(concept)
                            else:

                                existing_concept.subtopic_id = subtopic.id

                db.commit()
                print(f"✅ Finished file: {yaml_file.name}")

        print("✅ Knowledge Base Seeded Successfully")

    except Exception as e:
        db.rollback()
        print("❌ Error:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    seed_question_bank()


