# 产品数据与调用约定

predictions 的 pmf 为 [非负箱数,概率] 列表，代表 origin 时点对 target 的同一订舱需求分布；issued_at 不晚于 origin，known_at 才是入台时间。每个 product/origin/target 的 revision 独立更正；产品共享 sources 表示存在信息依赖，并不强制两个非相同分布必须使用相同权重。truth 的 target、known_at、revision 表示实况可见版本。每个回测 origin 只能使用当时可见的已成熟 truth 和预测，holdout_origins 不用于选权。新接口 POST /forecast-pool 接收 {case, as_of?, underbooking_cost?, overbooking_cost?}，返回 {snapshot, release, pooled, backtest, diagnostics}。release 包含来源/实况版本及训练窗口，pooled 必须是有效概率分布，复制一个完全相同且同上游的产品不应凭空改变聚合结果。

现有 GET /health、GET /cases 和 POST /preview 保留原有资料预览。新增 GET /study-cases 和 POST /study-preview {case} 已可用，只校验与描述 data/study 的资料；推断消费路由尚未实现。app.client.analysis 指向上文约定的新消费接口。所有 snapshot 都是相应原始资料字节的 SHA-256，输出仅使用有限 JSON 数值，无法判断用明确状态与 null 表达，不得返回 NaN。资料只供本地分析，不连接外部服务。

pooled 是记录列表，每项含 origin、target、pmf，pmf 与输入使用相同离散概率约定；没有足够共同支持时须在 diagnostics 交代回退。
