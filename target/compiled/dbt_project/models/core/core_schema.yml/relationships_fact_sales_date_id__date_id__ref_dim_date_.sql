
    
    

with child as (
    select date_id as from_field
    from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
    where date_id is not null
),

parent as (
    select date_id as to_field
    from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date`
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


