# Senna Foods LMS — SAP delivery file checker

Bonus task for the Senna Foods Implementation Engineer Intern assignment.

The script reads the nightly SAP delivery file, groups the rows into deliveries, and prints each delivery's shop, number of items and total weight. Problem rows are flagged and put on hold instead of crashing the run.

## What it checks

- **Missing or bad weight**: the delivery is put on hold (delivery 0080001236).
- **Unknown shop**: the delivery is put on hold (shop 0000100999). The LMS is assumed to know every other shop in the file.
- **Bad quantity**: flagged if it's empty, zero or not a number.
- **Weight unit**: `KG` is kept, `G` is divided by 1000, and anything else is flagged.
- **Leading zeros**: spreadsheets drop them (`80001234`), so the script puts them back (`0080001234`) before matching.

It works with both comma-separated and tab-separated files.

## Run it

Python 3, no extra libraries:

```
python3 check_deliveries.py SAP_delivery_sample.csv
```

## Output

```
DELIVERY    SHOP        SHOP NAME                 ITEMS  WEIGHT KG  STATUS
--------------------------------------------------------------------------------
0080001234  0000100245  Sri Balaji Stores             2       27.6  OK
0080001235  0000100317  Ganesh Mart                   2       17.2  OK
0080001236  0000100402  New Fresh Mart                1          ?  ON HOLD
              ! line 6, item 000010: missing or bad weight
0080001237  0000100999  Om Provisions                 1        5.6  ON HOLD
              ! line 7: unknown shop 0000100999
0080001238  0000100118  Lakshmi Traders               3       25.2  OK
0080001239  0000100533  Annapoorna Supermarket        2       98.5  OK
0080001240  0000100274  Royal Kirana                  1       51.0  OK
0080001241  0000100650  Daily Needs Store             2       12.0  OK
0080001242  0000100381  Venkateshwara Provisions      2       25.0  OK
0080001243  0000100712  Green Basket                  2       51.6  OK
0080001244  0000100159  Sai Ram Stores                1       12.0  OK
0080001245  0000100826  City Fresh Mart               2       13.6  OK
--------------------------------------------------------------------------------
21 rows, 12 deliveries: 10 ready to plan, 2 on hold
```
