-- ----
-- Extra Schema objects/definitions for history.hist_id in PostgreSQL
-- ----

-- ----
--      This is an extra column not present in the TPC-C
--      specs. It is useful for replication systems like
--      Bucardo and Slony-I, which like to have a primary
--      key on a table. It is an auto-increment or serial
--      column type. The definition below is compatible
--      with Oracle 11g, using a sequence and a trigger.
-- ----
-- Adjust the sequence above the current max(hist_id)
select setval('bmsql_hist_id_seq', (select max(hist_id) from bmsql_history));

-- Make nextval(seq) the default value of the hist_id column.
alter table bmsql_history 
    alter column hist_id set default nextval('bmsql_hist_id_seq');

-- Add a primary key history(hist_id)
alter table bmsql_history add primary key (hist_id);
