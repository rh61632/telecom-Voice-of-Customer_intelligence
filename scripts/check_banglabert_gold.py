import pandas as pd
import numpy as np

# Let's inspect the gold standard file and see what model predictions are present
f_gold = 'data/gold_set/blind_annotation_300_annotator1.csv'
df_gold = pd.read_csv(f_gold)
print("Columns in gold set:", df_gold.columns.tolist())

# Check comprehensive_benchmark_table.md or search for BanglaBERT in gold_set/
with open('data/gold_set/gold_standard_evaluation_report.md', 'r', encoding='utf-8') as f:
    print(f.read()[:2000])

