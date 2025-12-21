# Claude Code 自动更新脚本

一个用于安装和更新 Claude Code 的 PowerShell 脚本。

## 功能特性

- 自动检测当前版本并更新到最新版本
- 支持指定安装目录
- 支持指定版本安装
- 自动备份现有版本
- SHA256 校验确保文件完整性
- 自动创建环境变量和符号链接
- 进程检测和安全终止

## 使用方法

### 基本用法

```powershell
# 检查更新并安装最新版本
.\update-cc.ps1

# 安装稳定版本
.\update-cc.ps1 stable

# 安装指定版本
.\update-cc.ps1 2.0.70
```

### 高级选项

```powershell
# 强制重新安装（即使已是最新版本）
.\update-cc.ps1 -Force

# 安装到指定目录
.\update-cc.ps1 -InstallDir "C:\Tools"

# 显示帮助信息
.\update-cc.ps1 -Help
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `Target` | 目标版本 (latest/stable/版本号) | `latest` |
| `-Force` | 强制更新，跳过确认 | 无 |
| `-Help` | 显示帮助信息 | 无 |
| `-InstallDir` | 指定安装目录 | `C:\Software\ClaudeCode` |

## 系统要求

- Windows 10/11 x64
- PowerShell 5.1 或更高版本
- 网络连接

## 安装位置

默认安装到：`C:\Software\ClaudeCode\claude.exe`

脚本会自动：
- 添加安装目录到用户 PATH 环境变量
- 创建必要的符号链接
- 创建版本备份文件

## 安全特性

- SHA256 校验和验证
- 自动备份现有版本
- 安全的进程终止
- 失败时自动回滚

## 示例

```powershell
# 典型的更新流程
PS C:\> .\update-cc.ps1
[2024-01-01 10:00:00] [INFO] 正在检查当前版本...
[2024-01-01 10:00:01] [INFO] 当前版本: 2.0.69
[2024-01-01 10:00:02] [INFO] 发现新版本: 2.0.70
是否继续下载并安装 Claude Code 2.0.70 ? (y/N) y
[2024-01-01 10:00:03] [SUCCESS] Claude Code 更新安装成功！版本: 2.0.70
```

## 故障排除

如果遇到问题，请检查：
1. 网络连接是否正常
2. 是否有足够的磁盘空间
3. PowerShell 执行策略设置
4. 防病毒软件是否阻止了文件操作
