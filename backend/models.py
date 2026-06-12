from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True)
    candidate_name = Column(String)
    job_role = Column(String)
    experience_level = Column(String)

    history = relationship("ConversationHistory")


class ConversationHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        String,
        ForeignKey("interviews.id")
    )

    question = Column(String)
    answer = Column(String)
    score = Column(Float)
    feedback = Column(String)