Eftirfarandi þarf að vera sett upp á tölvunni
   -Python
   -SQLite

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
# Liður 2 - Saga Ísfólksins

## Yfirlit

Þetta verkefni vinnur með `isfolkid.db` SQLite gagnagrunninn, sem inniheldur gögn tengd bókabálkinum *Saga Ísfólksins* eftir Margit Sandemo. Verkefnið felur í sér að framkvæma SQL fyrirspurnir til að fá upplýsingar um persónur, bækur og fjölskyldutengsl.

## Forkröfur

Til að keyra þetta verkefni þarftu eftirfarandi:
- Gagnagrunnsskrána (`isfolkid.db`) í `sqlite-greyjoy\data` og SQL skipanaskrána (`isfolkid.sql`) í `sqlite-greyjoy` möppunni.

## Hvernig á að keyra kóðann

Til að keyra fyrirspurnirnar á `isfolkid.db`, fylgdu eftirfarandi skrefum:

### 1. Opnaðu skipanaglugga (Command Prompt)

1. Ýttu á `Win + R`, skrifaðu `cmd`, og ýttu á Enter.
2. Færðu þig í verkefnamöppuna `sqlite-greyjoy` með því að nota `cd` skipunina. Dæmi:

   ```bash
   cd path\to\sqlite-greyjoy
   ```

### 2. Keyrðu SQLite3

Til að keyra SQLite gagnagrunninn með `isfolkid.db` skrána skaltu skrifa:

```bash
sqlite3 data/isfolkid.db
```

Þetta mun opna SQLite3 gagnagrunnsgluggann og tengja við `isfolkid.db` gagnagrunninn.

### 3. Hladdu inn SQL fyrirspurnunum úr skránni

Til að framkvæma allar SQL fyrirspurnir í einu úr skránni `isfolkid.sql`, notaðu:

```bash
.read isfolkid.sql
```

Þetta keyrir allar fyrirspurnir sem eru skilgreindar í `isfolkid.sql` skránni og birtir niðurstöður.

## Keyra einstakar SQL skipanir

Ef þú vilt keyra einstaka SQL fyrirspurnir beint úr skipanaglugga án þess að opna SQLite gagnagrunninn, geturðu notað eftirfarandi skipan:

```bash
sqlite3 data/isfolkid.db "SELECT COUNT(*) AS adalpersonur FROM books;"
```

Þetta mun keyra SQL fyrirspurnina án þess að opna gagnagrunnsgluggann.



# Liður 3 - Lýsing á kóða fyrir úrslitavinnslu frá tímataka.net (Fyrir branchinn lidur3regex, forritið lidur3regex.py)

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

`python3 lidur3regex.py --links_file /Slóð/Að/Þinni/Textaskrá/urls.txt --output_dir results/ --metadata_output metadata.json --debug`


# merge_csvs.py

Þetta Python forrit sameinar allar CSV skrár í tilteknum möppum og skrifar þær í eina sameinaða skrá. Forritið tekur á móti tveimur möppum, einni fyrir niðurstöður og annarri fyrir metadata (gagnaskrá) og sameinar skrárnar innan hvorrar möppu.

## Skilgreiningar

- `results_dir`: Slóðin að möppunni sem inniheldur CSV skrárnar með niðurstöðum sem á að sameina.
- `metadata_dir`: Slóðin að möppunni sem inniheldur CSV skrárnar með metadata (gagnaskrám) sem á að sameina.
- `merged_results_file`: Slóðin þar sem sameinaða niðurstöðuskráin verður vistuð.
- `merged_metadata_file`: Slóðin þar sem sameinaða metadata skráin verður vistuð.

## Notkun

1. **Stilla möppur**: Tilgreindu réttar slóðir að niðurstöðum og metadata skrám í breytunum `results_dir` og `metadata_dir` í kóðanum.

2. **Keyra forritið**:
   Keyrðu forritið með því að opna skipanalínu og keyra eftirfarandi skipun:

   ```bash
   python3 merge_csvs.py


# timataka.sql - Gagnagrunnstaflanir fyrir hlaupagagnagrunn

Þetta SQL skjal inniheldur skipanir til að búa til tvær töflur, `hlaup` og `timataka`, til að geyma upplýsingar um hlaupa viðburði og tímatöku þátttakenda. Tengsl milli töflanna eru útfærð með framandlykli (`FOREIGN KEY`) sem vísar frá `timataka` yfir í `hlaup`.

## Tafluskipulag

### Tafla: `hlaup`

Taflan `hlaup` geymir grunnupplýsingar um hlaup eða keppnir.

## Notkun

2. **Keyra forritið**:
   Keyrðu forritið með því að opna skipanalínu og keyra eftirfarandi skipun:

   ```bash
   sqlite3 timataka.db
   .read timataka.sql

# fixed_csvs.py CSV to SQLite gagnainnflutningsverkfæri

Þetta Python forrit hleður inn, hreinsar og flytur gögn úr CSV skrám yfir í SQLite gagnagrunn. Það vinnur með tvær tegundir af gögnum: hlaupa metadata (keppnisupplýsingar) og tímatökuupplýsingar þátttakenda. Eftir að gögnin hafa verið hreinsuð eru þau sett í SQLite gagnagrunn.

## Skrár sem eru notaðar

- **Niðurstöðuskrá (results CSV)**: Inniheldur tímatökuupplýsingar fyrir keppendur í hlaupum.
- **Metadata skrá (metadata CSV)**: Inniheldur grunnupplýsingar um keppnir (hlaup).
- **SQLite gagnagrunnur**: Þar sem hreinsuð gögn verða vistuð.

## Skilgreiningar

- `results_file`: Slóðin að CSV skrá með niðurstöðum.
- `metadata_file`: Slóðin að CSV skrá með metadata upplýsingum.
- `db_file`: Slóðin að SQLite gagnagrunns skrá sem gögnin verða flutt inn í.

## Notkun

1. **Setja upp Python umhverfi**:
   Gakktu úr skugga um að þú sért með eftirfarandi pakka uppsetta í Python umhverfi þínu:

   ```bash
   pip install pandas sqlite3
   python3 fixed_csvs.py


   # SQL Fyrirspurnir til að Greina og Uppfæra Keppendagagnagrunn

Þetta verkefni inniheldur SQL fyrirspurnir sem vinna með hlaup og keppendur í gagnagrunni. Fyrirspurnirnar telja keppendur, bera saman skráðan fjölda við raunverulegan fjölda, uppfæra gögnin ef ósamræmi finnst, og athuga hvort afrit séu til staðar. Verkefnið gerir ráð fyrir tveimur töflum:

- **`hlaup`**: Tafla sem geymir upplýsingar um hvert hlaup (keppni).
- **`timataka`**: Tafla sem geymir tímatöku og upplýsingar um keppendur.

## Tafluskipulag

### Tafla: `hlaup`
| Dálkur  | Tegund    | Lýsing                                         |
|---------|-----------|------------------------------------------------|
| `id`    | INTEGER   | Aðallykill fyrir hvert hlaup                   |
| `upphaf`| DATETIME  | Upphafstími hlaups                             |
| `endir` | DATETIME  | Endatími hlaups                                |
| `nafn`  | TEXT      | Nafn hlaupsins                                 |
| `fjoldi`| INTEGER   | Skráður fjöldi keppenda                        |

### Tafla: `timataka`
| Dálkur      | Tegund    | Lýsing                                         |
|-------------|-----------|------------------------------------------------|
| `entry_id`  | INTEGER   | Aðallykill fyrir hverja tímatökufærslu         |
| `hlaup_id`  | INTEGER   | Framandlykill sem tengir tímatöku við hlaup     |
| `nafn`      | TEXT      | Nafn keppanda                                  |
| `timi`      | TIME      | Tími keppanda                                  |
| `kyn`       | TEXT      | Kyn keppanda                                   |
| `aldur`     | INTEGER   | Aldur keppanda                                 |

## Fyrirspurnir

### 1. Telja fjölda keppenda í hverju hlaupi

```sql
SELECT hlaup_id, COUNT(*) AS keppendafjoldi
FROM timataka
GROUP BY hlaup_id;
Þessi fyrirspurn telur fjölda keppenda í hverju hlaupi með því að skoða skráningar í timataka töflunni og hópa eftir hlaup_id.

2. Bera saman fjölda keppenda í hlaup og timataka
sql
Copy code
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(t.entry_id) AS fjoldi_raunverulegur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
ORDER BY h.id;
Þessi fyrirspurn ber saman fjölda keppenda í hlaup (skráður fjöldi) við raunverulegan fjölda keppenda í timataka og sýnir hvort þau gögn passi saman.

3. Finna hlaup þar sem fjöldi keppenda passar ekki saman
sql
Copy code
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(t.entry_id) AS fjoldi_raunverulegur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
HAVING h.fjoldi != COUNT(t.entry_id)
ORDER BY h.id;
Þessi fyrirspurn finnur þau hlaup þar sem skráður fjöldi keppenda í hlaup taflan passar ekki við raunverulegan fjölda í timataka.

4. Uppfæra skráðan fjölda keppenda í hlaup töflunni
sql
Copy code
UPDATE hlaup
SET fjoldi = (
    SELECT COUNT(*)
    FROM timataka
    WHERE timataka.hlaup_id = hlaup.id
);
Þessi fyrirspurn uppfærir dálkinn fjoldi í hlaup töflunni þannig að hann endurspegli raunverulegan fjölda keppenda úr timataka.

5. Telja einstaka keppendur í hverju hlaupi
sql
Copy code
SELECT hlaup_id, COUNT(DISTINCT nafn) AS einstakir_keppendur
FROM timataka
GROUP BY hlaup_id;
Fyrirspurnin telur einstaka keppendur í hverju hlaupi með því að nota COUNT(DISTINCT nafn) til að forðast afrit af nöfnum keppenda.

6. Bera saman fjölda einstaka keppenda við skráðan fjölda
sql
Copy code
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(DISTINCT t.nafn) AS fjoldi_einstakir_keppendur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
ORDER BY h.id;
Hér er skráðum fjölda keppenda í hlaup borið saman við fjölda einstaka keppenda (án afrita) í timataka til að athuga hvort einhverjir keppendur séu skráðir oftar en einu sinni.

7. Finna hlaup þar sem fjöldi einstaka keppenda passar ekki við skráðan fjölda
sql
Copy code
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(DISTINCT t.nafn) AS fjoldi_einstakir_keppendur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
HAVING h.fjoldi != COUNT(DISTINCT t.nafn)
ORDER BY h.id;
Þessi fyrirspurn finnur hlaup þar sem fjöldi einstaka keppenda er ekki sá sami og skráður fjöldi keppenda í hlaup töflunni.

. **Keyra forritið**:
   Keyrðu forritið með því að opna skipanalínu og keyra eftirfarandi skipun:

   ```bash
   sqlite3 timataka.db
   .read skipanir.sql



 **Keyra forritið í heild og réttri röð**:
   Keyrðu forritið með því að opna skipanalínu og keyra eftirfarandi skipun:
```bash
python3 lidur3regex.py --links_file /Slóð/Að/Þinni/Textaskrá/urls.txt --output_dir results/ --metadata_output metadata.json --debug
sqlite3 timataka.db
.read timataka.sql
.quit
python3 merge_csvs.py
python3 fixed_csvs.py
sqlite3 timataka.db
.read skipanir.sql


Hér er vert að athuga að setja slóðina þína að textaskránni (urls.txt) í þessa skpun.
einnig þarf að breyta öllum filepaths í liður3regex.py, merge_csvs.py og fixed_csvs.py í þitt rétt filepath fyrir þína tölvu


