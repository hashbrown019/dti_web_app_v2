-- === SELECT entries which all users(in puted by) are same area ======

SELECT * FROM `form_a_farmer_profiles` 
   WHERE USER_ID in 
      ( SELECT id from users WHERE rcu='{}' );

-- ===== same above but the 'USER_ID' is rename 'inputed_by' and the value is replaced from 'farmer.USER_ID' value to 'users.name'
SELECT form_a_farmer_profiles.addr_region ,  form_a_farmer_profiles.farmer_name , users.name as `inputed_by`
   FROM `form_a_farmer_profiles`
    INNER JOIN  users  ON form_a_farmer_profiles.USER_ID = users.id
   WHERE USER_ID in 
      ( SELECT id from users WHERE rcu='RCU 11' );

-- ========================getting all form A via RCU=================================
SELECT
   form_a_farmer_profiles.*,
   form_a_farm_land.*
   
FROM 
   `form_a_farmer_profiles` 
INNER JOIN form_a_farm_land ON form_a_farmer_profiles.farmer_code = form_a_farm_land.farmer_code
WHERE
   form_a_farmer_profiles.USER_ID in (SELECT users.id from users where rcu="RCU 11");

-- ============================ GROUP ENUMERATORS BY encoded=========
SELECT 
   users.name as `key`,
   count(form_a_farmer_profiles.USER_ID) as `total`
FROM
   form_a_farmer_profiles
INNER JOIN users ON form_a_farmer_profiles.USER_ID = users.id
WHERE
   USER_ID in ( 
        SELECT users.id from users where rcu="RCU 11"
    )

GROUP by users.name
ORDER BY count(form_a_farmer_profiles.USER_ID) DESC;


-- ============FILTER SQL===================
SELECT addr_region, COUNT(addr_region) as 'num' FROM `form_a_farmer_profiles` 
         WHERE  USER_ID in ( SELECT id from users WHERE rcu='RCU 11' )  AND 
            (`farmer_primary_crop` LIKE '%coconut%' OR 
            `farmer_primary_crop` LIKE '%coffee%' OR 
            `farmer_dip_ref` LIKE '%NESTLE PLUS%' OR 
            `farmer_fo_name_rapid` LIKE '%BASCOFA%' OR 
            `farmer_sex` LIKE '%male%')
            GROUP BY addr_region;