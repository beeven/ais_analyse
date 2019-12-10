select count(*), mmsi
from dachan20191205
where dachan20191205.mmsi not in 
 (select mmsi from aisdata)
group by mmsi
;

select count(*), mmsi
from dachan20191205
where dachan20191205.mmsi not in 
 (select mmsi from local20191205)
 and timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
group by mmsi
;

select count(*), mmsi
from local20191205
where local20191205.mmsi not in 
 (select mmsi from dachan20191205)
group by mmsi

;
select count(distinct(mmsi)) from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
; select count(*) from local20191205
where  timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
;
select count(distinct(mmsi)) from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
	
; select count(*) from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 

select count(distinct(mmsi)), count(*) from aisdata
where utc between 1575508860 and 1575509700


select max(latitude), max(longitude), min(latitude), min(longitude) from dachan20191205
where  latitude > 0 and longitude > 0
and timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 

select max(latitude), max(longitude), min(latitude), min(longitude) from local20191205
where latitude > 0 and longitude > 0
and timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 

select max(lat), max(lon), min(lat), min(lon) from aisdata
where lat > 0 and lon > 0
and utc between 1575508860 and 1575509700


-- 数据库船只数量
select count(distinct(mmsi)) from aisdata 
where lat/1000000.0 between  22.4202389 and 22.60018056
 and lon/1000000.0 between 113.7502639 and 113.94486778
 and utc between 1575508860 and 1575509700


        

-- 临时基站 not in 数据库
select count(distinct(mmsi))
from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and mmsi not in 
( select distinct(mmsi) from aisdata 
where lat/1000000.0 between  22.4202389 and 22.60018056
 and lon/1000000.0 between 113.7502639 and 113.94486778
 and utc between 1575508860 and 1575509700
 )
 
 
-- 临时基站 not in 山顶基站
 select count(distinct(mmsi))
from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and mmsi not in 
( select distinct(mmsi) from local20191205
where latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
 )
 
 
-- 山顶基站 not in 临时基站 
 select count(distinct(mmsi))
from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and mmsi not in 
( select distinct(mmsi) from dachan20191205
where  timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
 )

-- 山顶基站 not in 数据库
select count(distinct(mmsi))
from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and mmsi not in 
( select distinct(mmsi) from aisdata 
where lat/1000000.0 between  22.4202389 and 22.60018056
 and lon/1000000.0 between 113.7502639 and 113.94486778
 and utc between 1575508860 and 1575509700
 )

-- 数据库 not in 山顶基站
select distinct(mmsi)
from aisdata
where lat/1000000.0 between  22.4202389 and 22.60018056
 and lon/1000000.0 between 113.7502639 and 113.94486778
 and utc between 1575508860 and 1575509700
 and mmsi not in (
 select distinct(mmsi) from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
	)
and mmsi not in (
select distinct(mmsi) from dachan20191205
where  timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00' 
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
)
	

-- in 3
select distinct(mmsi)
from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
and mmsi in
(
select distinct(mmsi)
from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  22.4202389 and 22.60018056
  and longitude between 113.7502639 and 113.94486778
)
and mmsi IN
(
select distinct(mmsi)
from aisdata
where lat/1000000.0 between  22.4202389 and 22.60018056
 and lon/1000000.0 between 113.7502639 and 113.94486778
 and utc between 1575508860 and 1575509700
)