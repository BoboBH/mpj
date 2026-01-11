# Git MCP 服务器配置指南

## 安装状态

✅ Git MCP 服务器已成功安装!

## 安装详情

- **包名**: `@cyanheads/git-mcp-server`
- **版本**: 2.6.5
- **安装位置**: 全局安装 (npm global)
- **可执行命令**: `git-mcp-server`

## 可用的 Git 工具 (27个)

该 MCP 服务器提供了以下 Git 操作工具:

1. `git_add` - 添加文件到暂存区
2. `git_blame` - 查看文件的每一行是谁修改的
3. `git_branch` - 分支管理
4. `git_checkout` - 切换分支或恢复文件
5. `git_cherry_pick` - 挑选提交
6. `git_clean` - 清理未跟踪的文件
7. `git_clear_working_dir` - 清空工作目录
8. `git_clone` - 克隆仓库
9. `git_commit` - 创建提交
10. `git_diff` - 查看差异
11. `git_fetch` - 获取远程更新
12. `git_init` - 初始化仓库
13. `git_log` - 查看提交历史
14. `git_merge` - 合并分支
15. `git_pull` - 拉取远程更新
16. `git_push` - 推送到远程
17. `git_rebase` - 变基操作
18. `git_reflog` - 查看引用日志
19. `git_remote` - 远程仓库管理
20. `git_reset` - 重置操作
21. `git_set_working_dir` - 设置工作目录
22. `git_show` - 显示提交详情
23. `git_stash` - 暂存操作
24. `git_status` - 查看仓库状态
25. `git_tag` - 标签管理
26. `git_worktree` - 工作树管理
27. `git_wrapup_instructions` - Git 操作指导

## 配置 Claude Desktop

### Windows 配置文件位置

配置文件路径: `C:\Users\bobo\AppData\Roaming\Claude\claude_desktop_config.json`

### 配置内容

创建或编辑 `claude_desktop_config.json` 文件,添加以下内容:

```json
{
  "mcpServers": {
    "git": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\temp\\mpj"
      }
    }
  }
}
```

### 配置说明

- `command`: Git MCP 服务器的可执行命令
- `args`: 命令行参数 (通常为空数组)
- `env`: 环境变量
  - `GIT_WORKING_DIR`: Git 仓库的工作目录路径 (可以设置为你的项目路径)

### 多项目配置 (可选)

如果你有多个项目,可以这样配置:

```json
{
  "mcpServers": {
    "git-mpj": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\temp\\mpj"
      }
    },
    "git-other": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\other\\project"
      }
    }
  }
}
```

## 使用步骤

1. **重启 Claude Desktop**
   - 配置完成后,需要完全关闭并重新启动 Claude Desktop 应用

2. **验证连接**
   - 在 Claude Desktop 中,你应该能看到 Git 相关的工具提示
   - 可以询问 Claude: "请查看当前 Git 仓库的状态"

3. **开始使用**
   - 现在你可以在对话中让 Claude 执行 Git 操作
   - 例如:
     - "请帮我创建一个新的分支 feature/login"
     - "显示最近的提交历史"
     - "提交当前的更改"

## 实用示例

### 查看仓库状态
```
请使用 git_status 查看当前仓库的状态
```

### 创建新分支
```
请创建并切换到新分支 feature-new-ui
```

### 提交更改
```
请将所有更改添加到暂存区并提交,消息为"添加用户认证功能"
```

### 查看提交历史
```
请显示最近 10 条提交记录
```

### 克隆远程仓库
```
请克隆仓库 https://github.com/user/repo.git 到当前目录
```

## 故障排除

### 如果 Claude Desktop 无法连接 Git MCP

1. **检查配置文件路径**
   - Windows: `C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json`
   - 确保文件存在且格式正确 (可以使用 JSON 验证工具)

2. **验证安装**
   ```bash
   where git-mcp-server
   ```
   - 应该显示 Git MCP 服务器的安装路径

3. **检查日志**
   - Claude Desktop 的日志通常在:
   - `C:\Users\<username>\AppData\Roaming\Claude\logs\`

4. **手动测试**
   ```bash
   git-mcp-server
   ```
   - 如果成功启动,会显示日志信息

## 相关资源

- [MCP 官方文档](https://modelcontextprotocol.info/)
- [Git MCP 服务器 (@cyanheads/git-mcp-server)](https://glama.ai/mcp/servers/@cyanheads/git-mcp-server)
- [Awesome MCP ZH - 中文资源](https://github.com/yzfly/Awesome-MCP-ZH)
- [GitHub MCP 注册指南](https://github.blog/ai-and-ml/generative-ai/how-to-find-install-and-manage-mcp-servers-with-the-github-mcp-registry/)

## GitHub Token 配置

### 为什么需要 GitHub Token?

如果你需要:
- 访问私有仓库
- 推送代码到 GitHub
- 创建 Pull Request 或 Issue
- 其他需要认证的操作

### 创建 GitHub Personal Access Token

1. **登录 GitHub**
   - 访问 https://github.com/settings/tokens

2. **生成新 Token**
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 设置 Token 描述 (如: "Git MCP Server")
   - 选择过期时间 (建议: 90 days 或 No expiration)
   - **勾选必要的权限** (Scopes):
     - ✅ `repo` - 完整的仓库访问权限 (私有仓库读写)
     - ✅ `workflow` - GitHub Actions 工作流权限 (如果需要)
     - ✅ `admin:org` - 组织管理权限 (如果需要)
     - ✅ `delete_repo` - 删除仓库权限 (谨慎使用)

3. **生成并保存 Token**
   - 点击 "Generate token"
   - ⚠️ **重要**: 立即复制 token,它只会显示一次!
   - 建议保存到安全的位置

### 配置 Git 使用 Token

#### 方法 1: 使用 Git Credential Helper (推荐)

在命令行中运行:

```bash
git config --global credential.helper store
git config --global credential.helper manager-core
```

然后首次访问 GitHub 时输入用户名和 token。

#### 方法 2: 在 URL 中包含 Token

```bash
git clone https://<TOKEN>@github.com/username/repo.git
```

#### 方法 3: 在 MCP 配置中设置环境变量

在 `claude_desktop_config.json` 中配置:

```json
{
  "mcpServers": {
    "git": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\temp\\mpj",
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

⚠️ **安全警告**: 将 token 直接写在配置文件中存在安全风险,建议只在个人开发环境中使用。

### 配置 SSH 密钥 (更安全的方式)

#### 1. 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### 2. 添加 SSH 密钥到 GitHub

- 复制公钥: `cat ~/.ssh/id_ed25519.pub`
- 访问: https://github.com/settings/keys
- 点击 "New SSH key",粘贴公钥内容

#### 3. 测试 SSH 连接

```bash
ssh -T git@github.com
```

#### 4. 在 MCP 配置中使用 SSH

```json
{
  "mcpServers": {
    "git": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\temp\\mpj",
        "GIT_SSH_COMMAND": "C:\\Windows\\System32\\OpenSSH\\ssh.exe"
      }
    }
  }
}
```

## 高级配置

### 自定义 Git 可执行文件路径

如果 Git 不在系统 PATH 中,可以指定完整路径:

```json
{
  "mcpServers": {
    "git": {
      "command": "git-mcp-server",
      "args": [],
      "env": {
        "GIT_WORKING_DIR": "d:\\temp\\mpj",
        "GIT_EXEC_PATH": "D:\\Program Files\\Git\\cmd\\git.exe"
      }
    }
  }
}
```

### 环境变量说明

| 环境变量 | 说明 | 必需 |
|---------|------|------|
| `GIT_WORKING_DIR` | Git 仓库的工作目录 | ✅ 是 |
| `GITHUB_TOKEN` | GitHub Personal Access Token | 条件必需 |
| `GIT_EXEC_PATH` | Git 可执行文件路径 | 否 |
| `GIT_SSH_COMMAND` | SSH 可执行文件路径 | 否 |
| `GIT_CONFIG_GLOBAL` | 全局 Git 配置文件路径 | 否 |
| `GIT_AUTHOR_NAME` | 默认提交者名称 | 否 |
| `GIT_AUTHOR_EMAIL` | 默认提交者邮箱 | 否 |

## 总结

Git MCP 服务器已成功安装!现在你可以在 Claude Desktop 中通过自然语言与 Git 仓库进行交互,让 AI 帮助你完成版本控制操作。

记得配置 `claude_desktop_config.json` 文件并重启 Claude Desktop 以启用 MCP 集成。
