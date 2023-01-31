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

-- =========================================================



