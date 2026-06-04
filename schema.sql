-- ============================================================
-- Stellar System V2 — SQLite Schema
-- All tables are created with IF NOT EXISTS so the schema
-- can be applied safely on every startup.
-- ============================================================

-- Guild-level key/value settings (extensible)
CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id    INTEGER NOT NULL,
    key         TEXT    NOT NULL,
    value       TEXT,
    PRIMARY KEY (guild_id, key)
);

-- Ticket metadata
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id        INTEGER NOT NULL,
    channel_id      INTEGER NOT NULL UNIQUE,
    user_id         INTEGER NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    closed_at       TEXT,
    status          TEXT    NOT NULL DEFAULT 'open'   -- open | closed | deleted
);

-- Per-user warnings
CREATE TABLE IF NOT EXISTS warnings (
    warn_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id        INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    moderator_id    INTEGER NOT NULL,
    reason          TEXT    NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Auto-roles assigned on member join
CREATE TABLE IF NOT EXISTS autoroles (
    guild_id    INTEGER NOT NULL,
    role_id     INTEGER NOT NULL,
    PRIMARY KEY (guild_id, role_id)
);

-- Log channel per guild
CREATE TABLE IF NOT EXISTS log_channels (
    guild_id    INTEGER PRIMARY KEY,
    channel_id  INTEGER NOT NULL
);

-- Welcome channel per guild
CREATE TABLE IF NOT EXISTS welcome_channels (
    guild_id    INTEGER PRIMARY KEY,
    channel_id  INTEGER NOT NULL
);
