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

-- 7. Pilota ha totalizzato più punti di un altro nella stessa gara
-- In questo grafo, ogni arco va da un pilota che ha ottenuto più punti
-- di un altro nella stessa gara (results.points). Il peso rappresenta
-- quante volte questo "superamento in punti" è avvenuto tra i due piloti.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.points > r2.points
  AND r1.driverId <> r2.driverId
GROUP BY r1.driverId, r2.driverId;

-- 8. Confronto tra costruttori sui giri completati in una stessa gara
-- Per ogni coppia di team in ogni gara, se uno ha completato più giri,
-- allora "batte" l'altro. Il peso rappresenta il numero di gare in cui
-- questo confronto è stato verificato.
SELECT r1.constructorId AS id1, r2.constructorId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.laps > r2.laps
  AND r1.constructorId <> r2.constructorId
GROUP BY r1.constructorId, r2.constructorId;

-- 9. Confronto sulle vittorie nelle classifiche piloti (driverstandings)
-- In ogni gara, se un pilota ha più vittorie registrate (driverstandings.wins)
-- rispetto a un altro, si crea un arco da lui verso l’altro. Il peso è quante
-- volte ha avuto più vittorie rispetto a quell’avversario nella stessa gara.
SELECT ds1.driverId AS id1, ds2.driverId AS id2, COUNT(*) AS peso
FROM driverstandings ds1
JOIN driverstandings ds2 ON ds1.raceId = ds2.raceId
WHERE ds1.wins > ds2.wins
  AND ds1.driverId <> ds2.driverId
GROUP BY ds1.driverId, ds2.driverId;

-- 10. Confronto tra costruttori sui punti finali nelle classifiche (constructorstandings)
-- A ogni gara, se un costruttore ha ottenuto più punti in classifica rispetto a un altro,
-- allora crea un arco orientato verso il secondo. Il peso indica quante volte ciò è successo.
SELECT cs1.constructorId AS id1, cs2.constructorId AS id2, COUNT(*) AS peso
FROM constructorstandings cs1
JOIN constructorstandings cs2 ON cs1.raceId = cs2.raceId
WHERE cs1.points > cs2.points
  AND cs1.constructorId <> cs2.constructorId
GROUP BY cs1.constructorId, cs2.constructorId;

-- 11. Confronto tra piloti sulla differenza tra griglia di partenza e arrivo
-- Calcola il miglioramento: (grid - position). Un valore più alto indica che il pilota
-- ha guadagnato più posizioni. Si crea un arco tra i due con peso = volte in cui
-- uno ha guadagnato più posizioni dell’altro nella stessa gara.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE (r1.grid - r1.position) > (r2.grid - r2.position)
  AND r1.driverId <> r2.driverId
  AND r1.grid IS NOT NULL AND r1.position IS NOT NULL
  AND r2.grid IS NOT NULL AND r2.position IS NOT NULL
GROUP BY r1.driverId, r2.driverId;

-- 12. Confronto tra piloti sul giro più veloce nella stessa gara
-- Se un pilota ha un tempo migliore in “fastestLap” rispetto a un altro nella stessa gara,
-- si crea un arco da lui verso l’altro. Il peso rappresenta il numero di confronti vinti.
SELECT r1.driverId AS id1, r2.driverId AS id2, COUNT(*) AS peso
FROM results r1
JOIN results r2 ON r1.raceId = r2.raceId
WHERE r1.fastestLap < r2.fastestLap
  AND r1.fastestLap IS NOT NULL AND r2.fastestLap IS NOT NULL
  AND r1.driverId <> r2.driverId
GROUP BY r1.driverId, r2.driverId;

