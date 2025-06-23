-- 1. Pilota batte un altro pilota (position più bassa)
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.position IS NOT NULL AND r2.position IS NOT NULL
  AND r1.position < r2.position
GROUP BY r1.driverId, r2.driverId;


-- 2. Stesso principio di sopra, ma lo applichiamo ai team. Se un costruttore ha un pilota che arriva prima di un pilota dell'altro team, vince.
-- peso è quante volte è successo
SELECT r1.constructorId AS id1, r2.constructorId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.position IS NOT NULL AND r2.position IS NOT NULL
  AND r1.constructorId <> r2.constructorId
  AND r1.position < r2.position
GROUP BY r1.constructorId, r2.constructorId;

-- 3. Vale come il primo, ma usa la tabella qualifying. Il campo position indica la griglia di partenza
SELECT q1.driverId AS id1, q2.driverId AS id2, COUNT(*) AS peso
FROM qualifying q1
JOIN qualifying q2 ON q1.raceId = q2.raceId
WHERE q1.position IS NOT NULL AND q2.position IS NOT NULL
  AND q1.position < q2.position
GROUP BY q1.driverId, q2.driverId

-- 4. Pilota batte un altro, ma solo se dello stesso costruttore
-- Potrebbe servire se ti chiedono: "Quante volte un pilota ha battuto il suo compagno di squadra".
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.position IS NOT NULL AND r2.position IS NOT NULL
  AND r1.constructorId = r2.constructorId
  AND r1.driverId <> r2.driverId
  AND r1.position < r2.position
GROUP BY r1.driverId, r2.driverId

-- 5. Per ogni giro della stessa gara, confronta chi ha fatto il pit stop prima (in millisecondi).
SELECT p1.driverId AS id1, p2.driverId AS id2, COUNT(*) AS peso
FROM pitstops p1
JOIN pitstops p2 ON p1.raceId = p2.raceId AND p1.lap = p2.lap
WHERE p1.milliseconds IS NOT NULL AND p2.milliseconds IS NOT NULL
  AND p1.milliseconds < p2.milliseconds
GROUP BY p1.driverId, p2.driverId

-- 6. Confronta ogni giro tra due piloti nella stessa gara. Se l1 è più veloce di l2, allora ha vinto quel giro.
SELECT l1.driverId AS id1, l2.driverId AS id2, COUNT(*) AS peso
FROM laptimes l1
JOIN laptimes l2 ON l1.raceId = l2.raceId AND l1.lap = l2.lap
WHERE l1.milliseconds < l2.milliseconds
GROUP BY l1.driverId, l2.driverId

