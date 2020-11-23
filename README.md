# StreakImage

Simply feed the StreakImage class the path to an .img-file to get a python object.
The actual data is stored in a [Pandas Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html).

All parameters of the original image can be accessed as demonstrated below:

```
import StreakImage
image = StreakImage(path_to_img_file)
print(image.parameters.Acquisition.ExposureTime)
```

Output:

```
1001 ms
```

### Adding new correction files

Over time the included correction files might not work as good anymore.
New camera correction files can be placed in streakimage/correction_data/.
You can find a tutorial on how to create new correction files from an image of a white light in the [tutorial series on the evaluation of streak camera images](https://github.com/nicohofdtz/streak-eval-tutorial) (Tut 02).
The way StreakImage deals with the correction files makes it possible to have multiple sets of correction files in the same folder. Since a certain set of correction matrices will be valid for a certain time span, it is useful to use the date of its creation as the prefix to the files. The rest of the filename has to follow the pattern "*timerange*\_correction\_*width*x*height*".
An exemplary file name with file extension is "202004_ST1_correction_640x512.npy".
The config file (streakimage.ini) contains a section "Cam-Correction-Prefix" to which StreakImage refers to find the appropriate correction file.
The key to a prefix is the date range (from-to in YYYYMMDD notation) for which it is valid.
StreakImage finds the correct prefix by going through the list from top to bottom and checking if *from* <= *date* <= *to*, where *date* is the date of the streak image.
If no prefix fits the condition the default prefix is used.
Since it's the end date of the validity of a set of correction files is unclear when they're added, the end date of the newest prefix can be set to a date in far future.

### Licence
This project is not yet licenced but licencing it under the terms of the GNU or MIT licence is planned. 
