from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, TIMESTAMP, JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy import Enum
from sqlalchemy.sql import func
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def __init__(self, *args, **kwargs):
	cols = [(k,v) for k,v in type(self).__dict__.items() if k !='id' and isinstance(v,InstrumentedAttribute)]
	if args:
		for i,v in enumerate(args):
			setattr(self, cols[i][0], v)
	if kwargs:
		for k,v in kwargs.items():
			setattr(self, k, v)

class RawApiData(BaseModel):
	__tablename__ = "raw_api_data"

	id = Column(Integer, primary_key=True)
	ingest_timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
	api_name = Column(String(64), nullable=False)
	api_url = Column(Text, nullable=False)
	api_data = Column(JSON, nullable=True)


# class SponsorData(BaseModel):
# 	__tablename__ = "sponsor_data"