# NER Datasets

Dokumentasi lengkap dataset Named Entity Recognition (NER) yang digunakan dalam proyek ini.

## Sumber Data

Kedua dataset berasal dari **IndoNLU Benchmark**, sebuah kumpulan benchmark untuk pemrosesan bahasa alami Indonesia yang dikembangkan oleh IndoNLP.

**Repository**: https://github.com/IndoNLP/indonlu

**Paper**: Wilie, B., Vincentio, K., Winata, G. I., Cahyawijaya, S., Li, X., Lim, Z. Y., ... & Purwarianti, A. (2020). IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding. In Proceedings of AACL-IJCNLP 2020.

---

## NERGrit Dataset

Dataset NER yang dikumpulkan dari berita dan teks formal Indonesia.

### Statistik

| Split | Jumlah Kalimat | Jumlah Token |
|-------|----------------|--------------|
| Train | 1,672 | ~57,882 |
| Valid | 209 | ~7,192 |
| Test | - | ~7,063 |

### Entity Types

| Tag | Deskripsi | Contoh |
|-----|-----------|--------|
| `B-PERSON` / `I-PERSON` | Nama orang | Joko Widodo, Masamune |
| `B-PLACE` / `I-PLACE` | Nama tempat/lokasi | Jakarta, Seulawah, Provinsi Aceh |
| `B-ORGANISATION` / `I-ORGANISATION` | Nama organisasi | Kementerian, Grammy Awards |
| `O` | Non-entity | kata-kata biasa |

### Distribusi Entity (Train Set)

| Entity | B-tag | I-tag | Total |
|--------|-------|-------|-------|
| PERSON | 1,618 | 1,305 | 2,923 |
| PLACE | 2,688 | 2,288 | 4,976 |
| ORGANISATION | 1,015 | 1,204 | 2,219 |

### Format File

**CoNLL Format** (`.txt`):
```
Kontribusinya	O
terhadap	O
industri	O
Joko	B-PERSON
Widodo	I-PERSON
```

**JSON Format** (`.json`):
```json
[
  {
    "tokens": ["Kontribusinya", "terhadap", "industri", "Joko", "Widodo"],
    "tags": ["O", "O", "O", "B-PERSON", "I-PERSON"]
  }
]
```

### Sumber Langsung

```
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nergrit_ner-grit/train_preprocess.txt
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nergrit_ner-grit/valid_preprocess.txt
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nergrit_ner-grit/test_preprocess.txt
```

---

## NERP Dataset

Dataset NER yang lebih besar dengan lebih banyak entity types, dikumpulkan dari berbagai sumber berita Indonesia.

### Statistik

| Split | Jumlah Kalimat | Jumlah Token |
|-------|----------------|--------------|
| Train | 6,720 | ~163,129 |
| Valid | 840 | ~20,469 |
| Test | - | ~20,792 |

### Entity Types

| Tag | Deskripsi | Contoh |
|-----|-----------|--------|
| `B-PPL` / `I-PPL` | Person/People | Amos Kenda, Ahok |
| `B-PLC` / `I-PLC` | Place/Location | Manado, Jakarta, Monas |
| `B-ORG` / `I-ORG` | Organization | - |
| `B-EVT` / `I-EVT` | Event | - |
| `B-IND` / `I-IND` | Industry/Product | - |
| `B-FNB` / `I-FNB` | Food and Beverage | - |
| `O` | Non-entity | kata-kata biasa |

### Distribusi Entity (Train Set)

| Entity | B-tag | I-tag | Total |
|--------|-------|-------|-------|
| PPL (Person) | 4,845 | 2,818 | 7,663 |
| PLC (Place) | 4,379 | 2,005 | 6,384 |
| IND (Industry) | 3,065 | 2,202 | 5,267 |
| EVT (Event) | 1,022 | 1,622 | 2,644 |
| FNB (Food/Bev) | 542 | 319 | 861 |

### Sumber Langsung

```
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nerp_ner-prosa/train_preprocess.txt
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nerp_ner-prosa/valid_preprocess.txt
https://raw.githubusercontent.com/IndoNLP/indonlu/master/dataset/nerp_ner-prosa/test_preprocess.txt
```

---

## Penggunaan dalam Proyek

Dataset **NERGrit** digunakan sebagai benchmark utama untuk membandingkan dua model NER:
- **Model Cahya**: `cahya/bert-base-indonesian-NER`
- **Model Server**: Fine-tuned IndoBERT untuk NER

### Mapping Label

Karena kedua model menggunakan label set yang berbeda dari dataset, dilakukan mapping:

| Dataset (NERGrit) | Model Label |
|-------------------|-------------|
| PERSON | PER |
| PLACE | LOC |
| ORGANISATION | ORG |

---

## Lisensi

Dataset ini merupakan bagian dari IndoNLU Benchmark dan mengikuti lisensi yang ditetapkan oleh IndoNLP. Silakan merujuk ke repository resmi untuk informasi lisensi lengkap.

## Referensi

1. IndoNLU Repository: https://github.com/IndoNLP/indonlu
2. IndoNLU Paper: https://aclanthology.org/2020.aacl-main.85/
3. HuggingFace Datasets: https://huggingface.co/datasets/indonlp/NusaX-NER
