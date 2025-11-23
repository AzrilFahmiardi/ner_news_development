"""
Script untuk mengkonversi data NER dari format CSV ke format JSON Label Studio.

File ini membaca CSV yang berisi teks berita dan ground truth entitas (PER, LOC, ORG),
lalu mengkonversi ke format JSON yang kompatibel dengan Label Studio untuk proses
anotasi dan review Named Entity Recognition (NER).
"""

import pandas as pd
import json
import ast
import re

NAMA_FILE_CSV = "2025_07_gt_null_400.csv"
NAMA_FILE_JSON_OUTPUT = "data_berlabel3.json"
TEXT_TAG_NAME = "news_text"
LABELS_TAG_NAME = "ner_label"

def convert_to_ls_format(df):
    tasks = []
    print("Memulai konversi...")

    for index, row in df.iterrows():
        text = str(row['summary'])
        results = []
        
        # Daftar entitas 
        entity_map = [
            ("PER", "gt_PER"),
            ("LOC", "gt_LOC"),
            ("ORG", "gt_ORG")
        ]

        for label, column_name in entity_map:
            try:
                entities = ast.literal_eval(str(row[column_name]))
                
                if not isinstance(entities, list):
                    continue

                for entity_text in entities:
                    entity_text = str(entity_text)
                    for match in re.finditer(re.escape(entity_text), text):
                        start, end = match.span()
                        results.append({
                            "from_name": LABELS_TAG_NAME,
                            "to_name": TEXT_TAG_NAME,
                            "type": "labels",
                            "value": {
                                "start": start,
                                "end": end,
                                "text": entity_text,
                                "labels": [label]
                            }
                        })
            except (ValueError, SyntaxError):
                continue

        # Struktur task untuk Label Studio
        task = {
            "data": {
                "summary": text 
            },
            "predictions": [{
                "result": results
            }]
        }
        tasks.append(task)
        
        if (index + 1) % 100 == 0:
            print(f"  {index + 1} baris telah diproses...")

    return tasks

try:
    df = pd.read_csv(NAMA_FILE_CSV)
except FileNotFoundError:
    print(f"ERROR: File '{NAMA_FILE_CSV}' tidak ditemukan. Pastikan nama file sudah benar.")
    exit()

tasks_data = convert_to_ls_format(df)

with open(NAMA_FILE_JSON_OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(tasks_data, f, ensure_ascii=False, indent=2)

print(f"\nSelesai! Data telah dikonversi dan disimpan ke '{NAMA_FILE_JSON_OUTPUT}'")
print(f"Total {len(tasks_data)} baris data siap untuk diimpor ke Label Studio.")