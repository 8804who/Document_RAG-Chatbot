from langchain.smith import RunEvalConfig, run_on_dataset
from evaluate.langsmith_setting import client


def retrieve_metrics(run, example):
    retrieved_docs = run.outputs.get("source_documents", [])
    retrieved_ids = [doc.metadata.get("doc_id") for doc in retrieved_docs]

    relevant_ids = set(example["relevant_doc_ids"])
    hits = relevant_ids.intersection(set(retrieved_ids))

    recall = len(hits) / len(relevant_ids) if relevant_ids else 0.0
    precision = len(hits) / len(retrieved_ids) if retrieved_ids else 0.0
    rr = 0.0

    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            rr = 1.0 / rank
            break

    return {"Recall@k": recall, "Precision@k": precision, "MRR": rr}


def evaluate_retriever(model, dataset_name):
    eval_config = RunEvalConfig(
        evaluators=[retrieve_metrics],
    )

    results = run_on_dataset(
        client=client,
        dataset_name=dataset_name,
        llm_or_chain_factory=model,
        evaluation=eval_config,
    )
    return results
