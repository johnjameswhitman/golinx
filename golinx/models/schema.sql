DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS link;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE link (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  owner_id INTEGER NOT NULL,  -- Original owner of link.
  type TEXT CHECK( type IN ('CUSTOM', 'SHORT')) NOT NULL,
  original_path TEXT NOT NULL,  -- Stored as originally provided path.
  canonical_path TEXT NOT NULL,  -- Stored as canonicalized path.
  destination TEXT NOT NULL,
  other_owners TEXT,  -- Holds additional users who may edit link.
  readers TEXT,  -- Determines visibility of the link.
  title TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (owner_id) REFERENCES user (id)
);
