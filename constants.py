"""definition for project constants"""

LAT_LONG = {"Ranchi": (23.344315, 85.296013),"Delhi": (28.679079, 77.069710), "Mumbai": (19.076090, 72.877426), "Bhubaneswar": (20.296059, 85.824539), "Durg": (21.190449, 81.284920)}

MAX_RETRIES = 5  # number of retries to be made if hit to the API fails
TEMP_UNIT = "metric"  #  for temperature in Celsius default is Kelvin

DROP_DATASET1_TABLE_QUERY = """drop table if exists DATASET1"""

CREATE_DATASET1_QUERY = """
create table DATASET1 
as 
select distinct location Location, date(date_time) Date, temperature Temperature
from raw w_out
where temperature = (select max(temperature) 
                     from raw w_in 
                     where w_out.location=w_in.location
                     and strftime('%m', w_out.date_time) = strftime('%m', w_in.date_time))
"""

DROP_DATASET2_TABLE_QUERY = """drop table if exists DATASET2"""

CREATE_DATASET2_QUERY = """
create table DATASET2 
as 
select distinct date, round(avg_temperature, 2) avg_temperature, round(min_temperature, 2) min_temperature, w_min.location min_temp_loc, w_max.location max_temp_loc
from (
       select date(date_time) date, avg(temperature) avg_temperature, min(temperature) min_temperature, max(temperature) max_temperature 
       from raw
       group by date(date_time)
     ) w_agg
join raw w_min
on w_min.temperature=w_agg.min_temperature and date(w_min.date_time)=w_agg.date
join raw w_max
on w_max.temperature=w_agg.max_temperature and date(w_max.date_time)=w_agg.date
"""
