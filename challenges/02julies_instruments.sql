-- get the names of all of the instruments played by 
select InstrumentName
from Musician m
JOIN MusicianInstrument mi ON mi.MusicianId = m.MusicianId
JOIN Instrument i on i.InstrumentId = mi.InstrumentId
WHERE MusicianName = 'Julie';