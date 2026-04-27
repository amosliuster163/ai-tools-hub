---
name: growth-camp-generator
description: Generate 思维成长训练营 content for 知识星球. Each issue includes: story, mental model, action tasks, and discussion questions. Use when user asks to create 思维成长训练营内容, 知识星球weekly, or 思维模型文章. Triggers on: "思维成长训练营", "成长训练营", "知识星球内容", "思维模型文章", "第N期内容".
---

# Growth Camp Generator

Generate weekly mental model content for 知识星球 "思维成长训练营".

## Quick Start

### Scheme A: OpenClaw Skill (Built-in AI)
```bash
# Generate issue with built-in AI
python3 scripts/generate-issue.py --issue 11 --theme "地图不是疆域"
```

### Scheme B: Standalone Python Tool
```bash
cd ~/tools/growth-camp-automation
python3 main.py --issue 11 --theme "地图不是疆域"
```

## Content Structure (Fixed)

Each issue follows the exact format from published issues 1-10:

| Section | Ratio | Content |
|---------|-------|---------|
| 📖 Story | 20% | Character story with conflict and epiphany |
| 🧠 Mental Model | 30% | Core logic, examples table, scenarios, counter-intuitive insights |
| 📝 Action Task | 30% | 5-6 step actionable exercise with deadline |
| 💬 Discussion | 20% | 3 discussion questions |

## Published Issues (1-10)

| Issue | Theme | Mental Model |
|-------|-------|-------------|
| 1 | 为什么越无知的人越自信？ | 达克效应 |
| 2 | 为什么有能力的人总觉得"我不配"？ | 冒名顶替综合症 |
| 3 | 为什么你只看自己想看的？ | 确认偏误 |
| 4 | 为什么你不敢改变？ | 舒适区理论 |
| 5 | 如何像Elon Musk一样思考？ | 第一性原理 |
| 6 | 为什么你总觉得"他是故意的"？ | 汉隆剃刀 |
| 7 | 为什么你害怕失去胜过渴望得到？ | 损失厌恶 |
| 8 | 为什么你控制不了情绪？ | 情绪推理 |
| 9 | 如何进入高度专注的状态？ | 心流理论 |
| 10 | 如何像高手一样做决策？ | 二阶思维 |

## Pending Issues

| Issue | Theme | Mental Model |
|-------|-------|-------------|
| 11 | 为什么你总觉得"地图就是世界"？ | 地图不是疆域 |
| 12 | 如何用概率思维做决策？ | 概率思维 |

## Output Format

- 知识星球 Markdown format
- Use emoji dividers: 📖 🧠 📝 💬
- Include tables for comparison examples
- Blockquotes for golden quotes
- Short paragraphs (mobile-friendly)
- Next issue preview at end

## File Organization

```
growth-camp/
├── draft/                  # Drafts
│   └── 第N期-主题-模型.md
├── published/              # Published
│   └── phaseN/
└── templates/              # Templates
```

## Quality Checklist

Before publishing:
- [ ] Story has character, conflict, epiphany
- [ ] Mental model has: core logic + examples table + scenarios + insights
- [ ] Action task is specific (5-6 steps) with deadline
- [ ] 3 discussion questions
- [ ] 1-2 golden quotes
- [ ] Format matches published issues 1-10
- [ ] Next issue preview included
- [ ] No duplicate with published issues
