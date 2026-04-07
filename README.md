# svg-to-app-icons

Convert SVG icon files to app icons in png and ico format.

1. Put your application icon(s) in svg format into the **assets_app_icons** folder
2. Put your button icon(s) in svg format into the **assets_button_icons** folder
3. Run the script
4. Your application icon(s) will be available in the **out_app_icon** folder
5. Your button icon(s) will be available in the **out_icons_black** and **out_icons_white** folder


## Running the script

I recommend using UV ...

```shell
$ uv sync
$ uv run svg-to-app-icons.py
```
