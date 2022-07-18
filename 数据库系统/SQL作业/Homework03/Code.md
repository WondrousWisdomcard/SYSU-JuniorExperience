# Code:  1

```
DROP FUNCTION get_student_phone();
CREATE FUNCTION get_student_phone() RETURNS bigint AS $$
DECLARE
	head1 bigint := 13700000000;
	head2 bigint := 15900000000;
	s_phone bigint := 0;
	ten int := 1;
BEGIN
	IF RANDOM() > 0.5 THEN
		s_phone := head1;
	ELSE
		s_phone := head2;
	END IF;
	
	FOR i IN 1..8 LOOP
		s_phone := s_phone + ten * FLOOR(RANDOM() * 10);
		ten := ten * 10;
	END LOOP;
	
	RETURN s_phone;
END;
$$ LANGUAGE plpgsql;

select get_student_phone();
```

# Code:  2

```
DROP FUNCTION get_student_date();
CREATE FUNCTION get_student_date() RETURNS date AS $$
DECLARE
	s_date date;
	s_day int = 0;
BEGIN
	IF RANDOM() < 0.6 THEN
		s_date := make_date(2021, 1, 1); 
		s_day := FLOOR(RANDOM() * 364);
		s_date := s_date + s_day;
	ELSE
		s_date := make_date(2020, 1, 1); 
		s_day := FLOOR(RANDOM() * 365);
		s_date := s_date + s_day;
	END IF;
	RETURN s_date;
END;
$$ LANGUAGE plpgsql;

select get_student_date();
```

# Code:  3

```
DROP FUNCTION create_student_table();		
CREATE FUNCTION create_student_table(OUT student_id int, OUT phone_num bigint, OUT enrollment_date date) RETURNS SETOF record AS $$
DECLARE
	student_table record;
BEGIN
	FOR i IN 1..15 LOOP
		student_id := i;
		phone_num := get_student_phone();
		enrollment_date = get_student_date();		
		RETURN NEXT;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

select * from create_student_table();
```


# Code:  4

```
SELECT *
FROM create_student_table()
WHERE enrollment_date > date '2020-07-01';
```





