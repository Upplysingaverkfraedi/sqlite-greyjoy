-- 1. Telja fjölda keppenda í hverju hlaupi samkvæmt 'timataka' töflunni
SELECT hlaup_id, COUNT(*) AS keppendafjoldi
FROM timataka
GROUP BY hlaup_id;

-- Þessi fyrirspurn telur fjölda skráninga í 'timataka' fyrir hvert 'hlaup_id',
-- sem sýnir fjölda keppenda í hverju hlaupi.

-- 2. Bera saman fjölda keppenda við 'fjoldi' dálkinn í 'hlaup' töflunni
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(t.entry_id) AS fjoldi_raunverulegur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
ORDER BY h.id;

-- Hér tengjum við 'hlaup' og 'timataka' töflurnar til að bera saman
-- skráðan fjölda keppenda í 'hlaup' (h.fjoldi_skradur) við raunverulegan
-- fjölda keppenda samkvæmt 'timataka' (fjoldi_raunverulegur).

-- 3. Finna hlaup þar sem fjöldinn passar ekki saman
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(t.entry_id) AS fjoldi_raunverulegur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
HAVING h.fjoldi != COUNT(t.entry_id)
ORDER BY h.id;

-- Þessi fyrirspurn finnur hlaup þar sem skráður fjöldi keppenda í 'hlaup' töflunni
-- passar ekki við raunverulegan fjölda keppenda í 'timataka' töflunni.

-- 4. Uppfæra 'fjoldi' dálkinn í 'hlaup' töflunni til að samsvara raunverulegum fjölda
UPDATE hlaup
SET fjoldi = (
    SELECT COUNT(*)
    FROM timataka
    WHERE timataka.hlaup_id = hlaup.id
);

-- Þessi skipun uppfærir 'fjoldi' dálkinn í 'hlaup' töflunni þannig að hann
-- samsvari fjölda keppenda í 'timataka' töflunni fyrir hvert hlaup.

-- 5. Telja einstaka keppendur í hverju hlaupi (ef þörf er á að telja einstaka)
SELECT hlaup_id, COUNT(DISTINCT nafn) AS einstakir_keppendur
FROM timataka
GROUP BY hlaup_id;

-- Þessi fyrirspurn telur fjölda einstaka keppenda í hverju hlaupi
-- með því að nota 'COUNT(DISTINCT nafn)' til að forðast afrit.

-- 6. Bera saman fjölda einstaka keppenda við 'fjoldi' dálkinn í 'hlaup' töflunni
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(DISTINCT t.nafn) AS fjoldi_einstakir_keppendur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
ORDER BY h.id;

-- Hér berum við saman skráðan fjölda keppenda við fjölda einstaka keppenda
-- til að sjá hvort einhverjir afrit séu til staðar.

-- 7. Finna hlaup þar sem fjöldi einstaka keppenda passar ekki við skráðan fjölda
SELECT h.id AS hlaup_id,
       h.fjoldi AS fjoldi_skradur,
       COUNT(DISTINCT t.nafn) AS fjoldi_einstakir_keppendur
FROM hlaup h
LEFT JOIN timataka t ON h.id = t.hlaup_id
GROUP BY h.id, h.fjoldi
HAVING h.fjoldi != COUNT(DISTINCT t.nafn)
ORDER BY h.id;