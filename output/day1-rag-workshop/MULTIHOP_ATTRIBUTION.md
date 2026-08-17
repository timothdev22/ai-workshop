# MultiHopRAG subset attribution

The afternoon benchmark snapshot in this workshop is derived from:

- **Dataset:** [yixuantt/MultiHopRAG](https://huggingface.co/datasets/yixuantt/MultiHopRAG)
- **Repository:** [yixuantt/MultiHop-RAG](https://github.com/yixuantt/MultiHop-RAG)
- **Paper:** *MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries*, Yixuan Tang and Yi Yang, COLM 2024
- **License stated by the publishers:** [ODC Attribution License (ODC-BY)](https://opendatacommons.org/licenses/by/1-0/)

The workshop snapshot contains three examples from each published question type—`inference_query`, `comparison_query`, `temporal_query`, and `null_query`—plus one deterministic lexical hard-negative article per question. Article metadata and original URLs are retained in every document.

The selection code is in `prepare_multihop_subset.py`; exact upstream row indices and hard-negative URLs are recorded in `student_code/data/multihop_subset_manifest.json`.

The synthetic OrbitDesk files are not derived from MultiHopRAG. They remain a separate safety pack for version filtering, role-based retrieval, live-tool routing, and prompt-injection exercises.
