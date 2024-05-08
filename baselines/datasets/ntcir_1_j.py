import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datasets import Dataset
from baselines.datasets.base import DatasetBase

class Ntcir1J(DatasetBase):

    MD5 = {
        "topics": "94b0e23e8c3d92378f60c7e2ff7b9269",
        "qrels": "bfc4e420ec74d5a9473519f4463bbc9a",
        "docs": "26356b2fc2fd68c3d5fa6c7729770cca",
    }

    TOPIC_FILENAME = "topic0031-0083"
    QRELS_FILENAME = "rel2_ntc1-j1_0031-0083"
    DOC_FILENAME = "ntc1-j1"
    GRADE_LETTER_TO_INT = {"A": 2, "B": 1, "C": 0}

    def get_topics(self, filepath):
        topic_filepath = os.path.join(self.config["ntcir1"]["topic_dirpath"], self.TOPIC_FILENAME)
        def _read_topic_file():
            with open(topic_filepath, 'r', encoding="euc_jp") as f:
                soup = BeautifulSoup(f, "html.parser")
            topics = soup.find_all("topic")
            for topic in topics:
                query_id = topic.attrs["q"]
                query_id = int(query_id)
                query = topic.find("title").text.strip()
                yield {"query_id": query_id, "query": query}

        dataset = Dataset.from_generator(_read_topic_file)
        dataset.to_csv(filepath, sep='\t', index=None, header=None)

    def get_qrels(self, filepath):
        qrels_filepath = os.path.join(self.config["ntcir1"]["mlir_dirpath"], self.QRELS_FILENAME)
        def _read_qrels_file():
            with open(qrels_filepath, 'r', encoding="euc_jp") as f:
                for line in f:
                    qid, grade, did, _, _ = line.split("\t")
                    qid = int(qid)
                    yield {
                        "qid": qid, 
                        "Q0": "Q0",
                        "did": did,
                        "grade": self.GRADE_LETTER_TO_INT[grade]
                        }

        dataset = Dataset.from_generator(_read_qrels_file)
        dataset.to_csv(filepath, sep=' ', index=None, header=None)

    def get_docs(self, filepath):
        doc_filepath = os.path.join(self.config["ntcir1"]["mlir_dirpath"], self.DOC_FILENAME)

        def _process_rec(rec_text):
            soup = BeautifulSoup(rec_text, "html.parser")
            docid = soup.find("accn").text.strip()
            title = soup.find("titl").text.strip()
            abst = soup.find("abst").text.strip()
            contents = f"{title}\n{abst}"
            return {"id": docid, "contents": contents}

        def _read_doc_file():
            with open(doc_filepath, 'r', encoding="euc_jp", errors="ignore") as f:
                buffer = next(f)
                for line in f:
                    line = line.strip()
                    buffer += line
                    if line.startswith("</REC>"):
                        yield _process_rec(buffer)
                        buffer = ""

        dataset = Dataset.from_generator(_read_doc_file)
        self.to_multi_jsonl(dataset, filepath)