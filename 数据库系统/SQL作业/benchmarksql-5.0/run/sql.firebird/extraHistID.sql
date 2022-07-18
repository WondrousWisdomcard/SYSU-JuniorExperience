-- ----
-- Extra Schema objects/definitions for history.hist_id in Firebird
-- ----

-- ----
--	This is an extra column not present in the TPC-C
--	specs. It is useful for replication systems like
--	Bucardo and Slony-I, which like to have a primary
--	key on a table. It is an auto-increment or serial
--	column type. The definition below is compatible
--	with Firebird, using the sequence in a trigger.
-- ----
-- Adjust the sequence above the current max(hist_id)
execute block 
as
    declare max_hist_id integer\;
    declare dummy integer\;
begin
    max_hist_id = (select max(hist_id) + 1 from bmsql_history)\;
    dummy = GEN_ID(bmsql_hist_id_seq, -GEN_ID(bmsql_hist_id_seq, 0))\;
    dummy = GEN_ID(bmsql_hist_id_seq, max_hist_id)\;
end;

-- Create a trigger that forces hist_id to be hist_id_seq.nextval
create trigger bmsql_hist_id_gen for bmsql_history
active before insert
as
begin
    if (new.hist_id is null) then
	new.hist_id = GEN_ID(bmsql_hist_id_seq, 1)\;
end;

-- Add a primary key history(hist_id)
-- Firebird lacks the capacity to declare an existing column NOT NULL.
-- In order to not impose overhead due to CHECK constraints or other
-- constructs, we leave the column nullable because the above trigger
-- makes sure it isn't (at least on insert, which is all we ever do).
create unique index bmsql_history_idx1 on bmsql_history (hist_id);
