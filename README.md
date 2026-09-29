# 电商用户行为数据分析
电商用户行为数据集，采用 Python + MySQL + PowerBI 完成完整用户分析。

## 项目简介
使用Python完成数据清洗、特征加工、RFM用户指标计算、用户流失标签构建；
MySQL存储数据，编写SQL查询用户活跃、转化、用户价值指标；
PowerBI搭建可视化仪表盘，完成DAU趋势、用户转化漏斗、RFM用户分层可视化。

## 项目结构
app_user_behaviors_analysis/
├─ raw_data/          # 原始数据集，大文件不上传
├─ clean_data/        # Python 清洗后的中间数据，不上传
├─ powerbi/           # PowerBI 工程文件与仪表盘截图
│  ├─ ecommerce_analysis.pbix
│  └─ pics/
├─ analysis.py        # Python：数据清洗、RFM、流失特征计算
├─ mysql_script.sql   # MySQL 建表、业务查询 SQL 脚本
├─ requirements.txt   # Python 依赖包
└─ .gitignore         # Git 忽略配置



## 分析流程
1. 数据预处理（Python）
   - 缺失值、异常时间过滤、重复记录剔除
   - 计算R/F/M指标，给用户打流失标签
   - 输出清洗后的数据集到clean_data

2. 数据存储与指标查询（MySQL）
   - 建表导入原始用户行为数据
   - SQL统计DAU、各环节用户量、RFM基础指标

3. 可视化仪表盘（PowerBI）
   - DAU日活跃趋势折线图
   - 浏览→收藏→加购→购买转化漏斗
   - RFM用户分层分布饼图/柱状图

## 环境部署
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
