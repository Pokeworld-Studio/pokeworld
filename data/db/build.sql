CREATE TABLE IF NOT EXISTS server (
    GuildID integer PRIMARY KEY,
    Battles integer DEFAULT 0,
    Trades integer DEFAULT 0,
    Members integer DEFAULT 0
);