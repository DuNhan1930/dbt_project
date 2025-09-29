
    
    

with dbt_test__target as (

  select location_id as unique_field
  from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_location`
  where location_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


