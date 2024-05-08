from bs4 import BeautifulSoup
from datasets import Dataset
from baselines.datasets.base import DatasetBase

class NtcirJ(DatasetBase):


    def get_topics(self, filepath):
        topic_filepath = self.config["topic_filepath"]
        dataset = Dataset.from_generator(NtcirJ.read_topic_file_func(topic_filepath))
        dataset.to_csv(filepath, sep='\t', index=None, header=None)

    def get_qrels(self, filepath):
        qrels_filepath = self.config["qrels_filepath"]
        grade_letter_to_int = self.config["grade_letter_to_int"]
        dataset = Dataset.from_generator(NtcirJ.read_qrels_file_func(qrels_filepath, grade_letter_to_int))
        dataset.to_csv(filepath, sep=' ', index=None, header=None)

    @staticmethod
    def read_topic_file_func(filepath):
        def _read_topic_file():
            with open(filepath, 'r', encoding="euc_jp") as f:
                soup = BeautifulSoup(f, "html.parser")
            topics = soup.find_all("topic")
            for topic in topics:
                query_id = topic.attrs["q"]
                query_id = int(query_id)
                query = topic.find("title").text.strip()
                yield {"query_id": query_id, "query": query}
        return _read_topic_file

    @staticmethod
    def read_qrels_file_func(filepath, grade_letter_to_int):
        def _read_qrels_file():
            with open(filepath, 'r', encoding="euc_jp") as f:
                for line in f:
                    qid, grade, did, _, _ = line.split("\t")
                    qid = int(qid)
                    yield {
                        "qid": qid, 
                        "Q0": "Q0",
                        "did": did,
                        "grade": int(grade_letter_to_int[grade])
                        }
        return _read_qrels_file

    @staticmethod 
    def iter_records(filepath):
        with open(filepath, 'r', encoding="euc_jp", errors="ignore") as f:
            buffer = next(f)
            for line in f:
                line = line.strip()
                buffer += line
                if line.startswith("</REC>"):
                    soup = BeautifulSoup(buffer, "html.parser")
                    buffer = ""
                    yield soup