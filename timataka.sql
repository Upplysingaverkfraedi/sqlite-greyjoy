-- Create hlaup table
CREATE TABLE hlaup (
    id INTEGER PRIMARY KEY,   -- Preserve 'id' from CSV (race ID)
    upphaf DATETIME NOT NULL,
    endir DATETIME NOT NULL,
    nafn TEXT NOT NULL,
    fjoldi INTEGER NOT NULL
);

-- Create timataka table
CREATE TABLE timataka (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each row
    id INTEGER,                      -- Rank within the race
    hlaup_id INTEGER,                -- Reference to hlaup (which race)
    nafn TEXT NOT NULL,              -- Name of the participant
    timi TIME NOT NULL,              -- Time taken for the run
    kyn TEXT,                        -- Gender (optional)
    aldur INTEGER,                   -- Age of the participant
    FOREIGN KEY (hlaup_id) REFERENCES hlaup(id),
    UNIQUE (hlaup_id, nafn)          -- Ensure unique participant per race
);
