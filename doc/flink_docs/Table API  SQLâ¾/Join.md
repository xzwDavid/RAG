# Join


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Join#


## Description#


JOIN is used to combine rows from two relations based on join condition.

`JOIN`

## Syntax#


Hive Dialect supports the following syntax for joining tables:


```
join_table:
    table_reference [ INNER ] JOIN table_factor [ join_condition ]
  | table_reference { LEFT | RIGHT | FULL } [ OUTER ] JOIN table_reference join_condition
  | table_reference LEFT SEMI JOIN table_reference [ ON expression ] 
  | table_reference CROSS JOIN table_reference [ join_condition ]
 
table_reference:
    table_factor
  | join_table
 
table_factor:
    tbl_name [ alias ]
  | table_subquery alias
  | ( table_references )
 
join_condition:
    { ON expression | USING ( colName [, ...] ) }

```

`join_table:
    table_reference [ INNER ] JOIN table_factor [ join_condition ]
  | table_reference { LEFT | RIGHT | FULL } [ OUTER ] JOIN table_reference join_condition
  | table_reference LEFT SEMI JOIN table_reference [ ON expression ] 
  | table_reference CROSS JOIN table_reference [ join_condition ]
 
table_reference:
    table_factor
  | join_table
 
table_factor:
    tbl_name [ alias ]
  | table_subquery alias
  | ( table_references )
 
join_condition:
    { ON expression | USING ( colName [, ...] ) }
`

## JOIN Type#


### INNER JOIN#


INNER JOIN returns the rows matched in both join sides. INNER JOIN is the default join type.

`INNER JOIN`
`INNER JOIN`

### LEFT JOIN#


LEFT JOIN returns all the rows from the left join side and the matched values from the right join side. It will concat the values from both sides.
If there’s no match in right join side, it will append NULL value. LEFT JOIN is equivalent to LEFT OUTER JOIN.

`LEFT JOIN`
`NULL`
`LEFT JOIN`
`LEFT OUTER JOIN`

### RIGHT JOIN#


RIGHT JOIN returns all the rows from the right join side and the matched values from the left join side. It will concat the values from both sides.
If there’s no match in left join side, it will append NULL value. RIGHT JOIN is equivalent to RIGHT OUTER JOIN.

`RIGHT JOIN`
`NULL`
`RIGHT JOIN`
`RIGHT OUTER JOIN`

### FULL JOIN#


FULL JOIN returns all the rows from both join sides. It will concat the values from both sides.
If there’s one side does not match the row, it will append NULL value. FULL JOIN is equivalent to FULL OUTER JOIN.

`FULL JOIN`
`NULL`
`FULL JOIN`
`FULL OUTER JOIN`

### LEFT SEMI JOIN#


LEFT SMEI JOIN returns the rows from the left join side that have matching in right join side. It won’t concat the values from the right side.

`LEFT SMEI JOIN`

### CROSS JOIN#


CROSS JOIN returns the Cartesian product of two join sides.

`CROSS JOIN`

## Examples#


```
-- INNER JOIN
SELECT t1.x FROM t1 INNER JOIN t2 USING (x);
SELECT t1.x FROM t1 INNER JOIN t2 ON t1.x = t2.x;

-- LEFT JOIN
SELECT t1.x FROM t1 LEFT JOIN t2 USING (x);
SELECT t1.x FROM t1 LEFT OUTER JOIN t2 ON t1.x = t2.x;

-- RIGHT JOIN
SELECT t1.x FROM t1 RIGHT JOIN t2 USING (x);
SELECT t1.x FROM t1 RIGHT OUTER JOIN t2 ON t1.x = t2.x;

-- FULL JOIN
SELECT t1.x FROM t1 FULL JOIN t2 USING (x);
SELECT t1.x FROM t1 FULL OUTER JOIN t2 ON t1.x = t2.x;

-- LEFT SEMI JOIN
SELECT t1.x FROM t1 LEFT SEMI JOIN t2 ON t1.x = t2.x;

-- CROSS JOIN
SELECT t1.x FROM t1 CROSS JOIN t2 USING (x);

```

`-- INNER JOIN
SELECT t1.x FROM t1 INNER JOIN t2 USING (x);
SELECT t1.x FROM t1 INNER JOIN t2 ON t1.x = t2.x;

-- LEFT JOIN
SELECT t1.x FROM t1 LEFT JOIN t2 USING (x);
SELECT t1.x FROM t1 LEFT OUTER JOIN t2 ON t1.x = t2.x;

-- RIGHT JOIN
SELECT t1.x FROM t1 RIGHT JOIN t2 USING (x);
SELECT t1.x FROM t1 RIGHT OUTER JOIN t2 ON t1.x = t2.x;

-- FULL JOIN
SELECT t1.x FROM t1 FULL JOIN t2 USING (x);
SELECT t1.x FROM t1 FULL OUTER JOIN t2 ON t1.x = t2.x;

-- LEFT SEMI JOIN
SELECT t1.x FROM t1 LEFT SEMI JOIN t2 ON t1.x = t2.x;

-- CROSS JOIN
SELECT t1.x FROM t1 CROSS JOIN t2 USING (x);
`