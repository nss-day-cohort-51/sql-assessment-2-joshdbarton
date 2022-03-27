BEGIN TRANSACTION;
CREATE TABLE "Musician" (
	"MusicianId"	INTEGER NOT NULL,
	"MusicianName"	NVARCHAR(55) NOT NULL,
	PRIMARY KEY("MusicianId" AUTOINCREMENT)
);
CREATE TABLE "Difficulty" (
	"DifficultyId"	INTEGER NOT NULL,
	"Label"	NVARCHAR(25) NOT NULL,
	PRIMARY KEY("DifficultyId" AUTOINCREMENT)
);
CREATE TABLE "Instrument" (
	"InstrumentId"	INTEGER NOT NULL,
	"InstrumentName"	NVARCHAR(255) NOT NULL,
	"DifficultyId"	INTEGER NOT NULL,
	CONSTRAINT "FK_Instrument_Difficulty" FOREIGN KEY("DifficultyId") REFERENCES "Difficulty"("DifficultyId"),
	PRIMARY KEY("InstrumentId" AUTOINCREMENT)
);
CREATE TABLE "MusicianInstrument" (
	"MusicianInstrumentId"	INTEGER NOT NULL,
	"MusicianId"	INTEGER NOT NULL,
	"InstrumentId"	INTEGER NOT NULL,
	CONSTRAINT "FK_MusicianInstrument_Musician" FOREIGN KEY("MusicianId") REFERENCES "Musician"("MusicianId"),
	CONSTRAINT "FK_MusicianInstrument_Instrument" FOREIGN KEY("InstrumentId") REFERENCES "Instrument"("InstrumentId"),
	PRIMARY KEY("MusicianInstrumentId" AUTOINCREMENT)
);
INSERT INTO "Musician" ("MusicianId","MusicianName") VALUES (1,'Sun Ra'),
 (2,'Weird Guy Down the Street'),
 (3,'Julie');
INSERT INTO "Difficulty" ("DifficultyId","Label") VALUES (1,'Easy'),
 (2,'Hard');
INSERT INTO "Instrument" ("InstrumentId","InstrumentName","DifficultyId") VALUES (1,'Recorder',1),
 (2,'Triangle',1),
 (3,'Trumpet',2),
 (4,'Upright Bass',2),
 (5,'Fiddle',2);
INSERT INTO "MusicianInstrument" ("MusicianInstrumentId","MusicianId","InstrumentId") VALUES (1,1,3),
 (2,2,2),
 (3,3,2),
 (4,3,4);
COMMIT;
