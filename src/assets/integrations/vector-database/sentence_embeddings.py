import sys

from pgvector.psycopg import register_vector
import psycopg
from sentence_transformers import SentenceTransformer

# 创建数据库连接，并设置自动提交
conn = psycopg.connect(sys.argv[1], autocommit=True)

# 启用 pgvector 扩展，注册向量数据类型
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

# 重新创建表 documents
conn.execute('DROP TABLE IF EXISTS documents')
conn.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))')

# 嵌入输入文本
input = [
    'The dog is barking',
    'The cat is purring',
    'The bear is growling'
]
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(input)

# 将输入文本和相应的嵌入向量插入到数据库中
for content, embedding in zip(input, embeddings):
    conn.execute('INSERT INTO documents (content, embedding) VALUES (%s, %s)', (content, embedding))

# 查询与指定文档最相近的其他文档的文本内容
document_id = 1
neighbors = conn.execute('SELECT content FROM documents WHERE id != %(id)s ORDER BY embedding <=> (SELECT embedding FROM documents WHERE id = %(id)s) LIMIT 5', {'id': document_id}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])
