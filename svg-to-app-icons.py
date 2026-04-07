# Helper script to convert icons in svg to png
# Create a black and a white version
###################################################################
import io
import os

from PIL import Image
from cairosvg import svg2png

# Resoluties voor ICNS-bestanden
RESOLUTIONS = [16, 32, 64, 128, 256, 512, 1024]
WINDOWS_ICON_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]


def convert2png(source: str, destination: str, destination_white: str = None):
    os.makedirs(destination, exist_ok=True)
    if destination_white:
        os.makedirs(destination_white, exist_ok=True)

    for filename in os.listdir(source):
        if filename.endswith(".svg"):
            src_file = os.path.join(source, filename)
            dst_file_black = os.path.join(destination, filename.replace(".svg", ".png"))

            print(f"-> Convert {src_file} --> {dst_file_black} [black]")
            with open(src_file, "rb") as svg_file:
                svg2png(file_obj=svg_file, write_to=dst_file_black)
                png_data = svg2png(file_obj=svg_file)

            if destination_white:
                dst_file_white = os.path.join(destination_white, filename.replace(".svg", ".png"))
                print(f"-> Convert {src_file} --> {dst_file_white} [white]")
                with Image.open(io.BytesIO(png_data)) as img:
                    # Ensure the image is in RGBA mode
                    img = img.convert("RGBA")

                    # Invert the image colors (assuming the original is black on transparent)
                    # r, g, b, a = img.split()
                    # inverted_img = ImageOps.invert(Image.merge("RGB", (r, g, b)))
                    # inverted_img = Image.merge(
                    #     "RGBA",
                    #     (
                    #         inverted_img.getchannel(0),
                    #         inverted_img.getchannel(1),
                    #         inverted_img.getchannel(2),
                    #         a
                    #     )
                    # )
                    # inverted_img.save(dst_file_white)

                    # Convert black pixels to white, preserving transparency
                    data = img.getdata()
                    new_data = []
                    for item in data:
                        # Change all black (0,0,0) pixels to white (255,255,255)
                        if item[:3] == (0, 0, 0):
                            new_data.append((255, 255, 255, item[3]))
                        else:
                            new_data.append(item)
                    img.putdata(new_data)
                    img.save(dst_file_white)


def convert2icns(source: str, destination: str):
    os.makedirs(destination, exist_ok=True)

    for filename in os.listdir(source):
        if not filename.endswith(".svg"):
            continue

        src_file = os.path.join(source, filename)
        icon_file = filename.split(".")[0]  # remove file extension from filename

        icontemp_dir = os.path.join(destination, "icon.iconset")
        os.makedirs(icontemp_dir, exist_ok=True)

        for size in RESOLUTIONS:
            output_file = os.path.join(icontemp_dir, f"icon_{size}x{size}.png")
            print(f"-> Generate {src_file} --> {output_file}")
            svg2png(url=src_file, write_to=output_file, output_width=size, output_height=size)

        # Create ICNS file
        icns_file = f"{destination}/{icon_file}.icns"
        print(f"-> Create ICNS: {icns_file}")
        os.system(f"iconutil -c icns {icontemp_dir} -o {icns_file}")  # noqa: S605
        print(f"-> Remove temporary folder: {icontemp_dir}")
        os.system(f"rm -rf {icontemp_dir}")  # noqa: S605

        # Create Windows ICO file
        ico_file = f"{destination}/{icon_file}.ico"
        print(f"-> Create ICO: {ico_file}")
        png_data = svg2png(url=src_file)
        with Image.open(io.BytesIO(png_data)) as image:
            image = image.convert("RGBA")
            [image.resize(size) for size in WINDOWS_ICON_SIZES]
            image.save(ico_file, format='ICO', sizes=WINDOWS_ICON_SIZES)


if __name__ == "__main__":
    convert2png("assets_button_icons", "out_icons_black", "out_icons_white")
    convert2png("assets_app_icons", "out_app_icon")
    convert2icns("assets_app_icons", "out_app_icon")
