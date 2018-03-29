
# table generation

[RFC 4180](https://tools.ietf.org/html/rfc4180.html).
This test based on excel style.

## simple

~~~{#simple .shell-exec .csv-table header='true'}
nkf -Lw	<<"EOF"
Col1, Col2, Col3
1, 2, 3
10, 20, 30
EOF
~~~

## long cell

~~~{#not-quoted .shell-exec .csv-table header='true'}
nkf -Lw	<<"EOF"
col1,col2,col3
1,This is a cell.,2
2,This is another cell.,4
EOF
~~~

## quotes

~~~{#quoted .shell-exec .csv-table header='true'}
nkf -Lw	<<"EOF"
col1,col2,col3
5,"This is a cell, with comma.",6
7,"This is a cell
with newline.",8
EOF
~~~

