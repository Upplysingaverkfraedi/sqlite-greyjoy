--1. Hversu margar aðalpersónur eru í bókabálkinum?
SELECT COUNT(*) AS adalpersonur FROM books;

--2. Hversu margar persónur eru í hverri bók?
SELECT COUNT(id) AS personur FROM books;

--3. Hversu oft kemur Þengill fyrir í bókunum?
SELECT COUNT(*) AS Þengill FROM books WHERE characters LIKE '%Þengill%';

--4. Hvað eru margir af Paladín ættinni?
SELECT COUNT(*) AS Paladin FROM storytel_iskisur;

--5. Hversu algengur er illi arfurinn af þeim sem eru útvalin?
SELECT COUNT(*) AS illi FROM family WHERE chosen_one like '%evil%';

--6. Hver er fæðingartíðni kvenna í bókabálkinum?
SELECT COUNT(*) AS faedingartidni FROM family WHERE gender = 'F' AND birth IS NOT NULL;

--7. Hvað er Ísfólkið margar blaðsíður samanlagt?
SELECT MAX(pages) AS bladsidur FROM books;

--8. Hvað er meðallengd hvers þáttar af Ískisum?
SELECT AVG(length) AS medallengd FROM storytel_iskisur;
