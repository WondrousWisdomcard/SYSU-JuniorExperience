
alter table bmsql_warehouse drop constraint bmsql_warehouse_pkey;

alter table bmsql_district drop constraint bmsql_district_pkey;

alter table bmsql_customer drop constraint bmsql_customer_pkey;
drop index bmsql_customer_idx1;

-- history table has no primary key
-- commit;

alter table bmsql_oorder drop constraint bmsql_oorder_pkey;
drop index bmsql_oorder_idx1;

alter table bmsql_new_order drop constraint bmsql_new_order_pkey;

alter table bmsql_order_line drop constraint bmsql_order_line_pkey;

alter table bmsql_stock drop constraint bmsql_stock_pkey;

alter table bmsql_item drop constraint bmsql_item_pkey;
