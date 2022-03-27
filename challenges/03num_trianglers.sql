-- find the number of musicians that play Triangle. 
-- Name your count column 'NumberofTrianglers'
SELECT COUNT(*) NumberofTrianglers
FROM Musician m 
JOIN MusicianInstrument mi on m.MusicianId = mi.MusicianId
JOIN Instrument i on i.InstrumentId = mi.InstrumentId
WHERE InstrumentName = 'Triangle';