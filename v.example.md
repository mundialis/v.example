## DESCRIPTION

*v.example* is an example for a GRASS GIS addon. Here comes a short
description of the module.

New paragraph for more detailed description.

## NOTES

Rather technical notes are here.

Description of the algorithm or method

Hints for usage, e.g. for large maps or a large number of input
arguments.

## EXAMPLE

### Create grid for current region with grid box size of 1000 x 1000

```sh
v.example output=tiles box=1000,1000
```

### Extract tiles only for a given polygon "poly_aoi"

```sh
v.select ainput=tiles atype=area binput=poly_aoi btype=area operator=overlap output=tiles_aoi
```

Image with the result

[![image-alt](v_example.png)](v_example.png)  
*Figure: Vector map .... something.*

## SEE ALSO

*[v.mkgrid](v.mkgrid.md), [g.region](g.region.md)*

## AUTHORS

Name, [mundialis](https://www.mundialis.de/)
