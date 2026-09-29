import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ========== 解决matplotlib中文乱码 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.close("all")

# ========== 读取原始数据 + 抽样，降低内存压力 ==========
df = pd.read_csv("raw_data/淘宝用户行为.csv")
df = df.sample(n=300000, random_state=42)

# ====================== 1. 数据基础预处理 ======================
df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date
print("数据集基本信息：")
print(df.info())
print("-"*60)

# ====================== 2. DAU 日活跃用户图 ======================
dau = df.groupby("date")["user_id"].nunique().reset_index()
dau.columns = ["date", "dau"]

plt.figure(figsize=(12,5))
plt.plot(dau["date"], dau["dau"], color="#2E86AB", linewidth=2)
plt.title("淘宝APP日活跃用户DAU趋势")
plt.xlabel("日期")
plt.ylabel("活跃用户数")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("pic/dau_trend.png", dpi=300)
print("DAU图已保存至 pic/dau_trend.png")
print("-"*60)

# ====================== 3. 用户转化漏斗图 ======================
# behavior_type：1浏览，2收藏，3加购，4购买
funnel = []
step_name = ["浏览", "收藏", "加购", "购买"]
behavior_code = [1,2,3,4]
for code in behavior_code:
    cnt = df[df["behavior_type"] == code]["user_id"].nunique()
    funnel.append(cnt)

funnel_df = pd.DataFrame({
    "stage": step_name,
    "user_count": funnel
})
funnel_df["conversion_rate"] = funnel_df["user_count"] / funnel_df["user_count"].iloc[0]
funnel_df["step_rate"] = funnel_df["user_count"] / funnel_df["user_count"].shift(1)

print("====转化漏斗数据====")
print(funnel_df)

plt.figure(figsize=(10,6))
plt.barh(step_name, funnel, color=["#4878d0","#6acc64","#d65f5f","#c44e52"])
for i, v in enumerate(funnel):
    plt.text(v + 200, i, f"{v:,}", va="center")

plt.title("用户转化漏斗（浏览→收藏→加购→购买）")
plt.xlabel("独立用户数量")
plt.tight_layout()
plt.savefig("pic/funnel.png", dpi=300)
print("漏斗图已保存至 pic/funnel.png")
print("-"*60)

# ====================== 4. RFM 用户分层（改用pd.cut，彻底解决分箱重复报错） ======================
end_date = df["time"].max()
rfm = df.groupby("user_id").agg(
    Recency=("time", lambda x: (end_date - x.max()).days),
    Frequency=("behavior_type", "count"),
    Monetary=("behavior_type", lambda x: (x == 4).sum())
).reset_index()

# Recency：越小越好。R=2（最近活跃），R=1（很久没来）
rfm["R_score"] = pd.cut(
    rfm["Recency"],
    bins=[-1, 15, 1000],
    labels=[2, 1]
)

# Frequency 排名后切分
rfm["F_rank"] = rfm["Frequency"].rank(method="first")
rfm["F_score"] = pd.cut(
    rfm["F_rank"],
    bins=[0, rfm["F_rank"].median(), rfm["F_rank"].max()],
    labels=[1, 2]
)

# Monetary 排名后切分
rfm["M_rank"] = rfm["Monetary"].rank(method="first")
rfm["M_score"] = pd.cut(
    rfm["M_rank"],
    bins=[0, rfm["M_rank"].median(), rfm["M_rank"].max()],
    labels=[1, 2]
)

rfm["RFM_tag"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

def rfm_label(tag):
    if tag == "222":
        return "高价值用户"
    elif tag == "122":
        return "流失高价值用户"
    elif tag == "212":
        return "潜力用户"
    elif tag == "221":
        return "高活跃低消费用户"
    elif tag == "112":
        return "流失潜力用户"
    elif tag == "211":
        return "新用户"
    elif tag == "121":
        return "流失活跃用户"
    else:
        return "低价值沉睡用户"

rfm["user_segment"] = rfm["RFM_tag"].apply(rfm_label)
segment_stat = rfm["user_segment"].value_counts().reset_index()
segment_stat.columns = ["用户分层","用户数"]
print("====RFM用户分层统计====")
print(segment_stat)

plt.figure(figsize=(12,6))
plt.bar(segment_stat["用户分层"], segment_stat["用户数"], color="#5470C6")
plt.xticks(rotation=30)
plt.title("RFM用户分层分布")
plt.ylabel("用户数量")
plt.tight_layout()
plt.savefig("pic/rfm_segment.png", dpi=300)
print("RFM分层图已保存至 pic/rfm_segment.png")
print("-"*60)

# ====================== 5. 随机森林 用户流失预测模型 ======================
churn_days = 30
rfm["churn"] = (rfm["Recency"] >= churn_days).astype(int)

X = rfm[["Recency", "Frequency", "Monetary"]]
y = rfm["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
print("====随机森林分类报告====")
print(classification_report(y_test, y_pred))
print("====混淆矩阵====")
print(confusion_matrix(y_test, y_pred))

# 特征重要性可视化
feature_importance = pd.DataFrame({
    "feature": ["Recency(最近一次行为间隔)", "Frequency(行为总频次)", "Monetary(购买次数)"],
    "importance": rf_model.feature_importances_
}).sort_values("importance", ascending=False)

plt.figure(figsize=(8,5))
plt.barh(feature_importance["feature"], feature_importance["importance"], color="#7209B7")
plt.xlabel("特征重要性")
plt.title("用户流失预测 - 特征重要性")
plt.tight_layout()
plt.savefig("pic/feature_importance.png", dpi=300)
print("特征重要性图已保存至 pic/feature_importance.png")
print("\n✅ 全部代码执行完成！图片输出在 pic 文件夹下")
