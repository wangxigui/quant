create table swindex (
    SwIndexCode varchar(20),
    SwIndexName varchar(20),
    BargainDate date, -- BargainDate varchar(20),
    OpenIndex float,
    MaxIndex float,
    MinIndex float,
    CloseIndex float,
    BargainAmount double, -- 成交量
    BargainSum double, -- 成交额
    Markup float
)
