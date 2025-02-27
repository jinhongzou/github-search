import streamlit as st
import pandas as pd
import json

from utilities.githubsearch import GitHubSearch
# 假设 parsed_results 是通过某种方式（如API调用）获得的数据


def main():

    gh_search = GitHubSearch()  # 如果需要认证，请提供您的个人访问令牌

    # 侧边栏配置
    st.title("GitHub项目搜索工具 🔍")
    with st.sidebar:
        st.header("搜索设置")
        input_q = st.text_input("关键字")
        language = st.selectbox("编程语言",["","Python","JavaScript","Java","Go"])
        min_stars = st.number_input("最小星数", min_value=0, value=10)
        page_num = st.number_input("项目数量", min_value=0, value=10)
        sort_by = st.selectbox("排序方式", ["stars", "forks", "updated"])
        sort_order = st.radio("排序顺序", ["Desc", "Asc"])
        search_button = st.button("开始搜索")

    st.write("点击 “开始搜索” 开始查询")

    if search_button:

        parsed_results = gh_search.search_repositories(
                    query=input_q,
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
