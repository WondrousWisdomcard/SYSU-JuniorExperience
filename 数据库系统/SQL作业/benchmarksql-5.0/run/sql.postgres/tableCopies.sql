
copy bmsql_config
  (cfg_name, cfg_value)
  from '/tmp/csv/config.csv' WITH CSV;

copy bmsql_warehouse
  (w_id, w_ytd, w_tax, w_name, w_street_1, w_street_2, w_city, w_state, w_zip)
  from '/tmp/csv/warehouse.csv' WITH CSV;

copy bmsql_item
  (i_id, i_name, i_price, i_data, i_im_id)
  from '/tmp/csv/item.csv' WITH CSV;

copy bmsql_stock
  (s_i_id, s_w_id, s_quantity, s_ytd, s_order_cnt, s_remote_cnt, s_data,
   s_dist_01, s_dist_02, s_dist_03, s_dist_04, s_dist_05,
   s_dist_06, s_dist_07, s_dist_08, s_dist_09, s_dist_10)
  from '/tmp/csv/stock.csv' WITH CSV;

copy bmsql_district
  (d_id, d_w_id, d_ytd, d_tax, d_next_o_id, d_name, d_street_1,
   d_street_2, d_city, d_state, d_zip)
  from '/tmp/csv/district.csv' WITH CSV;

copy bmsql_customer
  (c_id, c_d_id, c_w_id, c_discount, c_credit, c_last, c_first, c_credit_lim,
   c_balance, c_ytd_payment, c_payment_cnt, c_delivery_cnt, c_street_1,
   c_street_2, c_city, c_state, c_zip, c_phone, c_since, c_middle, c_data)
  from '/tmp/csv/customer.csv' WITH CSV;

copy bmsql_history
  (hist_id, h_c_id, h_c_d_id, h_c_w_id, h_d_id, h_w_id, h_date, h_amount, h_data)
  from '/tmp/csv/cust-hist.csv' WITH CSV;

copy bmsql_oorder
  (o_id, o_w_id, o_d_id, o_c_id, o_carrier_id, o_ol_cnt, o_all_local, o_entry_d)
  from '/tmp/csv/order.csv' WITH CSV NULL AS 'NULL';

copy bmsql_order_line
  (ol_w_id, ol_d_id, ol_o_id, ol_number, ol_i_id, ol_delivery_d,
   ol_amount, ol_supply_w_id, ol_quantity, ol_dist_info)
  from '/tmp/csv/order-line.csv' WITH CSV NULL AS 'NULL';

copy bmsql_new_order
  (no_w_id, no_d_id, no_o_id)
  from '/tmp/csv/new-order.csv' WITH CSV;
