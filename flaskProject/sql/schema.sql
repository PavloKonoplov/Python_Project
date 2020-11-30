USE [Pavlo_Python]
GO

/****** Object:  Table [dbo].[User]    Script Date: 27.11.2020 15:38:28 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[User](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [varchar](64) NULL,
	[password] [varchar](16) NULL,
	[email] [varchar](64) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [Pavlo_Python]
GO

/****** Object:  Table [dbo].[Event]    Script Date: 27.11.2020 15:39:06 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Event](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](64) NULL,
	[date] [datetime] NULL,
	[description] [varchar](512) NULL,
	[author_id] [int] NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Event]  WITH CHECK ADD FOREIGN KEY([author_id])
REFERENCES [dbo].[User] ([id])
GO

USE [Pavlo_Python]
GO

/****** Object:  Table [dbo].[User_Events]    Script Date: 27.11.2020 15:39:27 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[User_Events](
	[user_id] [int] NOT NULL,
	[event_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED
(
	[user_id] ASC,
	[event_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[User_Events]  WITH CHECK ADD FOREIGN KEY([event_id])
REFERENCES [dbo].[Event] ([id])
GO

ALTER TABLE [dbo].[User_Events]  WITH CHECK ADD FOREIGN KEY([user_id])
REFERENCES [dbo].[User] ([id])
GO


