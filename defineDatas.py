from sqlalchemy import Column, Integer, String, Sequence, Bytes, DateTime
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()


class TsViodes(Base):
    __tablename__ = 'TtsVoides'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    send_user_name = Column(String(191))
    message_id = Column(String(191))
    send_user_id = Column(String(191))
    created_date = Column(DateTime(3))
    message_data = Column(Bytes)