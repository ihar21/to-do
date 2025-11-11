from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///tasks.db", echo = True)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    due_date = Column(DateTime)
    priority = Column(Integer)
    done = Column(Boolean, default = False)

    def __repr__(self):
        return f"<Task(id={self.id}), name={self.name}, description={self.description}"

Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

#test
#session.add_all([
#    Task(name="Test task1", description="dfsds")
#])
session.commit()

for task in session.query(Task).all():
    print(task)