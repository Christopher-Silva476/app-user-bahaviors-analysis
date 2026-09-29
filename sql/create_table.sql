
USE ecommerce_user;

CREATE TABLE IF NOT EXISTS user_behavior (
    user_id BIGINT COMMENT '用户ID',
    item_id BIGINT COMMENT '商品ID',
    behavior_type TINYINT COMMENT '行为类型：1浏览，2收藏，3加购，4购买',
    user_geohash VARCHAR(50) COMMENT '用户地理哈希',
    item_category BIGINT COMMENT '商品类目ID',
    time DATETIME COMMENT '行为发生时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

