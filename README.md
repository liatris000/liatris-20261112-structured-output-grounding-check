# grounding-check

構造化出力を「スキーマ検証 (A)」「+ 原文照合 (B)」「+ 項目間整合 (C)」で検査し、
手で作った誤り入りケース 12 件と正常ケース 2 件に対する検出数を数える。Python 3.11 標準ライブラリのみ、API キー不要。

```bash
python3 grounding_check.py data/cases.json
```

`data/cases.json` のケースは手で作ったもので、実際のモデル出力ではない。
