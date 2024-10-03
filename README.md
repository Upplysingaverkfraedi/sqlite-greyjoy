# Liður 1 - Tíðni nafna á Íslandi 

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


# Liður 3 - Lýsing á kóða fyrir úrslitavinnslu frá tímataka.net (Fyrir branchinn lidur3regex)

Þessi Python kóði er notaður til að sækja og vinna með hlaupaúrslit frá tímataka.net, vista gögnin í CSV skrár og metadata í JSON eða CSV formi. Kóðinn notar reglulegar segðir (regex) til að finna og greina dálkaheiti, línur og viðeigandi gögn úr HTML skjalinu fyrir hvert hlaup.

## Virkni kóðans

### Aðalhlutverk kóðans
1. **Les hlekki** úr tiltekinni textaskrá **urls.txt** sem innihalda lista af vefsíðum með hlaupaúrslitum.
2. **Sækir HTML gögn** frá þessum vefsíðum.
3. **Greinir dálkaheiti og gögn** (þátttakendur, tímar, kyn o.fl.) úr HTML-inu með reglulegum segðum.
4. **Vistar niðurstöður** í CSV skrár (í okkar tilviki 75 skrár) þar sem gögnin eru skipulögð í dálka: `id`, `hlaup_id`, `nafn`, `timi`, `kyn`, `aldur`.
5. **Skrifar metadata** um hlaup, svo sem heiti hlaups, þátttakendafjölda, byrjunar- og endatíma, og auðkenni hlaups.
6. Ef `--debug` flagg er sett, vistast HTML skrár fyrir hverja vefsíðu til frekari skoðunar.

### Aðal föll kóðans
- `read_links_from_file(file_path)`: Les hlekki úr textaskrá.
- `parse_column_headers(html)`: Notar regex til að finna og greina dálkaheiti í HTML töflum.
- `parse_participant_rows(html)`: Notar regex til að finna allar línur (rows) með þátttakendagögnum.
- `parse_participant_data(row)`: Notar regex til að sækja dálkagögn fyrir hvern þátttakanda.
- `fetch_html(url)`: Sækir HTML gögn frá tilteknum hlekk.
- `skrifa_nidurstodur(data, output_file)`: Vistar gögnin í CSV skrá.
- `parse_race_metadata(html)`: Finnur upplýsingar um hlaup, svo sem nafn, fjölda þátttakenda og tíma.
- `skrifa_metadata(output_file_base, idx, html)`: Vistar metadata í JSON og CSV skrár.

## Hvernig kóðinn er keyrður

Kóðinn er keyrður með eftirfarandi skipun í terminal:

```bash
python3 lidur3regex.py --links_file /Slóð/Að/Þínni/Textaskrá/urls.txt --output_dir results/ --metadata_output metadata.json --debug

Hér er vert að athuga að setja slóðina þína að textaskránni (urls.txt) í þessa skpun.


