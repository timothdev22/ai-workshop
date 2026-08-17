# Day 1 RAG workshop package

This directory contains a Colab-first Day 1 lesson built around a controlled RAG comparison.

## Files

- `DAY1_RAG_GUIDE.md` — concepts, teaching flow, acceptance checks, and sources
- `MULTIHOP_ATTRIBUTION.md` — dataset attribution, license, and snapshot description
- `notebooks/day1_rag_workshop_colab.ipynb` — self-contained instructor/student notebook
- `student_code/rag_workshop.py` — the transparent implementation used by the notebook
- `student_code/data/multihop_corpus.json` — 30 attributed benchmark articles
- `student_code/data/multihop_eval_cases.json` — 12 balanced MultiHopRAG cases
- `student_code/data/multihop_subset_manifest.json` — exact upstream rows and hard negatives
- `student_code/data/corpus.json` — nine original OrbitDesk safety documents
- `student_code/data/eval_cases.json` — 12 synthetic safety cases
- `student_code/test_rag_workshop.py` — offline acceptance and safety tests
- `student_code/requirements.txt` — Colab dependencies
- `prepare_multihop_subset.py` — reproducibly rebuilds the attributed snapshot

## Local check

```bash
cd student_code
python -m pip install -r requirements.txt
pytest -q -s
```

The notebook embeds copies of the module, corpus, cases, and tests, so it can run in a fresh Colab session without cloning this repository.

## Optional live generation

Retrieval, evaluation, charts, and tests run without an API key. For the live Nscale generation cells, add these values to Colab Secrets:

- `NSCALE_SERVICE_TOKEN`
- `NSCALE_MODEL_ID`

The notebook uses the documented base URL `https://inference.api.nscale.com/v1`. Verify the assigned model ID during the workshop freeze instead of guessing it.
