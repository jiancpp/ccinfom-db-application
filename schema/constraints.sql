-- ==========================================================
--  This SQL Script is for adding FOREIGN KEYS
-- ==========================================================

USE dbApp;

--
-- Constraints for `events`
--
ALTER TABLE events
ADD CONSTRAINT fk_events_artist
    FOREIGN KEY (`artist_id`) REFERENCES artists(`id`),
    ON DELETE CASCADE ON UPDATE CASCADE
ADD CONSTRAINT fk_events_fanclub
    FOREIGN KEY (`fanclub_id`) REFERENCES fanclubs(`id`),
    ON DELETE SET NULL ON UPDATE CASCADE
ADD CONSTRAINT fk_events_venue
    FOREIGN KEY (`venue_id`) REFERENCES venues(`id`),
    ON DELETE CASCADE ON UPDATE CASCADE
ADD CONSTRAINT chk_event_host_xor
CHECK (
    (artist_id IS NOT NULL AND fanclub_id IS NULL)
 OR (artist_id IS NULL AND fanclub_id IS NOT NULL)
);


