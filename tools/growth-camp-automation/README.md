# 思维成长训练营自动化工具

自动生成知识星球「思维成长训练营」每周内容。双轨制方案：OpenClaw Skill + 独立Python工具。

---

## 快速开始

### 方案A：OpenClaw Skill（推荐）

```bash
cd ~/.openclaw/skills/growth-camp-generator
python3 scripts/generate-issue.py --issue 11 --theme map_not_territory
```

### 方案B：独立Python工具

```bash
cd ~/tools/growth-camp-automation
python3 main.py --issue 11 --theme map_not_territory
```

---

## 安装依赖

**无需额外依赖**，仅需Python 3.6+标准库。

```bash
# 验证Python版本
python3 --version

# 如果提示缺少pathlib（Python 3.4以下）
pip3 install pathlib
```

---

## 可用主题

| 主题Key | 期数 | 主题名 | 核心模型 |
|---------|------|--------|----------|
| `map_not_territory` | 11 | 地图不是疆域 | The Map is Not the Territory |
| `probabilistic_thinking` | 12 | 概率思维 | Probabilistic Thinking |
| `compound_thinking` | 13 | 复利思维 | Compound Thinking |
| `systems_thinking` | 14 | 系统思维 | Systems Thinking |
| `critical_thinking` | 15 | 批判性思维 | Critical Thinking |
| `growth_mindset` | 16 | 成长型思维 | Growth Mindset |
| `opportunity_cost` | 17 | 机会成本 | Opportunity Cost |
| `survivorship_bias` | 18 | 幸存者偏差 | Survivorship Bias |
| `anchoring_effect` | 19 | 锚定效应 | Anchoring Effect |
| `loss_aversion` | 20 | 损失厌恶 | Loss Aversion |
| `confirmation_bias` | 21 | 确认偏误 | Confirmation Bias |

---

## 输出格式

生成的内容符合知识星球发布规范：

```markdown
# 第11期 - 地图不是疆域：为什么你总觉得地图就是世界？

> **核心概念**：地图不是疆域 (The Map is Not the Territory)
> **一句话**：你以为你在看世界，其实你在看地图。
> **完成时间**：约5分钟

---

[#📖](https://wx.zsxq.com/tags/...) 故事开场

[#🧠](https://wx.zsxq.com/tags/...) 思维模型

[#📝](https://wx.zsxq.com/tags/...) 本周行动任务

[#💬](https://wx.zsxq.com/tags/...) 讨论
```

---

## 如何扩展新主题

### 步骤1：在THEME_TEMPLATES中添加新主题

打开 `scripts/generate-issue.py` 或 `main.py`，在 `THEME_TEMPLATES` 字典中添加：

```python
"your_theme_key": {
    "theme_key": "中文主题名",
    "title": "吸引人的标题",
    "model": "模型名称 (英文)",
    "golden": "金句",
    "story": {
        "character": "角色身份",
        "context": "背景描述",
        "conflict": "冲突/困境",
        "epiphany": "顿悟时刻"
    },
    "core_logic": "核心逻辑一句话",
    "examples": [
        {"field1": "值1", "field2": "值2"}  # 根据案例类型调整字段
    ],
    "scenarios": ["场景1", "场景2"],
    "insights": ["洞察1", "洞察2", "洞察3"],
    "action_task": "任务名称",
    "action_steps": ["步骤1", "步骤2", "步骤3", "步骤4", "步骤5", "步骤6"],
    "discussion": ["问题1", "问题2", "问题3"],
    "next": "下一期主题key"
}
```

### 步骤2：测试生成

```bash
python3 scripts/generate-issue.py --issue 22 --theme your_theme_key --output test.md
cat test.md
```

### 步骤3：检查格式

- 标题格式是否正确
- emoji标签链接是否完整
- 表格是否对齐
- 段落长度是否适合移动端

---

## 常见问题

### Q: 生成的内容格式和已发布的不一致？

A: 检查模板中的标题格式是否为 `# 第N期 - 主题：副标题`，emoji标签是否包含完整链接。

### Q: 如何批量生成多期内容？

A: 写一个简单的shell脚本循环调用：

```bash
for i in 11 12 13; do
    python3 main.py --issue $i --theme map_not_territory
done
```

### Q: 可以集成AI自动生成吗？

A: 当前版本是硬编码模板。如需AI生成，可参考贴图号自动化工具的方案B架构，集成百炼API。

### Q: 如何归档已发布的内容？

A: 手动移动到 `growth-camp/published/phaseN/` 目录，或添加自动归档脚本。

---

## 文件结构

```
growth-camp-automation/
├── main.py              # 主脚本（方案B）
├── README.md            # 本文档
├── output/              # 输出目录
└── templates/           # 模板目录（预留）

~/.openclaw/skills/growth-camp-generator/
├── SKILL.md             # Skill定义（方案A）
├── scripts/
│   └── generate-issue.py # 生成脚本
└── references/          # 参考资料（预留）
```

---

## 版本历史

- v1.0 (2026-04-27): 初始版本，支持11个主题模板
- 待办：集成AI自动生成、HTML卡片输出、自动归档

---

**作者**: 小墨
**维护**: 老刘团队
**许可证**: 内部使用
