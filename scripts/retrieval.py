import os
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import numpy as np
from pinecone import Pinecone, ServerlessSpec
import json
import itertools

# Load configuration
def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

CONFIG = load_config()

PINECONE_API_KEY = CONFIG["pinecone_api_key"]
QUESTIONS_INPUT = CONFIG["questions_input"]

def read_md_contents(names):
    big_string = ""
    for name in names:
        filename = f"{name}.md"
        filepath = os.path.join('.', filename)

        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
                big_string += file_content
        else:
            print(f"File {filename} does not exist, skipping.")
    return big_string

def get_json_question_and_groundtruth(path):
    questions = []
    groundtruth = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):  
            file_path = os.path.join(path, filename)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                questions.append(data['question'])
                if 'documents' in data:
                    groundtruth.append(data['documents'].split('\n')[1:-1])
    return questions, groundtruth

def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def calculate_precision_recall(vector_pred, vector_true):
    set_pred = set(vector_pred)
    set_true = set(vector_true)
    tp = len(set_pred & set_true)
    fp = len(set_pred - set_true)
    fn = len(set_true - set_pred)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1

def get_embedding(input_texts):
    tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
    model = AutoModel.from_pretrained("thenlper/gte-large")
    batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
    return F.normalize(embeddings, p=2, dim=1).cpu().numpy()

def build_parent_dict(node, parent=None, parent_dict=None):
    if parent_dict is None:
        parent_dict = {}
    parent_dict[node['name']] = parent['name'] if parent else None
    for child in node.get('children', []):
        build_parent_dict(child, node, parent_dict)
    return parent_dict

def tree_retrieval(parent_dict, originaltopK, limit=10):
    return [tree_context_retrieval_parent(parent_dict, i, limit) for i in originaltopK]

def tree_context_retrieval_parent(parent_dict, topK, limit=10):
    retrieved = set()
    queue = list(topK)
    while len(queue) > 0 and len(retrieved) <= limit:
        retrieved.add(queue[0])
        if parent_dict[queue[0]]:
            queue.append(parent_dict[queue[0]])
        queue.pop(0)
    return list(retrieved)

def topK_retrieval(index, embedded_queries, K):
    retrieved = []
    for query in embedded_queries:
        response = index.query(vector=query.tolist(), top_k=K, include_metadata=True)
        retrieved.append([match['id'] for match in response["matches"]])
    return retrieved

def evaluate_precision_recall(to_eval, groundtruth):  
    assert len(groundtruth) == len(to_eval)
    sum_pre = sum_rec = sum_f1 = 0
    for orig, tree in zip(groundtruth, to_eval):
        pre, rec, f1 = calculate_precision_recall(orig, tree)
        sum_pre += pre
        sum_rec += rec
        sum_f1 += f1
    return sum_pre/len(groundtruth), sum_rec/len(groundtruth), sum_f1/len(groundtruth)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("spark-index")

mode = "test"

if mode == "evaluate":
    queries, groundtruth = get_json_question_and_groundtruth('./QA/qa')
    with open('md_tree.json', 'r', encoding='utf-8') as f:
        md_tree = json.load(f)
    parent_dict = build_parent_dict(md_tree)
    embedded_queries = get_embedding(queries)
    original = topK_retrieval(index, embedded_queries, 10)
    print(evaluate_precision_recall(groundtruth, original))
else:
    queries, _ = get_json_question_and_groundtruth(QUESTIONS_INPUT)
    with open('md_tree.json', 'r', encoding='utf-8') as f:
        md_tree = json.load(f)
    parent_dict = build_parent_dict(md_tree)
    embedded_queries = get_embedding(queries)
    original = topK_retrieval(index, embedded_queries, 10)
    tree_context = tree_retrieval(parent_dict, topK_retrieval(index, embedded_queries, 2), 10)

    os.makedirs('original', exist_ok=True)
    os.makedirs('tree', exist_ok=True)

    for i in range(len(queries)):
        with open(os.path.join('original', f'query_{i}.txt'), 'w', encoding='utf-8') as org:
            org.write(f"With the following context {read_md_contents(original[i])} \n Answer the question: {queries[i]}\n")
        with open(os.path.join('tree', f'query_{i}.txt'), 'w', encoding='utf-8') as tree_file:
            tree_file.write(f"With the following context {read_md_contents(tree_context[i])} \n Answer the question: {queries[i]}\n")
