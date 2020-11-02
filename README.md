#StreakImage
Simply feed the StreakImage class the path to an .img-file to get a python object.
The actual data is stored in a [Pandas Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html).
All parameteres of the original image can be accessed as demonstrated below:

```
import StreakImage
image = StreakImage(path_to_img_file)
print(image.parameters.Acquisition.ExposureTime)
```

Output:

```
1001 ms
```
