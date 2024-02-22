import sys

from qdrant_client import QdrantClient
from qdrant_client.http.models import (Distance, Filter, FieldCondition,
                                       MatchValue, PointStruct, VectorParams)

# 客户端在创建 collection 时存在 HTTP 超时问题，参考
# https://github.com/qdrant/qdrant-client/issues/394，采用 gRPC 作为临时解决方案
# client = QdrantClient(sys.argv[1])
client = QdrantClient(sys.argv[1], prefer_grpc=True)

# 创建一个 collection 以存储向量数据，设定向量维数为 4，使用点积度量距离
client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)

# 添加一些向量
client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1,
                    vector=[0.05, 0.61, 0.76, 0.74],
                    payload={"city": "Berlin"}),
        PointStruct(id=2,
                    vector=[0.19, 0.81, 0.75, 0.11],
                    payload={"city": "London"}),
        PointStruct(id=3,
                    vector=[0.36, 0.55, 0.47, 0.94],
                    payload={"city": "Moscow"}),
        PointStruct(id=4,
                    vector=[0.18, 0.01, 0.85, 0.80],
                    payload={"city": "New York"}),
        PointStruct(id=5,
                    vector=[0.24, 0.18, 0.22, 0.44],
                    payload={"city": "Beijing"}),
        PointStruct(id=6,
                    vector=[0.35, 0.08, 0.11, 0.44],
                    payload={"city": "Mumbai"}),
    ],
)

# 查询与向量 [0.2, 0.1, 0.9, 0.7] 最相似的 3 个向量
search_result = client.search(collection_name="test_collection",
                              query_vector=[0.2, 0.1, 0.9, 0.7],
                              limit=3)
print(search_result)

# 进一步过滤结果
search_result = client.search(
    collection_name="test_collection",
    query_vector=[0.2, 0.1, 0.9, 0.7],
    query_filter=Filter(
        must=[FieldCondition(key="city", match=MatchValue(value="London"))]),
    with_payload=True,
    limit=3,
)
print(search_result)
