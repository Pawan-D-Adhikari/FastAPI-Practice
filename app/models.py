from pickle import TRUE
from annotated_types import Timezone
from sqlalchemy import TIMESTAMP, Column ,Integer,String,Boolean, text ,false
from .database import Base

class Posts(Base):
    __tablename__='posts'
    
    id=Column(Integer,primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    creared_at=Column(TIMESTAMP(timezone=TRUE),nullable=false,server_default=text('now()'))
   

