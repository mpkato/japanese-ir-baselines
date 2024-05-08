import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datasets import Dataset
from baselines.datasets.ntcir_j import NtcirJ

class Ntcir1J(NtcirJ):

    def get_docs(self, filepath):
        doc_filepath = self.config["doc_filepath"]

        def _process_rec(record):
            docid = record.find("accn").text.strip()
            title = record.find("titl").text.strip()
            abst = record.find("abst").text.strip()
            contents = f"{title}\n{abst}"
            return {"id": docid, "contents": contents}
        
        def _read_doc_file():
            for record in NtcirJ.iter_records(doc_filepath):
                yield _process_rec(record)

        dataset = Dataset.from_generator(_read_doc_file)
        self.to_multi_jsonl(dataset, filepath)