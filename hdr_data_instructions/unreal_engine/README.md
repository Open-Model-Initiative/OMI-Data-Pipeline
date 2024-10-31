# Using Unreal Engine to Create HDR Data

Unreal Engine can be used to create HDR images of anything you can setup or render in Unreal Engine.

This should be focused on Unreal FAB marketplace items which have "Allows usage with AI" set to Yes at the time of adding to your library, or items you have ownership of and would like to create open HDR screenshots for.

To take HDR screenshots in Unreal Engine, move the editor camera to the desired location, press tilda (~) to open the command window, then run `HighResShot 1 filename="screenshot_00001.exr"` incrementing the number for each subsequent screenshot. You may need to enable HDR in the editor settings for this to work.

This process was tested with Unreal Engine 5.4.4.

Future contributions to better automate this process would be appreciated.
