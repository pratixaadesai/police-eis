DROP TABLE IF EXISTS staging.lookup_event_types; 
CREATE UNLOGGED TABLE staging.lookup_event_types (
	code                                                                  int,                --
	value                                                                 varchar,            --
	description                                                           varchar             --
);
