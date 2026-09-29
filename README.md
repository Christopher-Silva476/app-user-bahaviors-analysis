# APP 用户行为数据分析
APP 用户行为数据分析项目 | 漏斗转化、留存分析、RFM 用户分群、Python + SQL + PowerBI可视化

## 📖 项目简介
本项目基于APP用户行为日志，完成从原始数据清洗、SQL指标计算、Python建模分析，到PowerBI可视化报表搭建全流程。
核心分析目标：
1. 构建用户转化漏斗，分析各环节流失情况
2. RFM模型对用户进行价值分层，实现用户分群运营
3. 统计DAU时序变化，观察用户活跃度趋势
4. 挖掘特征重要性，定位影响用户留存的关键因素

## 📁 项目结构
app_user_behaviors_analysis/
├── raw_data/            # 原始数据集
├── clean_data/          # Python 清洗后的中间数据
├── power bi/            # PowerBI 工程文件 pbix
├── pic/                 # 可视化导出图片
├── analysis.py          # Python：数据清洗、RFM、流失特征计算
├── sql/                 # MySQL 建表、业务查询 SQL 脚本
├── .gitignore           # Git 忽略配置
├── LICENSE
|—— requirements.txt
└── README.md


## 🛠️ 技术栈
- 编程语言：Python（pandas, matplotlib, seaborn, scikit-learn）
- 数据库：MySQL
- 可视化：Matplotlib、PowerBI Desktop
- 版本管理：Git & GitHub

## 📊 PowerBI 可视化看板
PowerBI报表位于 `power bi/` 目录，包含3张核心图表：
1. 用户DAU日活跃时序折线图
2. APP用户行为转化漏斗图
3. RFM用户价值分群气泡散点图

## 🚀 项目运行说明
1. 将`raw_data`内原始数据导入MySQL，执行`sql/create_table.sql`建表
2. 运行sql目录下脚本，计算漏斗指标、RFM基础指标
3. 执行`analysis.py`完成数据建模、RFM分群与绘图
4. 使用PowerBI Desktop打开pbix文件，加载清洗后数据，查看交互式可视化看板

## ✨ 项目亮点
- 完整数据分析链路：原始数据 → SQL计算指标 → Python建模 → PowerBI交互式可视化
- 可直接用于数据分析岗简历项目，覆盖SQL、Python、BI三大高频考察技能
- 可复现，代码、数据、报表全部开源

## 📄 License
MIT License


