
# frame_grid

Sometimes it is useful to have a table like view our our data frame
data. This is provided with the `frame_grid()` method. It takes
the same parameters as the `frame_object()` and `frame()` methods.

## Example

If I have a collection named "photos.ds" and a previously
defined frame name "captions-dates-locations" I can get that
as a 2D JSON array with the folllowing---

```
    c_name = 'photos.ds'
    f_name = 'capations-dates-locations'
    grid1 = dataset.frame_grid(c_name, f_name)
```

`frame_grid()` also includes the option to suppress a header row.


```
    grid2 = dataset.frame_grid(c_name, f_name, use_header_row = False)
```

Explore the differences from `grid1` and grid2`.

