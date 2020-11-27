from database import *
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

maxim = User('SmakovMax', '25062004', 'noobdestroyer@rambler.ru')

pavlo = User('PavloKonoplov', 'ilikeducks', 'fakemail@trust.com')

teaParty = Event('Tea Party', None, 'Bring cookies', maxim)

pavlo.attended_events.append(teaParty)

session.add(maxim)

session.commit()
