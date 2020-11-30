USE [Pavlo_Python]
GO

INSERT INTO [dbo].[User]
           ([username]
           ,[password]
           ,[email])
     VALUES
           ('SmakovMax'
           ,'25062004'
           ,'noobdestroyer@rambler.ru'),
		              ('PavloKonoplov'
           ,'ilikeducks'
           ,'fakemail@trust.com')

GO

USE [Pavlo_Python]
GO

INSERT INTO [dbo].[Event]
           ([name]
           ,[date]
           ,[description]
           ,[author_id])
     VALUES
           ('Tea Party'
           ,null
           ,'Bring cookies'
           ,1)
GO

USE [Pavlo_Python]
GO

INSERT INTO [dbo].[User_Events]
           ([user_id]
           ,[event_id])
     VALUES
           (2
           ,1)
GO



