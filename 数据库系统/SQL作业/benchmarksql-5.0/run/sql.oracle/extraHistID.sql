-- ----
-- Extra Schema objects/definitions for history.hist_id in Oracle
-- ----

-- ----
--	This is an extra column not present in the TPC-C
--	specs. It is useful for replication systems like
--	Bucardo and Slony-I, which like to have a primary
--	key on a table. It is an auto-increment or serial
--	column type. The definition below is compatible
--	with Oracle 11g, using the sequence in a trigger.
-- ----
-- Adjust the sequence above the current max(hist_id)
alter sequence bmsql_hist_id_seq increment by 30000;
declare
    n integer\;
    i integer\;
    dummy integer\;
begin
    select max(hist_id) into n from bmsql_history\;
    i := 0\;
    while i <= n loop
	select bmsql_hist_id_seq.nextval into dummy from dual\;
	i := i + 30000\;
    end loop\;
end\;
;
alter sequence bmsql_hist_id_seq increment by 1;

-- Create a trigger that forces hist_id to be hist_id_seq.nextval
create trigger bmsql_history_before_insert
    before insert on bmsql_history
    for each row
    begin
	if :new.hist_id is null then
	    select bmsql_hist_id_seq.nextval into :new.hist_id from dual\;
	end if\;
    end\;
;

-- Add a primary key history(hist_id)
alter table bmsql_history add primary key (hist_id);
