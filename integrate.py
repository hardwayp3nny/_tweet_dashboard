from flask import Flask, send_from_directory, jsonify, render_template, request
import os
import pandas as pd
import pyodbc
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import re
app = Flask(__name__)

DATA_DIR = r'F:\py demos\coindata\historical_data'

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=twitter;UID=1;PWD=1')
    return conn

@app.route('/')
def index():
    return render_template('integrated_index.html')

@app.route('/tokens')
def get_tokens():
    tokens = [f.replace('_historical_data.csv', '') for f in os.listdir(DATA_DIR) if f.endswith('_historical_data.csv')]
    return jsonify(tokens)

@app.route('/data/<token>')
def get_data(token):
    file_path = os.path.join(DATA_DIR, f'{token}_historical_data.csv')
    if not os.path.exists(file_path):
        return "File not found", 404

    df = pd.read_csv(file_path)
    return df.to_json(orient='records')

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    token = request.form['token']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'Twitter_%'")
    tables = cursor.fetchall()

    G = nx.Graph()

    for table in tables:
        table_name = table[0]
        query = f"""
        SELECT TOP 100 tweet_content
        FROM {table_name}
        WHERE tweet_content LIKE ?
        """
        cursor.execute(query, ('%' + token + '%',))

        for row in cursor.fetchall():
            G.add_edge(table_name.replace('Twitter_', ''), token)

    conn.close()

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'graph_url': graph_url, 'node_positions': {node: [pos[node][0], pos[node][1]] for node in G.nodes()}})


@app.route('/search_token', methods=['POST'])
def search_token():
    token = request.form['token']
    author = request.form.get('author')

    conn = get_db_connection()
    cursor = conn.cursor()

    results = []

    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'Twitter_%'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        query = f"""
        SELECT TOP 1000 tweet_time, favorite_count, retweet_count, reply_count, tweet_content, '{table_name}' as author
        FROM {table_name}
        WHERE tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ? 
           OR tweet_content LIKE ?
           OR tweet_content LIKE ?
        """
        params = [
            f'% {token} %',  # 被空格包围
            f'% {token}.',  # 句子末尾
            f'% {token},',  # 后面跟逗号
            f'% {token}!',  # 后面跟感叹号
            f'% {token}?',  # 后面跟问号
            f'%${token}%',  # $符号开头（如 $eth）
            f'%#{token}%',  # #符号开头（如 #eth）
            f'%@{token}%',  # @符号开头（如 @eth）
            f'%({token})%'  # 被括号包围
        ]

        if author:
            query += f" AND '{table_name}' = ?"
            params.append('Twitter_' + author)

        cursor.execute(query, params)

        for row in cursor.fetchall():
            tweet_content = row[4]
            # 使用正则表达式进行更严格的匹配
            if re.search(r'\b' + re.escape(token) + r'\b|\$' + re.escape(token) + r'\b|#' + re.escape(
                    token) + r'\b|@' + re.escape(token) + r'\b|$' + re.escape(token) + r'$', tweet_content,
                         re.IGNORECASE):
                results.append({
                    'tweet_time': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                    'favorite_count': row[1],
                    'retweet_count': row[2],
                    'reply_count': row[3],
                    'tweet_content': tweet_content,
                    'author': row[5].replace('Twitter_', '')
                })

    conn.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
