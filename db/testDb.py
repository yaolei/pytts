from sqlalchemy import Column, Integer, String, DateTime, LargeBinary 
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()

class MP3File(Base):
    __tablename__ = 'TtsVoides'
    id = Column(Integer, primary_key=True)
    message_id = Column(String)
    send_user_id = Column(String)
    send_user_name = Column(String)
    created_date = Column(DateTime)
    message_data = Column(LargeBinary)