# flbook.com.cn PDF 下载工具

## 📖 项目简介

这是一个用于从 flbook.com.cn 网站下载 PDF 文件的自动化工具。脚本能够自动解析页面数据、提取加密密码，并下载解密后的 PDF 文件。

## ✨ 功能特性

- 🔍 **自动解析**
- 🔑 **密码提取**
- 📥 **文件下载**
- 🔐 **PDF 解密**
- 📝 **信息记录**
- 🔄 **交互模式**

## 📋 系统要求

- Python 3.7+

## 🔧 依赖安装

```bash
pip install requests PyPDF2
```
或
```bash
pip install -r ./requirements.txt
```

## 🚀 使用方法

### 1. 运行脚本

```bash
python flbook_downloader.py
```

### 2. 输入格式

程序启动后，支持以下输入格式：

- **编码**: `code`
- **完整URL**: `https://flbook.com.cn/c/code`
- **退出**: 输入 `q`

### 3. 输出文件

下载的文件保存在 `.\flbook_downloads\` 目录下：

```
flbook_downloads/
├── 文件名.pdf              # 原始下载文件（可能加密）
├── 文件名_解密版.pdf        # 解密后的文件（如果成功）
└── 文件名_密码.txt         # 密码信息文件
```

---

**免责声明**: 脚本仅供学习使用，请确保您有权访问和下载相关内容，并遵守网站的使用条款。