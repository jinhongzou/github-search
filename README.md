# GitHub项目搜索工具 🔍

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-%23FF4B4B)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

基于Streamlit构建的GitHub仓库智能搜索工具，支持多条件筛选和实时结果展示

## 功能特性

- 🎛️ 交互式搜索面板配置搜索参数
- 🔍 多维度过滤（编程语言、星标数量、排序方式）
- 📊 实时表格展示搜索结果
- ⚡ 基于GitHub REST API的快速查询
- 📱 响应式网页设计适配多端设备

## 安装指南

### 前置要求
- Python 3.8+
- GitHub个人访问令牌（可选，用于提高API限额）

### 安装步骤
```bash
git clone https://github.com/yourusername/github-search-tool.git
cd github-search-tool
pip install -r requirements.txt
```
## 使用说明
### 首次运行
```python
streamlit run app.py
```
### 界面功能说明
在侧边栏配置搜索参数：
-    关键字：项目名称/描述关键词
-    编程语言：过滤指定语言项目
-    最小星数：筛选优质项目
-    排序方式：按星标/分叉/更新时间排序
-    点击"开始搜索"按钮启动查询
结果将以交互表格形式展示在主页

### 高级配置
如需提高API调用限额，请按以下方式初始化GitHubSearch：

```python
gh_search = GitHubSearch(token="your_github_token")
```

### 项目结构

├── app.py                 # 主程序入口
├── requirements.txt       # 依赖库列表
└── utilities/
    └── githubsearch.py    # GitHub API封装模块
### 技术栈
Streamlit (Web框架)
Pandas (数据处理)
GitHub REST API v3

### 授权许可
MIT License



注意事项：
1. 请# GitHub项目搜索工具 🔍

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-%23FF4B4B)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

基于Streamlit构建的GitHub仓库智能搜索工具，支持多条件筛选和实时结果展示

## 功能特性

- 🎛️ 交互式搜索面板配置搜索参数
- 🔍 多维度过滤（编程语言、星标数量、排序方式）
- 📊 实时表格展示搜索结果
- ⚡ 基于GitHub REST API的快速查询
- 📱 响应式网页设计适配多端设备

## 安装指南

### 前置要求
- Python 3.8+
- GitHub个人访问令牌（可选，用于提高API限额）

### 安装步骤
```bash
git clone https://github.com/yourusername/github-search-tool.git
cd github-search-tool
pip install -r requirements.txt
```
## 使用说明
### 首次运行
```python
streamlit run app.py
```
### 界面功能说明
在侧边栏配置搜索参数：
-    关键字：项目名称/描述关键词
-    编程语言：过滤指定语言项目
-    最小星数：筛选优质项目
-    排序方式：按星标/分叉/更新时间排序
-    点击"开始搜索"按钮启动查询
结果将以交互表格形式展示在主页

### 高级配置
如需提高API调用限额，请按以下方式初始化GitHubSearch：

```python
gh_search = GitHubSearch(token="your_github_token")
```

### 项目结构

├── app.py                 # 主程序入口
├── requirements.txt       # 依赖库列表
└── utilities/
    └── githubsearch.py    # GitHub API封装模块
### 技术栈
Streamlit (Web框架)
Pandas (数据处理)
GitHub REST API v3

### 授权许可
MIT License



注意事项：
1. 请确保补充创建`requirements.txt`文件，内容应包含：
```text
streamlit>=1.29.0
pandas>=2.0.0
requests>=2.31.0
```
如需支持分页功能，建议在search_repositories方法中添加page参数处理

推荐添加结果导出功能（CSV/Excel），可扩展st.download_button组件

建议在.gitignore中添加secrets.toml避免密钥泄露确保补充创建`requirements.txt`文件，内容应包含：
```text
streamlit>=1.29.0
pandas>=2.0.0
requests>=2.31.0
```
如需支持分页功能，建议在search_repositories方法中添加page参数处理

推荐添加结果导出功能（CSV/Excel），可扩展st.download_button组件

建议在.gitignore中添加secrets.toml避免密钥泄露