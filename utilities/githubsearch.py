import requests
import base64

class GitHubSearch:
    def __init__(self, token=None):
        #self.headers = {'Accept': 'application/vnd.github.v3+json'}
        #if token:
        #    self.headers['Authorization'] = f'token {token}'
        self.base_url = 'https://api.github.com/search/repositories'

    def get_readme_content(self, full_name):
        """
        获取指定 GitHub 仓库的 README.md 文件内容。

        参数:
        - full_name (str): owner(用户名或组织名)/repo(仓库名称)

        返回:
        - str: README.md 文件的内容，如果是二进制文件则返回解码后的字符串。
        """
        url = f"https://api.github.com/repos/{full_name}/readme"
        response = requests.get(url)
        try:
            if response.status_code != 200:
                raise Exception(f"Error fetching data: {response.status_code}, {response.text}")

            content_info = response.json()
            # README 的内容是以 base64 编码的
            encoded_content = content_info['content']
            # 解码得到原始的文本内容
            decoded_content = base64.b64decode(encoded_content).decode('utf-8')

            return decoded_content
        except Exception as e:
            # 这里可以记录错误信息，或者采取其他措施
            print(f"An error occurred: {e}")
            return None
    # 如果 html_url 需要作为可点击的链接展示，我们可以先将其转换为 HTML 格式
    def make_clickable(self, val):
        return f'<a href="{val}" target="_blank">{val}</a>'

    def search_repositories(self, query, language=None, min_stars=0, sort='best_match', order='desc', created=None, pushed=None, per_page=10):
        """
        使用 GitHub Search API 搜索仓库。

        参数:
        - query (str): 搜索关键词。
        - language (str, optional): 仓库编程语言。
        - sort (str, optional): 排序方式（'stars', 'forks', 'updated'）。
        - order (str, optional): 排序顺序（'asc', 'desc'）。
        - created (str, optional): 创建时间范围（例如 '>=2024-01-01'）。
        - pushed (str, optional): 最近更新时间范围（例如 '>=2024-01-01'）。
        - per_page (int, optional): 每页显示的结果数量。

        返回:
        - dict: 解析后的搜索结果。
        """
        # 构建搜索 URL
        url = self.base_url
        params = {'q': query}

        if language:
            params['q'] += f'+language:{language}'

        if min_stars > 0:
            query += f"+stars:>={min_stars}"

        if sort != 'best_match':
            params['sort'] = sort

        if order:
            params['order'] = order

        if created:
            params['q'] += f'+created:{created}'

        #if pushed:
        #    params['q'] += f'+pushed:{pushed}'

        if per_page:
            params['per_page'] = per_page

        # 发送请求
        print(f"url: {url}, params:{params}")

        response = requests.get(url, params=params)
        #print(f"response: {response}")
        # 检查响应状态码
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}")

        # 解析 JSON 响应
        results = response.json()
        #print(f"results: {results}")

        # 解析并返回结果
        parsed_results = {
            'total_count': results['total_count'],
            'items': [
                {
                    '⭐': item['stargazers_count'],
                    '名称': item['name'],
                    '语言': item['language'],
                    #'full_name': item['full_name'],
                    #'html_url': self.make_clickable(item['html_url']),
                    '链接': item['html_url'],
                    '描述': item['description'],
                    #'open_issues_count': item['open_issues_count'],
                    '更新时间🕒': item['created_at'],
                    'Fork数': item['forks_count'],
                    #'updated_at': item['updated_at'],
                    'ReadMe': self.get_readme_content(item['full_name']),
                }
                for item in results['items']
            ]
        }


        return parsed_results



# 示例调用
if __name__ == '__main__':
    gh_search = GitHubSearch()  # 如果需要认证，请提供您的个人访问令牌
    try:

        #repos = gh_search.search_repositories(query="agentless", sort="stars", order="desc")
        #print(repos)
        repos = gh_search.search_repositories(
            query='Agentless',
            #language='Python',
            #sort='updated',
            order='desc',
            #per_page=100
        )

        for repo in repos['items']:
            print(f"Repo Name: {repo['name']}, Stars: {repo['stargazers_count']}, Language: {repo['language']} ...")
            #print(f"""readme: {get_readme_content(repo['full_name'])}""")
            #readme_content = gh_search.get_readme_content(full_name="OpenAutoCoder/Agentless")
            #print(readme_content)


    except Exception as e:
        print(e)