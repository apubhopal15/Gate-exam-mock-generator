from decimal import Decimal

from passlib.context import CryptContext
from app.database.db_connection import Base,engine,Session, get_db
from jose import jwt,JWTError
from datetime import UTC, datetime,timedelta
import random
from app.models.question import Question
from app.models.student_attempt import StudentAttempt
from app.models.mock_questions import MockQuestion
from app.models.attempt_answer import AttemptAnswer
from . import schema
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status

Base.metadata.create_all(bind=engine)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password) 



SECRET_KEY="n08jet57bw892nd7bcy6w9nv"
ALGORITHM="HS256"
EXPIRY_TIME=300

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(UTC) + timedelta(minutes=EXPIRY_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id= payload.get("user_id")
        name=payload.get("user_name")
        if id is None:
            raise credentials_exception
        token_data=schema.TokenData(id=id,name=name)
    except JWTError:
        raise credentials_exception
    return token_data


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='auth/login')
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception)

    
def pick_questions(db, concept_id, difficulty,count):
    pool=db.query(Question).filter(Question.concept_id==concept_id, Question.difficulty_level==difficulty).all()
    if len(pool)<=count:
        return pool
    return random.sample(pool,count)


def check_answer(question,answer):
    if question.question_type =='MCQ':
        if answer.selected_option is None:
            return False
        return (answer.selected_option and answer.selected_option==question.correct_option)
    if question.question_type == 'MSQ':
        if answer.selected_option is None:
            return False
        submitted = set(answer.selected_option)
        correct = set(question.correct_option)
        return submitted == correct
    if question.question_type=='NAT':
        if answer.answer_numeric is None:
            return False
        submitted_ans=answer.answer_numeric
        correct_ans=question.correct_answer_value
        tolerance=question.answer_tolerance
        if abs(correct_ans-submitted_ans)<=tolerance:
            return True
        return False
    

def calculate_attempt_metrics(attempt_id:int,db:Session):
    attempt=db.query(StudentAttempt).filter(StudentAttempt.id==attempt_id).first()
    mock_questions=db.query(MockQuestion,Question).join(Question,MockQuestion.question_id==Question.id).filter(MockQuestion.mocktest_id==attempt.mocktest_id).all()
    answers=db.query(AttemptAnswer).filter(AttemptAnswer.attempt_id==attempt.id).all()
    ans_map={
        ans.question_id:ans
        for ans in answers
    }
    total_questions=len(mock_questions)
    attempted=0
    not_attempted=0
    correct=0
    wrong=0
    marks_gained=Decimal("0")
    marks_lost=Decimal("0")
    for _,question in mock_questions:
        answer=ans_map.get(question.id)
        if not answer:
            not_attempted+=1
            continue
        attempted+=1
        is_correct=check_answer(question,answer)
        if is_correct:
            marks_gained+=question.marks
            correct+=1
        else:
            marks_lost+=question.negative_marks
            wrong+=1
    score=marks_gained-marks_lost
    return{
        "score":score,
        "attempted":attempted,
        "not_attempted":not_attempted,
        "total_questions":total_questions,
        "correct":correct,
        "wrong":wrong,
        "accuracy":(
            (correct/attempted)*100
            if attempted else 0
        ),
        "marks_gained":marks_gained,
        "marks_lost":marks_lost
    }


