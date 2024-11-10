-- name: InsertAudio :one
INSERT INTO Audio (id, name, extension, mime_type, path)
VALUES ($1, $2, $3, $4, $5)
RETURNING id, name, extension, mime_type, path;

-- name: GetAudioById :one
SELECT id, name, extension, mime_type, path
FROM Audio
WHERE id = $1;

-- name: ListAudios :many
SELECT id, name, extension, mime_type, path
FROM Audio
ORDER BY name;

-- name: UpdateAudioPath :exec
UPDATE Audio
SET path = $2
WHERE id = $1;

-- name: DeleteAudio :exec
DELETE FROM Audio
WHERE id = $1;
