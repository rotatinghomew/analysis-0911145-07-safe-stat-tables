# 产品数据与调用约定

cells 是待发布统计格，expression 为基础变量的线性组合，value 已由现有汇总计算器生成。constraints 使用 lower/upper；bounds 描述业务允许的非负范围。protected 指定需要保护的线性量及 minimum_width，均为模拟披露策略，不声称满足通用隐私定义。archive 的公开值无法撤销，scope 不同的等式只能按其真实变量关系使用。POST /publish {case, table_ids?} 返回 {snapshot, released, suppressed, ranges, status, diagnostics}。status 为 safe/infeasible/already_disclosed；safe 须对所有保护量给出可核验上下界且保留集合满足共同可行性。不得把私有基础变量或完整未抑制值夹入公开导出。

当前 GET /cases、POST /preview 和 GET /health 已可用；client.analysis 是待接入的业务消费调用，新分析路由尚不存在。原始数据通过 app.store 读取，snapshot 为输入字节的 SHA-256。新增接口须保留现有预览能力和 JSON 有限数值约定。

suppressed 只列格子标识，不得携带其真实 value；released 只包含实际公开格。ranges 面向内部保护审查，不应把私有实际值塞进公开文件。archive 的上一月变量不等于本月同名商户变量。
