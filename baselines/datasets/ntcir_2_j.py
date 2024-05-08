from datasets import Dataset
from baselines.datasets.ntcir_j import NtcirJ

class Ntcir2J(NtcirJ):

    def get_docs(self, filepath):
        ntc1_j1_filepath = self.config["doc_filepath"]["ntc1-j1"]
        ntc2_j1g_filepath = self.config["doc_filepath"]["ntc2-j1g"]
        ntc2_j1k_filepath = self.config["doc_filepath"]["ntc2-j1k"]

        def _process_rec(record, title_tag_name):
            docid = record.find("accn").text.strip()
            title = record.find(title_tag_name).text.strip()
            abst = record.find("abst").text.strip()
            contents = f"{title}\n{abst}"
            return {"id": docid, "contents": contents}
        
        def _read_doc_file():
            for record in NtcirJ.iter_records(ntc1_j1_filepath):
                record = _process_rec(record, "titl")
                record["id"] = record["id"].replace('gakkai-', 'gakkai-j-')
                yield record

            for record in NtcirJ.iter_records(ntc2_j1g_filepath):
                yield _process_rec(record, "titl")

            for record in NtcirJ.iter_records(ntc2_j1k_filepath):
                yield _process_rec(record, "pjnm")

        dataset = Dataset.from_generator(_read_doc_file)
        self.to_multi_jsonl(dataset, filepath)