# 1. Tíðni nafna á Íslandi - Verkefni

Þetta verkefni vinnur með tíðnigögn um eiginnöfn og millinöfn á Íslandi úr tveimur CSV skrám: `first_names_freq.csv` og `middle_names_freq.csv`. Gögnin eru lesin inn í SQLite gagnagrunn, þar sem þau eru unnin, sameinuð og greind til að svara spurningum um hópmeðlimi með ákveðin nöfn.

## Virkni kóðans

1. **Hleðsla gagna:** Kóðinn les gögnin úr tveimur CSV skrám, setur þau í töflur í SQLite gagnagrunninn, og bætir við dálknum `type` sem skilgreinir hvort nafnið sé eiginnöfn eða millinöfn.

2. **Greining:** Að lokinni innsetningu eru eftirfarandi spurningar svaraðar með SQL fyrirspurnum:
   - Hvaða hópmeðlimur á algengasta eiginnafnið? (Einar, Guðný, Halldór eða Valur)
   - Hvenær voru þessi nöfn vinsælust?
   - Hvenær komu þessi nöfn fyrst fram?

3. **Niðurstöður:** Fyrirspurnir skila niðurstöðum fyrir tíðni, vinsælustu árin, og fyrsta árið sem nöfnin birtust í gagnagrunninum.

## Keyrsla verkefnisins

Til að keyra þetta verkefni þarftu að fylgja þessum skrefum:

1. **Staðsetning skrár:**
   - Gakktu úr skugga um að eftirfarandi skrár séu í sqlite-greyjoy möppunni:
     - `data/first_names_freq.csv`
     - `data/middle_names_freq.csv`
     - `1_Tíðni_nafna_á_Íslandi/names.sql`

2. **Búa til og hlaða SQLite gagnagrunninn:**
   - Farðu í sqlite-greyjoy möppuna
   - Keyrðu eftirfarandi skipun í skipanalínu eða Command Prompt til að keyra SQL skrána og búa til gagnagrunninn:
     ```bash
     sqlite3 1_Tíðni_nafna_á_Íslandi/names_freq.db < 1_Tíðni_nafna_á_Íslandi/names.sql
     ```
