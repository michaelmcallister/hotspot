CREATE TABLE model_risk (
  brand TEXT,
  model TEXT,
  total INTEGER,
  best_match TEXT,
  score INTEGER,
  percentage DOUBLE PRECISION,
  model_risk DOUBLE PRECISION
);

CREATE TABLE postcode_risk (
  postcode TEXT,
  locality TEXT,
  long DOUBLE PRECISION,
  lat DOUBLE PRECISION,
  lgaregion TEXT,
  local_government_area TEXT,
  motorcycle_theft_rate DOUBLE PRECISION,
  postcode_risk DOUBLE PRECISION
);

CREATE TABLE default_risk (
  model_default_risk DOUBLE PRECISION,
  postcode_default_risk DOUBLE PRECISION
);

CREATE TABLE user_contribution (
  parking_id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT NOT NULL,
  suburb TEXT NOT NULL,
  postcode TEXT NOT NULL,
  type TEXT CHECK(type IN ('on-street', 'off-street', 'secure')) NOT NULL,
  /* The integers map to the UI, poor (1), fair (2), good (3), excellent (4) */
  lighting INTEGER CHECK(lighting IN (1, 2, 3, 4)),
  cctv BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE facilities (
  facility_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  facility_name TEXT NOT NULL UNIQUE 
);

CREATE TABLE user_contribution_facilities (
  parking_id INTEGER NOT NULL,
  facility_id INTEGER NOT NULL,
  PRIMARY KEY (parking_id, facility_id), 
  FOREIGN KEY (parking_id) REFERENCES user_contributions(parking_id) ON DELETE CASCADE, 
  FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE
);

INSERT INTO facilities (facility_name) VALUES 
('Toilet'),
('Cafe'),
('Lockers'),
('Covered parking'),
('Security guard'),
('Accessible');

CREATE TABLE victorian_addresses (
    address TEXT NOT NULL,
    suburb TEXT NOT NULL,
    postcode TEXT NOT NULL
);

CREATE TABLE postcode_distances (
    primary_postcode TEXT NOT NULL,
    secondary_postcode TEXT NOT NULL,
    distance_meters REAL NOT NULL
);

CREATE TABLE postcode_yearly_thefts (
    year INTEGER NOT NULL,
    postcode TEXT NOT NULL,
    yearly_thefts REAL
);

-- Add unique constraint to prevent duplicate parking locations, this ensures each unique address/suburb/postcode combination can only exist once
CREATE UNIQUE INDEX idx_user_contribution_unique_location
ON user_contribution(address, suburb, postcode);

CREATE INDEX IF NOT EXISTS idx_user_contribution_postcode
ON user_contribution(postcode);
