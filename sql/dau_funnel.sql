USE ecommerce_user;
-- 1. 每日DAU
SELECT
    DATE(time) AS dt,
    COUNT(DISTINCT user_id) AS dau
FROM user_behavior
GROUP BY dt
ORDER BY dt;

-- 2. 漏斗各环节独立用户数
SELECT
    CASE behavior_type
        WHEN 1 THEN '浏览'
        WHEN 2 THEN '收藏'
        WHEN 3 THEN '加购'
        WHEN 4 THEN '购买'
    END AS behavior_name,
    COUNT(DISTINCT user_id) AS user_cnt
FROM user_behavior
GROUP BY behavior_type
ORDER BY user_cnt DESC;

-- 3. 漏斗转化率
WITH funnel_data AS (
    SELECT
        behavior_type,
        COUNT(DISTINCT user_id) AS user_cnt
    FROM user_behavior
    GROUP BY behavior_type
)
SELECT
    CASE behavior_type
        WHEN 1 THEN '浏览'
        WHEN 2 THEN '收藏'
        WHEN 3 THEN '加购'
        WHEN 4 THEN '购买'
    END AS behavior_name,
    user_cnt,
    ROUND(user_cnt / (SELECT user_cnt FROM funnel_data WHERE behavior_type = 1), 4) AS conversion_rate
FROM funnel_data
ORDER BY behavior_type;
