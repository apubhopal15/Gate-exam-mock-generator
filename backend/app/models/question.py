from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, Integer,String ,Text, Enum, ForeignKey, DECIMAL, TIMESTAMP, Index
from sqlalchemy.sql import func
from app.database.db_connection import Base

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    question_code=Column(String,nullable=False)
    concept_id = Column(Integer, ForeignKey("concept.id"), index=True)

    question_text = Column(Text, nullable=False)

    question_type = Column(Enum("MCQ","MSQ","NAT", name="question_type"), nullable=False)
    difficulty_level = Column(Enum("easy","medium","hard", name="q_difficulty"), nullable=False)

    explaination = Column(Text)

    correct_answer_value = Column(DECIMAL(10,4))
    answer_tolerance = Column(DECIMAL(10,4), default=0)
    correct_option=Column(ARRAY(String))
    marks = Column(DECIMAL(5, 2), nullable=False)
    negative_marks = Column(DECIMAL(5, 2), nullable=False, default=0)
    source = Column(Enum("PYQ","AI","curated", name="question_source"))

    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        Index("idx_question_concept", "concept_id"),
    )