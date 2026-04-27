#!/usr/bin/env python3
"""
思维成长训练营内容生成脚本 - 修正版
修复格式一致性：标题格式 + emoji标签链接
"""

import argparse
from pathlib import Path

THEME_TEMPLATES = {
    "map_not_territory": {
        "theme_key": "地图不是疆域",
        "title": "为什么你总觉得地图就是世界？",
        "model": "地图不是疆域 (The Map is Not the Territory)",
        "golden": "你以为你在看世界，其实你在看地图。",
        "story": {
            "character": "老周，公司战略总监",
            "context": "他有一个习惯：做决策前必看数据报表。",
            "conflict": "市场变化太快，数据总是滞后。按报表做的决策，次次踩空。",
            "epiphany": "顾问说了一句话：你的报表是地图，市场是疆域。地图再精确，也不是真实的地形。"
        },
        "core_logic": "所有模型都是对现实的简化，必然遗漏重要信息。当你把模型当现实本身，就会犯错。",
        "examples": [
            {"map": "KPI考核表", "territory": "员工真实贡献"},
            {"map": "用户画像", "territory": "活生生的人"},
            {"map": "财务报表", "territory": "公司真实健康状况"},
            {"map": "SWOT分析", "territory": "复杂的市场环境"}
        ],
        "scenarios": ["看数据做决策时", "用模型评估人时", "战略规划时", "任何你觉得事情就是这样的时刻"],
        "insights": [
            "模型越精确，不代表越接近真相",
            "好地图的价值在于有用，不在于真实",
            "真正的高手，知道地图哪里不完整"
        ],
        "action_task": "地图不是疆域练习",
        "action_steps": [
            "选一个你最近做的决定",
            "问自己：我在用地图还是疆域思考？",
            "列出你忽略的信息",
            "找一个不同观点的人，听他说10分钟",
            "根据新信息，更新你的判断",
            "写下：我原来以为...现在我认为..."
        ],
        "discussion": [
            "你有过一次发现地图不是疆域的经历吗？",
            "你现在最可能在用什么简化模型看世界？",
            "分享一个你更新认知的经历"
        ],
        "next": "概率思维"
    },
    "probabilistic_thinking": {
        "theme_key": "概率思维",
        "title": "为什么你总是用对错看世界？",
        "model": "概率思维 (Probabilistic Thinking)",
        "golden": "世界不是非黑即白，是灰度的概率分布。",
        "story": {
            "character": "小陈，连续创业者",
            "context": "他做决策的方式：要么all in，要么放弃。",
            "conflict": "第一次创业，all in失败，亏了200万。第二次，不敢投，错过风口。",
            "epiphany": "投资人说：你不是在赌对错，你是在算概率。"
        },
        "core_logic": "没有100%确定的事。高手不做对错判断，他们计算概率和期望值。",
        "examples": [
            {"scenario": "创业", "binary": "成功或失败", "probabilistic": "成功率30%，但期望值是正的"},
            {"scenario": "跳槽", "binary": "跳还是不跳", "probabilistic": "70%更好，30%更糟，算期望值"},
            {"scenario": "投资", "binary": "涨还是跌", "probabilistic": "上涨概率60%，预期收益多少？"}
        ],
        "scenarios": ["创业决策", "投资选择", "职业转型", "任何二选一的困境"],
        "insights": [
            "对错思维让你赌，概率思维让你算",
            "高手不是看对了，是算准了",
            "贝叶斯更新：新信息来了，更新概率，不是推翻一切"
        ],
        "action_task": "概率思维练习",
        "action_steps": [
            "选一个你面临的选择（创业/跳槽/投资）",
            "列出每个选项的成功概率和失败概率",
            "计算每个选项的期望值（概率x收益）",
            "问自己：如果失败10次，我还能承受吗？",
            "根据期望值，而不是直觉，做决定",
            "写下：我选这个因为期望值是..."
        ],
        "discussion": [
            "你有过一次用对错思维做决定，结果踩坑的经历吗？",
            "你现在面临的最需要用概率思维的选择是什么？",
            "分享一个你算对概率、做对决定的案例"
        ],
        "next": "复利思维"
    },
    "compound_thinking": {
        "theme_key": "复利思维",
        "title": "为什么每天进步1%这么可怕？",
        "model": "复利思维 (Compound Thinking)",
        "golden": "复利是世界第八大奇迹。",
        "story": {
            "character": "小林，普通上班族",
            "context": "他想快速成功，总找捷径。",
            "conflict": "学了10门课，读了50本书，三年后还是原地踏步。",
            "epiphany": "导师说：你不是学得不够多，是你没有让知识复利。"
        },
        "core_logic": "每天进步1%，一年后是37倍。复利的关键不是速度，是持续性和方向一致。",
        "examples": [
            {"area": "学习", "linear": "每天学1小时，一年365小时", "compound": "每天复习+新增，知识网络指数增长"},
            {"area": "健身", "linear": "偶尔练一次", "compound": "每天15分钟，一年后体质质变"},
            {"area": "写作", "linear": "等灵感来了再写", "compound": "每天写300字，一年后出书"}
        ],
        "scenarios": ["学习新技能", "健康管理", "财富积累", "人际关系"],
        "insights": [
            "复利前期几乎看不到效果，后期爆发",
            "方向比速度重要，持续性比强度重要",
            "中断是复利的最大敌人"
        ],
        "action_task": "复利思维练习",
        "action_steps": [
            "选一个你想长期投入的领域",
            "设计一个每天只需15分钟的最小行动",
            "确保今天的行动能叠加在昨天的基础上",
            "记录第1天、第7天、第30天的进展",
            "找到至少一个可以复利的杠杆点",
            "写下：我的复利公式是..."
        ],
        "discussion": [
            "你有过一次体验过复利效应的经历吗？",
            "你现在哪个领域最需要复利思维？",
            "分享一个你坚持下来并看到复利效果的习惯"
        ],
        "next": "系统思维"
    },
    "systems_thinking": {
        "theme_key": "系统思维",
        "title": "为什么你总是治标不治本？",
        "model": "系统思维 (Systems Thinking)",
        "golden": "问题不在表面，在系统结构里。",
        "story": {
            "character": "老张，部门经理",
            "context": "团队效率低，他不断加人手、定KPI。",
            "conflict": "人越多，沟通成本越高，效率反而更低。",
            "epiphany": "顾问画了一张图：问题不在人少，在流程结构。"
        },
        "core_logic": "系统是相互连接的要素组成的整体。改变单个要素没用，要改变连接方式和反馈回路。",
        "examples": [
            {"problem": "团队效率低", "surface_fix": "加人手", "system_fix": "优化协作流程"},
            {"problem": "客户流失", "surface_fix": "打折促销", "system_fix": "改善产品体验"},
            {"problem": "体重反弹", "surface_fix": "节食", "system_fix": "改变生活习惯系统"}
        ],
        "scenarios": ["管理团队", "解决复杂问题", "个人成长瓶颈", "商业决策"],
        "insights": [
            "短期有效的方案，长期可能有害",
            "系统中的延迟反馈让人误判",
            "杠杆点往往在最不起眼的地方"
        ],
        "action_task": "系统思维练习",
        "action_steps": [
            "选一个你反复出现的问题",
            "画出这个问题的因果关系图",
            "找出至少3个相互影响的要素",
            "识别正反馈回路和负反馈回路",
            "找到一个高杠杆的干预点",
            "写下：我原来的解法是...系统的解法是..."
        ],
        "discussion": [
            "你有过一次治标不治本的经历吗？",
            "你现在哪个问题是系统性的？",
            "分享一个你用系统思维解决问题的案例"
        ],
        "next": "批判性思维"
    },
    "critical_thinking": {
        "theme_key": "批判性思维",
        "title": "为什么你总是轻信别人说的？",
        "model": "批判性思维 (Critical Thinking)",
        "golden": "怀疑不是否定，是独立思考的开始。",
        "story": {
            "character": "小王，刚入职场的年轻人",
            "context": "他相信专家、相信权威、相信热搜。",
            "conflict": "被割韭菜三次，才发现那些'专家'都在卖课。",
            "epiphany": "前辈说：你要学会问'证据在哪里？'"
        },
        "core_logic": "批判性思维不是挑刺，是对信息的来源、证据、逻辑进行系统性检验。",
        "examples": [
            {"claim": "这个产品销量第一", "question": "谁统计的？样本多大？", "insight": "数据来源可疑"},
            {"claim": "专家说这样最好", "question": "哪个专家？有什么利益关联？", "insight": "权威不等于正确"},
            {"claim": "大家都这么做", "question": "大家是谁？有独立思考吗？", "insight": "从众不等于合理"}
        ],
        "scenarios": ["看新闻", "做投资决策", "听别人建议", "评估产品宣传"],
        "insights": [
            "越是情绪化的内容，越需要冷静分析",
            "相关性不等于因果性",
            "沉默的证据往往最重要"
        ],
        "action_task": "批判性思维练习",
        "action_steps": [
            "选一个你最近相信的观点",
            "问自己：证据在哪里？来源可靠吗？",
            "找出至少一个反例或反面论证",
            "检查有没有逻辑谬误（因果倒置、以偏概全等）",
            "换一个立场重新审视这个观点",
            "写下：我原来的看法是...经过批判性思考后..."
        ],
        "discussion": [
            "你有过一次被误导的经历吗？",
            "你现在最怀疑的一个流行观点是什么？",
            "分享一个你用批判性思维识破谎言的案例"
        ],
        "next": "成长型思维"
    },
    "growth_mindset": {
        "theme_key": "成长型思维",
        "title": "为什么你总是说'我不行'？",
        "model": "成长型思维 (Growth Mindset)",
        "golden": "能力不是固定的，是可以成长的。",
        "story": {
            "character": "小李，内向的技术人员",
            "context": "他觉得自己的性格改不了，不适合做管理。",
            "conflict": "拒绝晋升机会，觉得自己'天生不行'。",
            "epiphany": "mentor说：你不是不行，你只是还没学会。"
        },
        "core_logic": "固定型思维认为能力是天生的，成长型思维认为能力可以通过努力和学习提升。",
        "examples": [
            {"fixed": "我数学不好", "growth": "我还没掌握数学方法"},
            {"fixed": "我不擅长社交", "growth": "我可以练习沟通技巧"},
            {"fixed": "我太老了学不会", "growth": "学习方法比年龄重要"}
        ],
        "scenarios": ["面对挑战", "接受批评", "看到别人成功", "遭遇失败"],
        "insights": [
            "'还不行'比'不行'多了一个可能性",
            "努力不是耻辱，是成长的必经之路",
            "失败不是定义，是反馈"
        ],
        "action_task": "成长型思维练习",
        "action_steps": [
            "列出三个你说'我不行'的事情",
            "把每个'我不行'改成'我还没学会'",
            "为每个'还没学会'设计一个学习计划",
            "找一个已经做到的人，请教他的学习路径",
            "设定一个30天的微进步目标",
            "写下：我从固定型思维转向成长型思维的转变是..."
        ],
        "discussion": [
            "你有过一次从'我不行'到'我可以'的转变吗？",
            "你现在哪个领域最需要成长型思维？",
            "分享一个你通过努力突破自我的经历"
        ],
        "next": "机会成本"
    },
    "opportunity_cost": {
        "theme_key": "机会成本",
        "title": "为什么你总觉得'反正都花了'？",
        "model": "机会成本 (Opportunity Cost)",
        "golden": "选择的代价，是你放弃的那个选项。",
        "story": {
            "character": "老赵，中年职场人",
            "context": "他在一个没前景的行业干了10年。",
            "conflict": "想转行但舍不得10年的积累，继续耗着。",
            "epiphany": "朋友问：你再干10年，失去的是什么？"
        },
        "core_logic": "每个选择都有成本，成本不是你付出的，是你放弃的。沉没成本不应影响未来决策。",
        "examples": [
            {"choice": "继续做不喜欢的工作", "cost": "失去探索新领域的10年"},
            {"choice": "维持一段糟糕的关系", "cost": "失去遇到合适的人的机会"},
            {"choice": "死守亏损的投资", "cost": "失去投资其他项目的资金"}
        ],
        "scenarios": ["职业选择", "投资决策", "人际关系", "时间分配"],
        "insights": [
            "沉没成本不是成本，是历史",
            "最大的成本往往是看不见的",
            "不选择也是一种选择，也有成本"
        ],
        "action_task": "机会成本练习",
        "action_steps": [
            "选一个你正在犹豫的决定",
            "列出你选择A的成本（放弃B的收益）",
            "列出你选择B的成本（放弃A的收益）",
            "问自己：如果我今天从零开始，我会选哪个？",
            "忽略已经投入的时间/金钱/精力",
            "写下：我选择X，因为我愿意放弃Y"
        ],
        "discussion": [
            "你有过一次被沉没成本困住的经历吗？",
            "你现在哪个决定最难做？机会成本是什么？",
            "分享一个你勇敢放弃、获得更大收益的案例"
        ],
        "next": "幸存者偏差"
    },
    "survivorship_bias": {
        "theme_key": "幸存者偏差",
        "title": "为什么你总是模仿成功者？",
        "model": "幸存者偏差 (Survivorship Bias)",
        "golden": "你看到的成功者，只是幸存下来的少数。",
        "story": {
            "character": "小张， aspiring entrepreneur",
            "context": "他读了100本成功学书籍，模仿大佬的做法。",
            "conflict": "照搬马云、马斯克的方法，结果屡战屡败。",
            "epiphany": "导师说：你只看到了幸存者，没看到死者。"
        },
        "core_logic": "我们只能看到成功的案例，失败的案例消失了。模仿幸存者可能恰恰是失败的原因。",
        "examples": [
            {"success_story": "辍学创业成功", "hidden_truth": "99%辍学创业的人失败了"},
            {"success_story": "All in一支股票赚了", "hidden_truth": "All in的人大多破产了"},
            {"success_story": "每天工作18小时成功", "hidden_truth": "更多人因此健康崩溃"}
        ],
        "scenarios": ["学习成功经验", "投资决策", "职业规划", "商业策略"],
        "insights": [
            "成功者的建议可能是他们成功的障碍",
            "失败者的教训比成功者的经验更有价值",
            "运气在成功中的比重远超想象"
        ],
        "action_task": "幸存者偏差练习",
        "action_steps": [
            "选一个你想模仿的成功案例",
            "去找至少3个同样做法但失败的人",
            "分析幸存者和失败者的差异",
            "问自己：这个成功有多少是运气？",
            "找出这个案例中被忽略的关键变量",
            "写下：我学到的不是'怎么做'，而是'什么情况下不能这么做'"
        ],
        "discussion": [
            "你有过一次盲目模仿成功者却失败的经历吗？",
            "你现在最想去模仿谁？幸存者偏差风险在哪？",
            "分享一个你从失败案例中学到更多的经历"
        ],
        "next": "锚定效应"
    },
    "anchoring_effect": {
        "theme_key": "锚定效应",
        "title": "为什么你总是被第一个数字困住？",
        "model": "锚定效应 (Anchoring Effect)",
        "golden": "第一个信息，决定了你所有的判断。",
        "story": {
            "character": "小刘，购物达人",
            "context": "她看到一个商品标价999，打折到499。",
            "conflict": "觉得赚大了，买回家后发现根本不需要。",
            "epiphany": "朋友说：如果没有999这个锚，你会觉得499便宜吗？"
        },
        "core_logic": "人们在做判断时，过度依赖接收到的第一个信息（锚点），后续调整不足。",
        "examples": [
            {"scenario": "工资谈判", "anchor": "HR先报价", "effect": "你的还价围绕这个数字"},
            {"scenario": "买房", "anchor": "挂牌价", "effect": "成交价围绕挂牌价波动"},
            {"scenario": "评估能力", "anchor": "第一印象", "effect": "后续表现难以改变初始评价"}
        ],
        "scenarios": ["价格谈判", "绩效评估", "投资决策", "日常消费"],
        "insights": [
            "锚点可以是完全无关的数字",
            "知道自己被锚定，也难以摆脱",
            "最好的防御是自己先设锚"
        ],
        "action_task": "锚定效应练习",
        "action_steps": [
            "回想一个你最近做的价格相关决定",
            "问自己：我被哪个数字锚定了？",
            "尝试从零开始评估真实价值",
            "在下一次谈判中，争取先报价（自己设锚）",
            "找一个完全没有锚点的场景做对比",
            "写下：我原来的判断是...去掉锚点后我的判断是..."
        ],
        "discussion": [
            "你有过一次被锚定效应影响的经历吗？",
            "你现在哪个决定可能被锚定了？",
            "分享一个你成功摆脱锚定的案例"
        ],
        "next": "损失厌恶"
    },
    "loss_aversion": {
        "theme_key": "损失厌恶",
        "title": "为什么你害怕失去胜过渴望得到？",
        "model": "损失厌恶 (Loss Aversion)",
        "golden": "失去100块的痛苦，大于得到100块的快乐。",
        "story": {
            "character": "老王，资深股民",
            "context": "他持有一只亏损的股票两年了。",
            "conflict": "明知该止损，但舍不得'割肉'，越亏越多。",
            "epiphany": "分析师说：你不是在持有股票，你是在持有痛苦。"
        },
        "core_logic": "人对损失的敏感度远高于收益。为了避免损失，人们会做出非理性决策。",
        "examples": [
            {"scenario": "股票止损", "rational": "该卖就卖", "loss_aversion": "再等等，万一涨回来"},
            {"scenario": "跳槽", "rational": "新机会更好", "loss_aversion": "万一新工作不如现在呢"},
            {"scenario": "断舍离", "rational": "不用的东西扔掉", "loss_aversion": "万一以后用得上呢"}
        ],
        "scenarios": ["投资决策", "职业选择", "清理物品", "结束关系"],
        "insights": [
            "损失厌恶让人抱残守缺",
            "框架效应：把'损失'重新框架为'释放'",
            "预设规则可以克服情绪干扰"
        ],
        "action_task": "损失厌恶练习",
        "action_steps": [
            "列出一个你迟迟不愿放弃的东西/关系/投资",
            "问自己：如果我现在没有它，我会花钱买它吗？",
            "计算继续持有的真实成本",
            "设定一个明确的退出标准（提前预设）",
            "想象你已经放弃了，感受那种轻松",
            "写下：我放弃X，因为我获得了Y"
        ],
        "discussion": [
            "你有过一次因为损失厌恶而吃亏的经历吗？",
            "你现在哪个决定被损失厌恶影响了？",
            "分享一个你成功克服损失厌恶的案例"
        ],
        "next": "确认偏误"
    },
    "confirmation_bias": {
        "theme_key": "确认偏误",
        "title": "为什么你只看自己想看的？",
        "model": "确认偏误 (Confirmation Bias)",
        "golden": "你不是在寻找真相，你是在寻找认同。",
        "story": {
            "character": "小美，养生爱好者",
            "context": "她相信某种保健品有效。",
            "conflict": "只收集有效的案例，忽略无效的反例。",
            "epiphany": "医生说：你看到的不是证据，是你的信念过滤器。"
        },
        "core_logic": "人们倾向于寻找、解释和记住支持自己已有信念的信息，忽略相反的证据。",
        "examples": [
            {"belief": "这个投资会涨", "bias_behavior": "只看利好消息，忽略利空"},
            {"belief": "这个人不可信", "bias_behavior": "只注意他的缺点，忽略优点"},
            {"belief": "这个方法有效", "bias_behavior": "只记住成功案例，忘记失败案例"}
        ],
        "scenarios": ["投资决策", "人际判断", "健康选择", "政治观点"],
        "insights": [
            "算法加剧了确认偏误（信息茧房）",
            "主动寻找反面证据是解毒剂",
            "承认自己可能错是智慧的开始"
        ],
        "action_task": "确认偏误练习",
        "action_steps": [
            "选一个你坚信的观点",
            "主动搜索至少3个反面证据",
            "认真读一遍，不要反驳",
            "问自己：如果我是错的，会怎样？",
            "找一个持相反观点的人，真诚交流",
            "写下：我原来的信念是...看到反面证据后..."
        ],
        "discussion": [
            "你有过一次被确认偏误误导的经历吗？",
            "你现在哪个观点可能需要反面证据？",
            "分享一个你主动推翻自己信念的经历"
        ],
        "next": "汉隆剃刀"
    }
}

# Tags for 知识星球
TAG_BOOK = "[#\U0001f4d6](https://wx.zsxq.com/tags/%F0%9F%93%96/15442551812522)"
TAG_BRAIN = "[#\U0001f9e0](https://wx.zsxq.com/tags/%F0%9F%A7%A0/48554882124848)"
TAG_NOTE = "[#\U0001f4dd](https://wx.zsxq.com/tags/%F0%9F%93%9D/88225884145852)"
TAG_CHAT = "[#\U0001f4ac](https://wx.zsxq.com/tags/%F0%9F%92%AC/51552114842124)"


def generate_content(issue_num, theme_key):
    if theme_key not in THEME_TEMPLATES:
        return None

    t = THEME_TEMPLATES[theme_key]
    NL = "\n"

    story = NL.join([
        t['story']['character'],
        "",
        t['story']['context'],
        "",
        t['story']['conflict'],
        "",
        t['story']['epiphany'],
        "",
        "他不是不聪明，他是被困在了自己的思维模式里。"
    ])

    examples_md = ""
    if "map" in t['examples'][0]:
        examples_md = "| 地图 | 疆域 |" + NL + "|------|------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['map'] + " | " + ex['territory'] + " |" + NL
    elif "linear" in t['examples'][0]:
        examples_md = "| 领域 | 线性思维 | 复利思维 |" + NL + "|------|---------|---------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['area'] + " | " + ex['linear'] + " | " + ex['compound'] + " |" + NL
    elif "fixed" in t['examples'][0]:
        examples_md = "| 固定型思维 | 成长型思维 |" + NL + "|-----------|-----------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['fixed'] + " | " + ex['growth'] + " |" + NL
    elif "success_story" in t['examples'][0]:
        examples_md = "| 成功故事 | 隐藏的真相 |" + NL + "|---------|-----------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['success_story'] + " | " + ex['hidden_truth'] + " |" + NL
    elif "scenario" in t['examples'][0] and "anchor" in t['examples'][0]:
        examples_md = "| 场景 | 锚点 | 效应 |" + NL + "|------|------|------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['scenario'] + " | " + ex['anchor'] + " | " + ex['effect'] + " |" + NL
    elif "rational" in t['examples'][0]:
        examples_md = "| 场景 | 理性决策 | 损失厌恶 |" + NL + "|------|---------|---------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['scenario'] + " | " + ex['rational'] + " | " + ex['loss_aversion'] + " |" + NL
    elif "belief" in t['examples'][0]:
        examples_md = "| 信念 | 偏误行为 |" + NL + "|------|---------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['belief'] + " | " + ex['bias_behavior'] + " |" + NL
    else:
        examples_md = "| 场景 | 对错思维 | 概率思维 |" + NL + "|------|---------|---------|" + NL
        for ex in t['examples']:
            examples_md += "| " + ex['scenario'] + " | " + ex['binary'] + " | " + ex['probabilistic'] + " |" + NL

    scenarios_text = NL.join("- " + s for s in t['scenarios'])
    insights_text = NL.join("- " + i for i in t['insights'])
    steps_text = NL.join(str(i+1) + ". " + s for i, s in enumerate(t['action_steps']))
    discussion_text = NL.join(str(i+1) + ". " + d for i, d in enumerate(t['discussion']))

    content = NL.join([
        "# 第" + str(issue_num) + "期 - " + t['theme_key'] + "：" + t['title'],
        "",
        "> **核心概念**：" + t['model'],
        "> **一句话**：" + t['golden'],
        "> **完成时间**：约5分钟",
        "",
        "---",
        "",
        TAG_BOOK + " 故事开场",
        "",
        story,
        "",
        TAG_BRAIN + " 思维模型",
        "",
        "##核心逻辑",
        "",
        t['core_logic'],
        "",
        "##经典案例",
        "",
        examples_md,
        "##适用场景",
        scenarios_text,
        "",
        "##反常识洞察",
        insights_text,
        "",
        TAG_NOTE + " 本周行动任务",
        "",
        "任务：" + t['action_task'],
        "",
        steps_text,
        "",
        "完成标准：完成6步以上，并在评论区分享",
        "",
        "截止时间：周日24:00",
        "",
        TAG_CHAT + " 讨论",
        "",
        discussion_text,
        "",
        "欢迎在评论区分享！",
        "",
        "下期预告：第" + str(issue_num+1) + "期 \u2014 " + t['next']
    ])

    return content


def main():
    parser = argparse.ArgumentParser(description='思维成长训练营内容生成器')
    parser.add_argument('--issue', type=int, required=True, help='期数')
    parser.add_argument('--theme', type=str, required=True, help='主题key')
    parser.add_argument('--output', type=str, help='输出路径')
    args = parser.parse_args()

    content = generate_content(args.issue, args.theme)
    if not content:
        print("未知主题: " + args.theme)
        print("可用主题: " + ", ".join(THEME_TEMPLATES.keys()))
        return

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path("output/第" + str(args.issue) + "期-" + args.theme + ".md")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    print("已生成: " + str(out_path))
    print("第" + str(args.issue) + "期: " + args.theme)


if __name__ == '__main__':
    main()
