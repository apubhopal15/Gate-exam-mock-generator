from app.models.user import User
from app.models.concept import Concept
from app.models.mock_questions import MockQuestion
from app.models.mocktest import MockTest
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.student_attempt import StudentAttempt
from app.models.attempt_answer import AttemptAnswer

from . import schema,utils
from app.database.db_connection import Session,get_db
from typing import Literal
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import FastAPI,Depends, Query,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import UTC, datetime

app=FastAPI()

origins=["http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#authentication
@app.post('/auth/register',status_code=status.HTTP_201_CREATED,response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session=Depends(get_db)):
    existing_user= db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password= utils.hash_password(user.password)
    user.password=hashed_password
    new_user=User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/auth/login', status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    access_token=utils.create_access_token({"user_id":user.id,"user_name":user.name})
    return {"token":access_token,"type":"bearer"}


@app.get('/users/me')
def get_me(current_user=Depends(utils.get_current_user)):
    return {
        "message": "User is authenticated",
        "user_id": current_user.id,
        "user_name":current_user.name
    }


#exam
@app.get('/exam',status_code=status.HTTP_200_OK)
def get_exam_type(exam_type:Literal["CSE","DA"]= Query(...,description="Select exam type"),current_user=Depends(utils.get_current_user)):
    return{
        "success":True,
        "selected_exam_type": exam_type
    }


#mock generation
@app.post('/mock/generate')
def generate_mock(exam_type:str,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    TOTAL_QUESTIONS=65
    concepts=db.query(Concept).filter(Concept.exam_type==exam_type).all()
    if not concepts:
        raise ValueError("No concepts found")
    total_weightage=sum(c.weightage for c in concepts)
    selected_questions=[]
    for concept in concepts:
        target_count=max(1,round(concept.weightage*TOTAL_QUESTIONS/total_weightage))
        easy_count=round(target_count*0.25)
        medium_count=round(target_count*0.55)
        hard_count=(target_count-easy_count-medium_count)
        easy_questions=utils.pick_questions(db,concept.id,"easy",easy_count)
        selected_questions.extend(easy_questions)
        medium_questions=utils.pick_questions(db,concept.id,"medium",medium_count)
        selected_questions.extend(medium_questions)
        hard_questions=utils.pick_questions(db,concept.id,"hard",hard_count)
        selected_questions.extend(hard_questions)
    unique_questions={}
    for q in selected_questions:
        unique_questions[q.id]=q
    selected_questions=list(unique_questions.values())
    random.shuffle(selected_questions)
    selected_questions=selected_questions[:TOTAL_QUESTIONS]
    print(len(selected_questions))
    mock_test=MockTest(        
        title=f"{exam_type} mock test",
        exam_type=exam_type,
        created_by=current_user.id,
        total_marks=100,
        duration_minutes=180,
        is_generated=True 
        )
    db.add(mock_test)
    db.flush()
    for order,question in enumerate(selected_questions,start=1):
        mock_question=MockQuestion(
            mocktest_id=mock_test.id,
            question_id=question.id,
            question_order=order
        )
        db.add(mock_question)
    db.commit()
    db.refresh(mock_test)
    return mock_test


#fetch mock
@app.get('/mocks/{mock_id}')
def fetch_mock(mock_id:int, db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    mock_test=db.query(MockTest).filter(MockTest.id==mock_id).first()
    if not mock_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Mock Test not found")
    questions_data=[]
    mock_questions= db.query(MockQuestion).filter(MockQuestion.mocktest_id==mock_id).all()
    for mq in mock_questions:
        question= db.query(Question).filter(Question.id==mq.question_id).first()
        options=db.query(QuestionOption).filter(QuestionOption.question_id==mq.question_id).all()
        questions_data.append({
            "question_id":question.id,
            "question_order":mq.question_order,
            "question_code":question.question_code,
            "question_text":question.question_text,
            "question_type":question.question_type,
            "difficulty_level":question.difficulty_level,
            "marks":question.marks,
            "negative_marks":question.negative_marks,
            "options":[{"option_id":option.id,
                        "option_label":option.option_label,
                        "option_text":option.option_text
                        }
                       for option in options]
            })
    return {
        "id":mock_test.id,
        "title":mock_test.title,
        "exam_type":mock_test.exam_type,
        "total_marks":mock_test.total_marks,
        "duration":mock_test.duration_minutes,
        "created_by":mock_test.created_by,
        "created_at":mock_test.created_at,
        "questions":questions_data
        }
        

#start attempt
@app.post('/attempts/{mock_id}/start')
def start_attempt(mock_id:int,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    mock_test=db.query(MockTest).filter(MockTest.id==mock_id).first()
    if not mock_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mock test not found')
    attempt=StudentAttempt(
        user_id=current_user.id,
        mocktest_id=mock_id,
        started_at=datetime.now(UTC),
        status='in_progress'
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return{
        "attempt_id":attempt.id,
        "mocktest_id":attempt.mocktest_id,
        "started_at":attempt.started_at,
        "status":attempt.status,
        "duration_in_minutes":mock_test.duration_minutes
    }

# @app.post('/attempts/{attempt_id}/answer')
# def save_answer(attempt_id:int, data: dict):
#     print("RAW DATA:", data)
#     return {"ok": True}
#save answer
@app.post('/attempts/{attempt_id}/answer')
def save_answer(attempt_id:int,data:schema.SaveAnswerRequest,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    attempt=db.query(StudentAttempt).filter(StudentAttempt.id==attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Attempt not found")
    if attempt.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not allowed")
    if attempt.status!="in_progress":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Attempt already submitted")
    print(data.selected_option, type(data.selected_option))
    answer=db.query(AttemptAnswer).filter(AttemptAnswer.attempt_id==attempt_id,AttemptAnswer.question_id==data.question_id).first()
    if answer:
        answer.answer_numeric=data.answer_numeric if data.answer_numeric else None
        answer.selected_option=(data.selected_option) if data.selected_option else None
    else:
        answer=AttemptAnswer(
            attempt_id=attempt_id,
            question_id=data.question_id,
            answer_numeric=data.answer_numeric if data.answer_numeric else None,
            selected_option=(data.selected_option) if data.selected_option else None
        )
        db.add(answer)
        db.flush()
    db.commit()
    db.refresh(answer)
    return{
        "message":"answes saved",
        "attempt_id":attempt_id,
        "question_id":answer.question_id,
        "answer_id":answer.id
    }


#submit
@app.post('/attempts/{attempt_id}/submit')
def submit(attempt_id:int,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    attempt=db.query(StudentAttempt).filter(StudentAttempt.id==attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Attempt not found")
    attempt.completed_at=datetime.now(UTC)
    attempt.status="submitted"
    db.commit()
    db.refresh(attempt)
    return {
        "attempt_id":attempt_id,
        "mocktest_id":attempt.mocktest_id,
        "status":attempt.status,
        "started_at":attempt.started_at,
        "completed_at":attempt.completed_at
    }


#score_evaluation
@app.get('/attempts/{attempt_id}/result')
def result(attempt_id:int,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    attempt=db.query(StudentAttempt).filter(StudentAttempt.id==attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Attempt not found")
    metrics=utils.calculate_attempt_metrics(attempt_id,db)
    attempt.score=metrics["score"]
    db.commit()
    return{
        "score":metrics["score"]
    }
    


#analytics
@app.get('/attempts/{attempt_id}/analytics')
def analytics(attempt_id:int,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    metrics=utils.calculate_attempt_metrics(attempt_id,db)
    return metrics


#user dashboard  -->  return summary and recent attempts
@app.get('/users/me/dashboard')
def dashboard(db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    attempts=db.query(StudentAttempt).filter(StudentAttempt.user_id==current_user.id).all()
    total_attempts=len(attempts)
    completed_attempts=[ a
        for a in attempts
        if a.status in ["completed","submitted"]]
    scores=[float(a.score)
            for a in completed_attempts]
    avg_score=(round(sum(scores)/len(scores),2) if scores else 0)
    best_score=max(scores) if scores else 0
    recent_attempts=db.query(StudentAttempt).filter(StudentAttempt.user_id==current_user.id).order_by(StudentAttempt.started_at.desc()).limit(5).all()
    return{
        "summary":{
            "total_attempts":total_attempts,
            "completed_attempts":len(completed_attempts),
            "avg_score":avg_score,
            "best_score":best_score
        },
        "recent_attempts":[
            {
                "attempt_id":a.id,
                "mocktest_id":a.mocktest_id,
                "score":a.score,
                "status":a.status,
                "started_at":a.started_at,
                "completed_at":a.completed_at
            }for a in recent_attempts
        ]
    }


#history  -->  returns all attempt with pagination
@app.get('/users/me/attempts')
def history(page:int=1,size:int=10,db:Session=Depends(get_db),current_user=Depends(utils.get_current_user)):
    offset=(page-1)*size
    query=db.query(StudentAttempt).filter(StudentAttempt.user_id==current_user.id)
    total_attempts=query.count()
    attempts=query.order_by(StudentAttempt.started_at.desc()).limit(size).offset(offset).all()
    return{
        "page":page,
        "size":size,
        "total_attempts":total_attempts,
        "attempts":[
            {
                "attempt_id":a.id,
                "mocktest_id":a.mocktest_id,
                "score":a.score,
                "status":a.status,
                "started_at":a.started_at,
                "completed_at":a.completed_at
            }for a in attempts
        ]
    }