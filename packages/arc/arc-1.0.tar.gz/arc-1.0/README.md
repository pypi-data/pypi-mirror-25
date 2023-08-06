# arc

A small python library for calculating the length of an arc.

## How to use

```python
from arc import arc_length

radius_of_circle = 12 # 12"
degree_of_arc = 60 # 60°

length_of_arc = arc_length(
    degree_of_arc,
    radius_of_circle
)
print length_of_arc # 12.56637061435917

circumference_of_circle = 24

length_of_arc = arc_length(
    degree_of_arc,
    circumference=circumference_of_circle
)
print length_of_arc # 12.56637061435917
```
