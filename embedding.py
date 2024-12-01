# 导入必要的库
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import numpy as np
from pinecone import Pinecone, ServerlessSpec

# 初始化Pinecone
pc = Pinecone(api_key="pcsk_4FZe81_JGbD2TPTehuekuXeRAtWMhB5eifgiY55y3itjq5cHTf38XE8ShvrMHByYNCrMG5")

# 创建索引
index_name = "rag"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1024,  # GTE-large的embedding维度应该是1024
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# 定义平均池化函数
def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

# 文档列表
input_texts = [
    "what is the capital of China?",
    "how to implement quick sort in python?",
    "Beijing",
    "sorting algorithms"
]

# 初始化Tokenizer和Model
tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
model = AutoModel.from_pretrained("thenlper/gte-large")

# 对输入文本进行编码
batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

# 生成embedding
with torch.no_grad():
    outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

# (可选) 归一化embedding
embeddings = F.normalize(embeddings, p=2, dim=1)

# **步骤1：将embedding存储到Pinecone中**

# 将embedding转换为numpy数组
embeddings_np = embeddings.cpu().numpy()

# 为每个文本生成唯一的id
ids = [f'id_{i}' for i in range(len(input_texts))]

# 准备要上传到Pinecone的向量数据，包括id、向量和元数据（原始文本）
vectors = list(zip(ids, embeddings_np.tolist(), [{'text': text} for text in input_texts]))

# 将向量上传到Pinecone索引
index.upsert(vectors)

# **步骤2：针对查询文本生成embedding并检索相关文档**

# 定义查询文本
query_text = "How can I sort a list in Python?"

# 对查询文本进行编码
query_dict = tokenizer(query_text, max_length=512, padding=True, truncation=True, return_tensors='pt')

# 生成查询文本的embedding
with torch.no_grad():
    query_output = model(**query_dict)
    query_embedding = average_pool(query_output.last_hidden_state, query_dict['attention_mask'])
    # 归一化
    query_embedding = F.normalize(query_embedding, p=2, dim=1)
    query_embedding_np = query_embedding.cpu().numpy()

# 在Pinecone中查询相似的文档
query_response = index.query(
    vector=query_embedding_np.tolist()[0],
    top_k=3,  # 返回最相似的3个文档
    include_values=False,
    include_metadata=True
)
print(query_response)

# 打印检索结果
print("检索到的文档：")
for match in query_response['matches']:
    print(f"得分: {match['score']}\tID: {match['id']}\t文本: {match['metadata']['text']}")

# **步骤3：在RAG中使用检索到的文档**

# 假设我们使用生成式模型来回答问题，可以将检索到的文档作为上下文

# 示例：将检索到的文本合并，作为上下文传递给生成式模型
retrieved_texts = [match['metadata']['text'] for match in query_response['matches']]
context = "\n".join(retrieved_texts)

# 构建新的输入，包含上下文和问题
final_input = f"Context:\n{context}\n\nQuestion: {query_text}\nAnswer:"

# 这一步您可以根据您的生成模型或Pipeline来完成，这里不具体展开
