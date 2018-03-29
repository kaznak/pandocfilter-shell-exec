
# shell code execution

## simple

~~~{#simple .shell-exec}
echo 'HELLO! SHELL!'
~~~

## piped

~~~{#piped .shell-exec}
echo 'HELLO! SHELL!'	|
tr 'A-Z' 'a-z'
~~~

## multiple

~~~{#multiple .shell-exec}
echo 'HELLO! SHELL!'	|
tr 'A-Z' 'a-z'
echo 'FROM PANDOC!'	|
tr 'A-Z' 'a-z'
~~~

## program designation

~~~{#prog .shell-exec prog="bc 		-ql "}
1+1
~~~
