

  create or replace view `symmetric-fin-469415-q9`.`glamira_data_2025`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `symmetric-fin-469415-q9`.`glamira_data_2025`.`my_first_dbt_model`
where id = 1;

