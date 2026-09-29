USE ecommerce_user;
WITH user_last_date AS (
    SELECT MAX(DATE(time)) AS max_date FROM user_behavior
)
SELECT
    ub.user_id,
    DATEDIFF((SELECT max_date FROM user_last_date), MAX(DATE(ub.time))) AS R,
    COUNT(ub.time) AS F,
    SUM(CASE WHEN ub.behavior_type = 4 THEN 1 ELSE 0 END) AS M
FROM user_behavior ub
GROUP BY ub.user_id;
