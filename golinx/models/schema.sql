DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS link;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER,  -- Original creator of record.
  updated_by INTEGER,  -- Most recent editor of record.
  is_deleted BOOLEAN,  -- Soft delete.
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  FOREIGN KEY (created_by) REFERENCES user (id),
  FOREIGN KEY (updated_by) REFERENCES user (id)
);

CREATE TABLE link (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,  -- Original creator of record.
  updated_by INTEGER NOT NULL,  -- Most recent editor of record.
  is_deleted BOOLEAN,  -- Soft delete.
  owner_id INTEGER NOT NULL,  -- Current owner of the record.
  link_type TEXT CHECK( link_type IN ('CUSTOM', 'SHORT')) NOT NULL,
  original_path TEXT NOT NULL,  -- Stored as originally provided path.
  canonical_path TEXT NOT NULL UNIQUE,  -- Stored as canonicalized path.
  destination TEXT NOT NULL,
  other_owners TEXT,  -- CSV of others with read/write.
  readers TEXT,  -- CSV of others with read. 'WORLD' in first spot means public.
  title TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (created_by) REFERENCES user (id),
  FOREIGN KEY (updated_by) REFERENCES user (id)
);
