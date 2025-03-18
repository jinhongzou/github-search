import streamlit as st
import pandas as pd
import json
import os

from utilities.githubsearch import GitHubSearch
from utilities.keyword4llm import KeyWord4Llm  # 假设这是一个生成关键字的函数
# 假设 parsed_results 是通过某种方式（如API调用）获得的数据

gh_search = GitHubSearch()  # 如果需要认证，请提供您的个人访问令牌
keyword4llm = KeyWord4Llm(api_key=os.getenv('MODEL_API_KEY'),
                              base_url=os.getenv('MODEL_BASE_URL'),
                              model=os.getenv('MODEL_NAME')
                              )

def main():
    
    # 侧边栏配置
    st.title("GitHub项目搜索工具 🔍")

    with st.sidebar:

        st.header("搜索设置")
        st.subheader("输入关键字")

        # 初始化 session state 变量
        if 'input_keyword' not in st.session_state:
            st.session_state.input_keyword = "ai"
        if 'optimized_keyword' not in st.session_state:
            st.session_state.optimized_keyword = None

        # 输入框用于接收用户的关键字
        input_keyword = st.text_input(
            "用户输入关键字",
            value="ai",
            key="input_q"
        )

        # 当用户输入发生变化时，更新 session state 并清除优化后的关键字
        if st.session_state.input_keyword != input_keyword:
            st.session_state.input_keyword = input_keyword
            st.session_state.optimized_keyword = None

        # 按钮用于触发 AI 优化
        if st.button("AI优化关键字"):
            # 调用优化函数并更新 session state
            st.session_state.optimized_keyword = keyword4llm.get_keyword(query=st.session_state.input_keyword)

        # 显示最终关键字
        final_input_q = st.text_input(
            "最终关键字",
            value=st.session_state.optimized_keyword if st.session_state.optimized_keyword else st.session_state.input_keyword,
            disabled=True  # 禁止用户直接编辑最终关键字
        )

        # 提示用户如何操作
        if not st.session_state.optimized_keyword:
            st.info("点击 'AI优化关键字' 按钮以优化您的关键字。")
        else:
            st.success("关键字已优化！您可以使用此优化后的关键字进行搜索。")
        language = st.selectbox("编程语言",["","Python","JavaScript","Java","Go"])
        min_stars = st.number_input("最小星数", min_value=0, value=10)
        page_num = st.number_input("项目数量", min_value=0, value=10)
        sort_by = st.selectbox("排序方式", ["stars", "forks", "updated"])
        sort_order = st.radio("排序顺序", ["Desc", "Asc"])
        search_button = st.button("开始搜索")

    st.write("点击 “开始搜索” 开始查询")

    if search_button:

        parsed_results = gh_search.search_repositories(
                    query=final_input_q,
                    language=language.lower(),
                    min_stars=min_stars,
                    sort=sort_by,
                    order=sort_order,
                    per_page=page_num
            )

        if parsed_results['total_count'] != 0:
            # 将 parsed_results 转换为 DataFrame
            df = pd.DataFrame(parsed_results)

            # 解析 JSON 字符串
            expanded_df = pd.json_normalize(df['items'])

            # 使用Streamlit的dataframe组件展示数据
            st.session_state.search_results = expanded_df
        else:
            if 'search_results' in st.session_state:
                del st.session_state['search_results']


    if 'search_results' in st.session_state:
        st.dataframe(st.session_state.search_results)
    else:
        st.warning("未找到相关项目")

if __name__ == "__main__":
    main()
