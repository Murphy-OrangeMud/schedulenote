from sqlalchemy import Column,String,Integer,Text,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql+pymysql://root:123456@localhost:3306/ScheduleNotes?charset=utf8',
                        max_overflow=0,
                        pool_size=10,
                        pool_timeout=30,
                        pool_recycle=-1    
                    )
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer,primary_key = True,autoincrement=True)
    filename = Column(String(20))
    score = Column(Integer)
    uploader = Column(Integer)
    description = Column(Text)
    course = Column(Integer)
    def __init__(self, filename, uploader,description,course):
        self.filename = filename
        self.uploader = uploader
        self.description = description
        self.course = course
        self.score = 0
    def save(self):
        session.add(self)
        session.commit()
    def upvote():
        score += 1
        session.commit()
    def downvote():
        score -= 1
        session.commit()

class Course(Base):
    # 表的名字:
    __tablename__ = 'course'
    # 表的结构:
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(20))
    score = Column(Integer)
    info = Column(Text)
    def __init__(self,name,info=""):
        self.name = name
        self.info = info
    def save(self):
        session.add(self)
        session.commit()
    def addFile(self,newfile):
        # file = File(
        print("res")
        file = File(newfile["filename"],newfile["uploader"],newfile["description"],self.id)
        file.save()
        print(newfile)
        pass
    def deleteFile(self,id):
        res = session.query(File).filter(File.id == id).delete()
        session.commit()
        return res


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # # C1 = Course(1,"ICS","hard")
    # file = {"filename":"txtbook.txt","uploader":1,"description":"txtbook"}
    # print(file)
    # Cs = session.query(Course).filter(Course.id == 1).all()
    # for c in Cs:
    #     c.addFile(file)
    #     c.addFile(file)
    # pass
