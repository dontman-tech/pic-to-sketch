# pic-to-sketch
python program to turn an image into a pencil sketch

Viewed sketch.py
Edited sketch.py

I have written the complete code for the image-to-pencil-sketch GUI program into your active file `c:\Users\Miracle\Desktop\code\sketch.py`.

The program uses `tkinter` for the GUI, and relies on `opencv-python` (cv2) for the image processing and `Pillow` (PIL) for displaying the images in the Tkinter window. 

The image processing uses a popular approach to generate a pencil sketch:
1. Converting the image to grayscale
2. Inverting the grayscale image
3. Applying a Gaussian blur to the inverted image
4. Inverting the blurred image
5. Using a "Color Dodge" blend (via `cv2.divide`) to combine the grayscale image with the inverted blurred image.

### How to run it:
If you haven't already, you will need to install the required image processing libraries. You can do this by running the following command in your terminal:
```bash
pip install opencv-python Pillow
```

After that, just run the file:
```bash
cd c:\Users\Miracle\Desktop\code
python sketch.py
```

A window will open where you can click "Upload Image", view the generated sketch, and optionally click "Save Sketch" to save the result!
