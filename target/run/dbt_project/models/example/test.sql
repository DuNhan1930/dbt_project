
  
    

    create or replace table `symmetric-fin-469415-q9`.`glamira_data_2025`.`test`
      
    
    

    
    OPTIONS()
    as (
      

WITH src AS (
 SELECT *
 FROM symmetric-fin-469415-q9.glamira_data_2025.summary
),


checkout_success AS (
 SELECT
   _id AS customer_id,
   ip AS ip_address,
   time_stamp AS date_id,
   local_time AS local_time,
   device_id AS device_id,
   email_address AS email_address,
   resolution AS resolution,
   user_id_db AS user_id_db,
   user_agent AS user_agent,
   referrer_url AS referrer_url
 FROM src
 WHERE collection = 'checkout_success'
)

SELECT * FROM checkout_success
    );
  