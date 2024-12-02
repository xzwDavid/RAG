# 导入必要的库
import os
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import numpy as np
from pinecone import Pinecone, ServerlessSpec

# 初始化Pinecone
pc = Pinecone(api_key="")

# 创建索引
# index_name = "numpy"
index_name = "numpy/"

# if not pc.has_index(index_name):
#     pc.create_index(
#         name=index_name,
#         dimension=1024,  # GTE-large的embedding维度应该是1024
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )

index = pc.Index(index_name)

# 定义平均池化函数
def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def traverse_directory(directory):
    file_contents = []  # List to store contents of files
    file_names = []     # List to store file names
    
    # Walk through all the subdirectories and files
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            print("file",file_path)
            
            try:
                # Open the file and read its content
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    
                    # Append the content and the file name to the lists
                    file_contents.append(contents)
                    file_names.append(file_path)  # Store the full file path for easy identification
                
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    
    return file_names, file_contents

def remove_non_ascii(text):
    return ''.join([char for char in text if ord(char) < 128])

directory_path = 'doc/numpy_docs'  # Replace with your folder path
ids, input_texts = traverse_directory(directory_path)
# 文档列表
# input_texts = [
#     "what is the capital of China?",
#     "how to implement quick sort in python?",
#     "Beijing",
#     "sorting algorithms"
# ]


def get_embedding(input_texts ):
    # 初始化Tokenizer和Model
    tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
    model = AutoModel.from_pretrained("thenlper/gte-large")

    # 对输入文本进行编码
    batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

    print("finish tokenizer")
    # 生成embedding
    with torch.no_grad():
        outputs = model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

    print("normalize embeddings started")
    # (可选) 归一化embedding
    embeddings = F.normalize(embeddings, p=2, dim=1)
    print("normalize embeddings finished")

    # **步骤1：将embedding存储到Pinecone中**

    # 将embedding转换为numpy数组
    embeddings_np = embeddings.cpu().numpy()
    print("finish get embeddings")
    return embeddings_np


MAX_METADATA_SIZE = 40950  # Maximum allowed size in bytes

def truncate_text_to_limit(text, max_size=MAX_METADATA_SIZE):
    # Estimate the size of the text when encoded in UTF-8
    encoded_text = text.encode('utf-8')  # Encoding the text to get byte size
    if len(encoded_text) > max_size:
        # If the text exceeds the limit, truncate it
        print(f"Truncating text to {max_size} bytes")
        truncated_text = encoded_text[:max_size]
        return truncated_text.decode('utf-8', 'ignore')  # Decode back to string, ignoring invalid characters
    return text


# 4 chunk
embeddings_np = get_embedding(input_texts)
print(embeddings_np.shape)
#(4,1024)
# concat_text = ""
# # 1 chunk
# for text in input_texts:
#     concat_text = concat_text + text
# print(get_embedding(concat_text).shape)
#(1,1024)


# 为每个文本生成唯一的id
# ids = [f'id_{i}' for i in range(len(input_texts))]

# 准备要上传到Pinecone的向量数据，包括id、向量和元数据（原始文本）
print("prepare vectors")
for i in range(len(ids)):
    ids[i] = remove_non_ascii(ids[i])
vectors = list(zip(ids, embeddings_np.tolist(), [{'text': truncate_text_to_limit(text)} for text in input_texts]))

# 将向量上传到Pinecone索引
index.upsert(vectors)

