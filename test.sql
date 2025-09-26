SELECT COUNT(*) FROM contacts 
WHERE email LIKE "%shvedskiy@maction.ru%"
            
SELECT * FROM contacts 
WHERE email LIKE "%shvedskiy@maction.ru%"
ORDER BY created_at DESC 
LIMIT 20 OFFSET 0


SELECT COUNT(*) FROM contacts
WHERE name LIKE '%shvedskiy@m3action.ru%' OR email LIKE '%shvedskiy@m3action.ru%' OR phone LIKE '%shvedskiy@m3action.ru%'

SELECT * FROM contacts WHERE id = 6

CREATE TABLE IF NOT EXISTS contacts2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    message TEXT NOT NULL,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)