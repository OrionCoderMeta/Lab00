-- 1. Pilota batte un altro pilota (position più bassa), filtrato per anno
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.position IS NOT NULL
  AND r2.position IS NOT NULL
  AND r1.position < r2.position
  AND r.year = 1951
GROUP BY r1.driverId, r2.driverId;

-- 2. Confronto tra team: un team batte un altro se un suo pilota arriva prima (position più bassa)
SELECT r1.constructorId AS id1, r2.constructorId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.position IS NOT NULL
  AND r2.position IS NOT NULL
  AND r1.constructorId <> r2.constructorId
  AND r1.position < r2.position
  AND r.year = 1951
GROUP BY r1.constructorId, r2.constructorId;

-- 3. Confronto tra piloti nelle qualifiche: chi parte davanti batte chi parte dietro
SELECT q1.driverId AS id1, q2.driverId AS id2, COUNT(*) AS peso
FROM qualifying q1, qualifying q2, races r
WHERE q1.raceId = q2.raceId
  AND q1.raceId = r.raceId
  AND q1.position IS NOT NULL
  AND q2.position IS NOT NULL
  AND q1.position < q2.position
  AND r.year = 1951
GROUP BY q1.driverId, q2.driverId;

-- 4. Un pilota batte un altro compagno di squadra (stesso costruttore) nella stessa gara
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.position IS NOT NULL
  AND r2.position IS NOT NULL
  AND r1.constructorId = r2.constructorId
  AND r1.driverId <> r2.driverId
  AND r1.position < r2.position
  AND r.year = 1951
GROUP BY r1.driverId, r2.driverId;

-- 5. Pilota che ha fatto pit stop più veloce (in millisecondi) nello stesso giro della stessa gara
SELECT p1.driverId AS id1, p2.driverId AS id2, COUNT(*) AS peso
FROM pitstops p1, pitstops p2, races r
WHERE p1.raceId = p2.raceId
  AND p1.raceId = r.raceId
  AND p1.lap = p2.lap
  AND p1.milliseconds IS NOT NULL
  AND p2.milliseconds IS NOT NULL
  AND p1.milliseconds < p2.milliseconds
  AND r.year = 1951
GROUP BY p1.driverId, p2.driverId;

-- 6. Confronta ogni giro tra due piloti nella stessa gara. Se il primo è più veloce, vince il giro
-- Filtro per anno (modifica il valore in AND r.year = 1951)
SELECT l1.driverId AS id1, l2.driverId AS id2, COUNT(*) AS peso
FROM laptimes l1, laptimes l2, races r
WHERE l1.raceId = l2.raceId
  AND l1.lap = l2.lap
  AND l1.raceId = r.raceId
  AND l1.milliseconds < l2.milliseconds
  AND r.year = 1951
GROUP BY l1.driverId, l2.driverId;

-- 7. Pilota ha totalizzato più punti di un altro nella stessa gara
-- In questo grafo, ogni arco va da un pilota che ha ottenuto più punti
-- di un altro nella stessa gara (results.points). Il peso rappresenta
-- quante volte questo "superamento in punti" è avvenuto tra i due piloti.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.points > r2.points
  AND r1.driverId <> r2.driverId
  AND r.year = 1951
GROUP BY r1.driverId, r2.driverId;

-- 8. Confronto tra costruttori sui giri completati in una stessa gara
-- Per ogni coppia di team in ogni gara, se uno ha completato più giri,
-- allora "batte" l'altro. Il peso rappresenta il numero di gare in cui
-- questo confronto è stato verificato.
SELECT r1.constructorId AS id1, r2.constructorId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.laps > r2.laps
  AND r1.constructorId <> r2.constructorId
  AND r.year = 1951
GROUP BY r1.constructorId, r2.constructorId;

-- 9. Confronto sulle vittorie nelle classifiche piloti (driverstandings)
-- Arco da un pilota verso un altro se ha più vittorie (driverstandings.wins) nella stessa gara
-- Il peso è quante volte è successo, considerando solo le gare dell’anno indicato
SELECT ds1.driverId AS id1, ds2.driverId AS id2, COUNT(*) AS peso
FROM driverstandings ds1, driverstandings ds2, races r
WHERE ds1.raceId = ds2.raceId
  AND ds1.raceId = r.raceId
  AND ds1.wins > ds2.wins
  AND ds1.driverId <> ds2.driverId
  AND r.year = 1951
GROUP BY ds1.driverId, ds2.driverId;

-- 10. Confronto tra costruttori sui punti finali nelle classifiche (constructorstandings)
-- Se un costruttore ha ottenuto più punti in classifica rispetto a un altro nella stessa gara,
-- allora crea un arco da lui verso l’altro. Il peso indica quante volte è successo nell’anno richiesto.
SELECT cs1.constructorId AS id1, cs2.constructorId AS id2, COUNT(*) AS peso
FROM constructorstandings cs1, constructorstandings cs2, races r
WHERE cs1.raceId = cs2.raceId
  AND cs1.raceId = r.raceId
  AND cs1.points > cs2.points
  AND cs1.constructorId <> cs2.constructorId
  AND r.year = 1951
GROUP BY cs1.constructorId, cs2.constructorId;

-- 11. Confronto tra piloti sulla differenza tra griglia di partenza e arrivo
-- Si calcola il miglioramento (grid - position): se maggiore per un pilota rispetto a un altro
-- nella stessa gara, si crea un arco. Il peso rappresenta il numero di volte che è successo nell’anno scelto.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND (r1.grid - r1.position) > (r2.grid - r2.position)
  AND r1.driverId <> r2.driverId
  AND r1.grid IS NOT NULL AND r1.position IS NOT NULL
  AND r2.grid IS NOT NULL AND r2.position IS NOT NULL
  AND r.year = 1951
GROUP BY r1.driverId, r2.driverId;

-- 12. Confronto tra piloti sul giro più veloce nella stessa gara
-- Se un pilota ha un tempo migliore (fastestLap) rispetto a un altro nella stessa gara,
-- si crea un arco da lui verso l’altro. Il peso rappresenta il numero di confronti vinti nell’anno specificato.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1, results r2, races r
WHERE r1.raceId = r2.raceId
  AND r1.raceId = r.raceId
  AND r1.fastestLap IS NOT NULL AND r2.fastestLap IS NOT NULL
  AND r1.fastestLap < r2.fastestLap
  AND r1.driverId <> r2.driverId
  AND r.year = 1951
GROUP BY r1.driverId, r2.driverId;

