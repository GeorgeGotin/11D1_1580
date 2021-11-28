ALTER TABLE clients ADD COLUMN reg_date DATE;
UPDATE clients SET reg_date = DATE(registration_date);
ALTER TABLE clients DROP COLUMN registration_date;
ALTER TABLE clients RENAME COLUMN reg_date TO registration_date;