# grounding-check

構造化出力を「スキーマ検証 (A)」「+ 原文照合 (B)」「+ 項目間整合 (C)」で検査し、
手で作った誤り入りケース 12 件と正常ケース 2 件に対する検出数を数える。

## 前提

Python 3.11 以上。標準ライブラリのみ、API キー不要。

## 動かし方

```bash
python3 grounding_check.py data/cases.json
```

## 期待される出力

```text
c01 correct           A:通す B:通す C:通す  
c02 correct           A:通す B:通す C:通す  
c03 schema            A:弾く B:弾く C:弾く  type:fee_yen
c04 schema            A:弾く B:弾く C:弾く  format:start_date
c05 schema            A:弾く B:弾く C:弾く  type:venue
c06 invented_value    A:通す B:弾く C:弾く  ungrounded:venue
c07 invented_value    A:通す B:弾く C:弾く  ungrounded:fee_yen
c08 invented_value    A:通す B:弾く C:弾く  ungrounded:start_date
c09 invented_value    A:通す B:弾く C:弾く  ungrounded:event
c10 order             A:通す B:通す C:弾く  order:end_date<start_date
c11 sum               A:通す B:通す C:弾く  sum:total_yen
c12 wrong_place_value A:通す B:通す C:通す  
c13 wrong_place_value A:通す B:通す C:通す  
c14 paraphrase        A:通す B:弾く C:弾く  ungrounded:venue

誤り入りケース 12 件 / 正常ケース 2 件
A: 誤りを弾いた 3/12, 正常を誤って弾いた 0/2
B: 誤りを弾いた 8/12, 正常を誤って弾いた 0/2
C: 誤りを弾いた 10/12, 正常を誤って弾いた 0/2
```

## 確かめていない範囲

`data/cases.json` のケースは手で作ったもので、実際のモデル出力ではない。モデルがどのくらい間違えるかは確かめていない。

## 記事

https://zenn.dev/liatris/articles/20261112-structured-output-grounding-check
