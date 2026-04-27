# CC Switch 使用指南：在 Claude Code 中自由切换模型

> 一个跨平台的桌面工具，让你在 Claude Code、Codex、OpenCode 等 AI 编程工具中一键切换不同的模型提供商。

---

## 目录

1. [CC Switch 是什么](#1-cc-switch-是什么)
2. [支持的模型提供商](#2-支持的模型提供商)
3. [安装](#3-安装)
4. [配置提供商](#4-配置提供商)
5. [使用方式](#5-使用方式)
6. [常见问题](#6-常见问题)
7. [Mac Mini 配置指南](#7-mac-mini-配置指南)

---

## 1. CC Switch 是什么

CC Switch 是一个开源桌面工具（GitHub: [farion1231/cc-switch](https://github.com/farion1231/cc-switch)），它可以管理多个 **API 提供商配置**，让你在 Claude Code 中一键切换不同的模型。

**核心功能：**
- 管理多个模型提供商的 API Key 和 Endpoint
- 一键切换当前使用的模型
- 支持 Claude Code、Codex、OpenCode、Gemini CLI 等多个 CLI 工具
- 跨平台（Windows / macOS / Linux）

---

## 2. 支持的模型提供商

经过实测验证，以下提供商可以正常配合 CC Switch 使用：

| 提供商 | Anthropic 兼容 Endpoint | 推荐模型 | 备注 |
|--------|------------------------|----------|------|
| **阿里云百炼** | `coding.dashscope.aliyuncs.com/apps/anthropic` | qwen3.5-plus / qwen3.6-plus | 需开通百炼 Coding Plan |
| **MiniMax** | `api.minimaxi.com/anthropic` | MiniMax-M2.7 | 需申请 API Key |
| **DeepSeek** | `api.deepseek.com/anthropic` | deepseek-v4-flash | 价格极低，需账户有余额 |

> **原理说明：** Claude Code 底层使用 Anthropic SDK，只能连接 Anthropic 格式的 API 接口。上述提供商都提供了 **Anthropic 兼容接口**（在原有 OpenAI 接口之外额外提供的），所以才能正常工作。

---

## 3. 安装

### 3.1 Windows 安装

**方法一：MSI 安装包（推荐）**

1. 访问 [GitHub Releases 页面](https://github.com/farion1231/cc-switch/releases/latest)
2. 下载 `CC-Switch-<版本号>-Windows.msi` 文件
3. 双击运行，按提示完成安装

**方法二：Portable 便携版**

- 下载 `CC-Switch-<版本号>-Windows-Portable.zip`
- 解压后直接运行 `cc-switch.exe`

安装完成后，在开始菜单中找到 **CC Switch** 启动即可。

### 3.2 macOS / Mac Mini 安装

使用 Homebrew 安装：

```bash
# 添加 tap 源
brew tap farion1231/ccswitch

# 安装
brew install --cask cc-switch

# 更新（如有新版本）
brew upgrade --cask cc-switch
```

安装后在 `应用程序` 中找到 CC Switch 启动。

---

## 4. 配置提供商

### 4.1 准备工作：获取 API Key

在开始配置前，你需要先准备好以下 API Key：

| 提供商 | 获取地址 | 说明 |
|--------|---------|------|
| 阿里云百炼 | [百炼控制台](https://bailian.console.aliyun.com/) | 开通 Coding Plan 后获取 |
| MiniMax | [MiniMax 开放平台](https://platform.minimaxi.com/) | 注册后创建 API Key |
| DeepSeek | [DeepSeek 平台](https://platform.deepseek.com/) | 注册后创建 API Key，需充值 |

### 4.2 清理冲突的环境变量

**重要：** 在配置 CC Switch 之前，需要检查并清理系统中可能冲突的环境变量。Claude Code 会读取以下环境变量：

```
ANTHROPIC_API_KEY
ANTHROPIC_AUTH_TOKEN
ANTHROPIC_BASE_URL
```

如果这些变量存在，会覆盖 CC Switch 的设置。检查方法：

**Windows（PowerShell）：**
```powershell
# 检查用户环境变量
[Environment]::GetEnvironmentVariables("User") | Where-Object { $_.Name -match "ANTHROPIC" }

# 删除冲突变量
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", $null, "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", $null, "User")

# 注册表也清理一下
Remove-ItemProperty -Path "HKCU:\Environment" -Name "ANTHROPIC_API_KEY" -ErrorAction SilentlyContinue
Remove-ItemProperty -Path "HKCU:\Environment" -Name "ANTHROPIC_AUTH_TOKEN" -ErrorAction SilentlyContinue
Remove-ItemProperty -Path "HKCU:\Environment" -Name "ANTHROPIC_BASE_URL" -ErrorAction SilentlyContinue
```

**macOS / Linux：**
```bash
# 检查 ~/.bashrc / ~/.zshrc 中是否有相关变量
grep -n "ANTHROPIC" ~/.zshrc ~/.bashrc 2>/dev/null

# 如果存在，用编辑器删除对应行，或者执行：
unset ANTHROPIC_API_KEY
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_BASE_URL
```

> **注意：** 如果这些变量写在 shell 配置文件（如 `~/.bashrc`、`~/.zshrc`）中，需要同时删除对应行，否则新开终端会重新注入。

### 4.3 在 CC Switch 中添加提供商

启动 CC Switch 后：

1. **添加百炼（默认配置）：**
   - 通常 CC Switch 会自动检测到已有的 Anthropic 配置并导入
   - 如果没有，手动点击右上角 `+`，填写：
     - Name: `百炼`（或任意名称）
     - App Type: `Claude Code`
     - API Key: 你的百炼 API Key
     - Base URL: `https://coding.dashscope.aliyuncs.com/apps/anthropic`
     - Model: `qwen3.5-plus`（或你需要的模型名）

2. **添加 MiniMax：**
   - 点击右上角 `+`，选择预设的 `MiniMax` 供应商
   - 填写从 MiniMax 开放平台获取的 API Key
   - 确认 Base URL 为 `https://api.minimaxi.com/anthropic`
   - 模型名填写：`MiniMax-M2.7`
   - 添加额外环境变量：
     - `ANTHROPIC_MODEL` = `MiniMax-M2.7`
     - `ANTHROPIC_DEFAULT_SONNET_MODEL` = `MiniMax-M2.7`
     - `ANTHROPIC_DEFAULT_OPUS_MODEL` = `MiniMax-M2.7`
     - `ANTHROPIC_DEFAULT_HAIKU_MODEL` = `MiniMax-M2.7`

3. **添加 DeepSeek：**
   - 点击右上角 `+`，选自定义配置
   - Name: `DeepSeek`
   - API Key: 你的 DeepSeek API Key
   - Base URL: `https://api.deepseek.com/anthropic`
   - Model: `deepseek-v4-flash`（价格极低，日常使用首选）

### 4.4 验证配置

配置完成后，在 CC Switch 首页点击目标 provider 的 **「启用」** 按钮。

然后在终端中启动 Claude Code 验证：

```bash
claude
```

启动后输入 `/status` 查看当前配置：

- `ANTHROPIC_BASE_URL` 应指向你所选的提供商地址
- Model 名称应与配置一致

再输入 `/model` 确认可以正常列出和切换模型。

---

## 5. 使用方式

### 5.1 切换模型

在 CC Switch 主界面，点击你想使用的 provider 的「启用」按钮即可切换。

**注意：** 切换 provider 后，需要 **关闭所有 Claude Code 窗口，重新打开一个新终端**，环境变量才会刷新。

### 5.2 常用命令

在 Claude Code 中：

| 命令 | 用途 |
|------|------|
| `/model` | 查看和切换当前可用的模型 |
| `/status` | 查看当前连接状态和环境变量 |
| `/exit` | 退出 Claude Code |

### 5.3 日常使用建议

- **频繁切换时：** 在 CC Switch 中点一下切换，然后关掉 Claude Code 重开即可
- **长期使用一个模型：** 设置好就不需要动了
- **余额管理：** DeepSeek 等按量计费的模型，注意在对应平台控制台关注余额
- **DeepSeek 模型选择：** 日常使用推荐 **deepseek-v4-flash**（价格极低，输入 ¥1/百万、输出 ¥2/百万），v4-pro 按 token 计费且会因 thinking 模式产生大量额外消耗（详见常见问题 7）

---

## 6. 常见问题

### 问题 1：安装后提示「环境变量冲突」

**现象：** 打开 CC Switch 时提示检测到 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_BASE_URL` 等环境变量冲突。

**原因：** 系统中存在已设置的环境变量，会覆盖 CC Switch 的配置。

**解决：** 参照本文 [4.2 清理冲突的环境变量](#42-清理冲突的环境变量) 删除冲突变量，然后重启 CC Switch。

### 问题 2：切换 provider 后 Claude Code 仍用旧模型

**现象：** 在 CC Switch 切换了 provider，但 Claude Code 启动后还是之前的模型。

**原因：** 环境变量在终端启动时加载，切换后需要新开终端。

**解决：** 关闭所有 Claude Code 窗口，打开全新的终端窗口再运行 `claude`。

### 问题 3：Claude Code 报错 `claude.exe` 找不到

**现象：**
```
无法将 "claude.exe" 项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

**原因：** CC Switch 在更新 Claude Code 时，可能重命名了旧版的 `claude.exe`，但新版未成功下载。

**解决：** 在 npm 目录中找到备份文件并恢复：

```powershell
# Windows
Copy-Item "$env:APPDATA\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe.old.*" "$env:APPDATA\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
```

### 问题 4：切换后 API 报错

**现象：** 切换到某个 provider 后，Claude Code 报 `API Error`。

**常见情况：**

| 错误 | 原因 | 解决 |
|------|------|------|
| `401 Unauthorized` | API Key 错误或未填写 | 检查 API Key 是否正确 |
| `402 Insufficient Balance` | 账户余额不足 | 到对应平台充值 |
| `404 Not Found` | Endpoint 地址错误 | 检查 Endpoint 是否正确（注意是 `/anthropic` 结尾不是 `/v1`） |
| 连接超时 | 网络问题 | 检查网络代理设置 |

### 问题 5：GitHub Releases 下载慢或无法下载

**现象：** 用 `curl` 下载 MSI 时报错 `Empty reply from server`。

**原因：** 国内网络访问 GitHub 不稳定。

**解决：** 直接在浏览器中打开 GitHub Releases 链接下载，浏览器通常有更好的网络兼容性。

### 问题 6：Mac 上 brew install 失败

**原因：** 可能需要先安装 Homebrew。

**解决：**
```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 添加 tap
brew tap farion1231/ccswitch

# 安装
brew install --cask cc-switch
```

### 问题 7：DeepSeek V4 Pro 调用费用过高

**现象：** 在 Claude Code 中使用 DeepSeek V4 Pro 时，短短几次对话就产生大量 token 消耗，费用较高（实测 4 次对话消耗 38 万 tokens，花费 ¥1.03）。

**原因：** Claude Code 底层使用 Anthropic SDK，默认开启 `thinking` 模式（`thinking: enabled`, `effort: max`）。DeepSeek 的 Anthropic 兼容 API 支持 thinking 参数，模型会在输出最终回答前先生成大量 `reasoning_content`（思维链内容），加上 Claude Code agent loop 中频繁的 tool calls，每次工具调用轮次的 thinking 内容都必须回传给 API 参与后续上下文，导致 **token 消耗成倍增长**。

具体来说，DeepSeek Anthropic 兼容 API 的思考模式有如下行为：
- 普通请求默认 `effort: high`，Agent 类请求（Claude Code、OpenCode）自动设为 `effort: max`
- 工具调用轮次必须完整回传 `reasoning_content`，后续所有请求都携带这些 thinking 内容
- 这就导致大量 token 被浪费在思维链上，而不是实际的代码输出

**解决方案：切换到 DeepSeek V4 Flash（推荐）**

deepseek-v4-flash 价格极低（输入 ¥1/百万 tokens，输出 ¥2/百万），日常编程辅助的成本几乎可以忽略不计，无需担心费用问题。在 CC Switch 中修改：

1. 停止 CC Switch，找到数据库文件：
   - Windows: `C:\Users\<用户名>\.cc-switch\cc-switch.db`
   - macOS/Linux: `~/.cc-switch/cc-switch.db`

2. 用 sqlite3 工具更新 provider 配置：

   ```bash
   sqlite3 "~/.cc-switch/cc-switch.db" "UPDATE providers SET settings_config='{\"env\":{\"ANTHROPIC_AUTH_TOKEN\":\"<你的DeepSeek API Key>\",\"ANTHROPIC_BASE_URL\":\"https://api.deepseek.com/anthropic\",\"ANTHROPIC_MODEL\":\"deepseek-v4-flash\"}}' WHERE id='deepseek' AND app_type='claude';"
   ```

3. 同时在 `common_config_claude` 中更新 custom model：

   ```bash
   sqlite3 "~/.cc-switch/cc-switch.db" "UPDATE settings SET value='...自定义 JSON，将 name 改为 deepseek-v4-flash...' WHERE key='common_config_claude';"
   ```

4. 重启 CC Switch

**DeepSeek 模型对比：**

| | v4-pro | v4-flash |
|---|---|---|
| 价格 | 按 token 计费（缓存未命中输入 ¥3/百万，输出 ¥6/百万） | 极低（缓存未命中输入 ¥1/百万，输出 ¥2/百万） |
| thinking 模式 | 支持 | 支持 |
| tool calls | 支持 | 支持 |
| 上下文长度 | 1M tokens | 1M tokens |
| 适用场景 | 复杂推理、深度分析 | **日常编码、日常问答** |

> **建议：** 如果你有百炼 Coding Plan 包月套餐，日常编码主力应该用百炼（已付费，无额外消耗）。DeepSeek V4 Flash 作为低成本备用方案即可。

---

## 7. Mac Mini 配置指南

要在 Mac Mini 上完成同样的配置，按以下步骤操作：

### 步骤 1：安装 CC Switch

```bash
brew tap farion1231/ccswitch
brew install --cask cc-switch
```

### 步骤 2：清理冲突的环境变量

```bash
# 检查是否有冲突变量
echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
echo "ANTHROPIC_AUTH_TOKEN=$ANTHROPIC_AUTH_TOKEN"
echo "ANTHROPIC_BASE_URL=$ANTHROPIC_BASE_URL"

# 从 shell 配置中删除
sed -i '' '/ANTHROPIC_API_KEY/d' ~/.zshrc
sed -i '' '/ANTHROPIC_AUTH_TOKEN/d' ~/.zshrc
sed -i '' '/ANTHROPIC_BASE_URL/d' ~/.zshrc

# 立即生效
source ~/.zshrc
```

### 步骤 3：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 步骤 4：启动 CC Switch 并添加提供商

启动 CC Switch（在 `应用程序` 中找到），参照本文 [第 4 节](#4-配置提供商) 添加三个提供商。

### 步骤 5：验证

```bash
claude
```

输入 `/status` 确认配置正确，再输入 `/model` 确认模型可切换。

---

## 附录：配置文件存储位置

CC Switch 的数据存储在以下位置：

| 平台 | 路径 |
|------|------|
| Windows | `C:\Users\<用户名>\.cc-switch\` |
| macOS | `~/.cc-switch/` |
| Linux | `~/.cc-switch/` |

核心文件：
- `cc-switch.db` — SQLite 数据库，存储所有 provider 配置
- `settings.json` — 应用设置（开机启动、窗口行为等）
- `logs/` — 日志目录

---

> **提示：** 如果遇到本文未覆盖的问题，可以在 [CC Switch GitHub Issues](https://github.com/farion1231/cc-switch/issues) 中搜索或提交问题。
