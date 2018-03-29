
# image generation

## simple

~~~{#simple .shell-exec .image}
echo "This code MUST pandoc-ed in same directory"	>&2
id=simple
img=./img/$id.png
mkdir -p $(dirname $img)
dot -Tpng -o $img <<"EOF"
graph {
    a -- b;
    b -- c;
    a -- c;
    d -- c;
    e -- c;
    e -- a;
  }
EOF
echo $img
~~~

## attrs

~~~{#attrs .shell-exec .image style='width:100vw' alt='alt str' title='title str'}
cat	<<EOF	>&2
This code MUST pandoc-ed in same directory.
use style attribute to write styles like below.
{#attrs .shell-exec .image style='width:100vw' alt='alt str' title='title str'}

below description does not work correctory.
{#attrs .shell-exec .image width='100vw' alt='alt str' title='title str'}
pandoc ommits width="100vw" attribute.
!!TODO!! report this bug to pandoc community.
EOF

id=attrs
img=./img/$id.png
mkdir -p $(dirname $img)
dot -Tpng -o $img <<"EOF"
graph {
    a -- b;
    b -- c;
    a -- c;
    d -- c;
    e -- c;
    e -- a;
  }
EOF
echo $img
~~~
