How to Train a YOLOv8 Model for CNTS
Since we need to detect Indian Currency (specifically ₹500 notes), and we don't have a pre-trained model, you will need to create one. This is known as "Training a Custom Object Detector".

Phase 1: Data Collection
We need 50-100 images of the note in different angles, lighting, and backgrounds to get a decent result.

Run the Helper Tool: I have created a script to help you take photos using your webcam.
python tools/collect_data.py
Capture Images:
Hold a ₹500 note in front of the camera.
Press [Spacebar] to save an image.
Move the note around:
Front side
Back side
Folded / crumpled
Different distances
Different lighting (if possible)
Aim for at least 50 images.
Check Images: The images are saved in datasets/raw_images.
Phase 2: Annotation (Labeling)
The computer needs to know what in the image is the note.

Use Roboflow (Recommended for ease):

Go to roboflow.com (free account).
Create a new project (Object Detection).
Upload your images from datasets/raw_images.
Use their annotation tool to draw a box around the ₹500 note in every image.
Class Name: Use 500 as the class name.
Generate a dataset version.
Export: Choose YOLOv8 format. It will give you a download code or zip.
Alternative: Manual Local Annotation:

Install labelImg: pip install labelImg
Run labelImg.
Open your raw_images folder.
Draw boxes and save.
You will need to organize folders manually into train/images, train/labels, val/images, etc. (Roboflow does this automatically).
Phase 3: Training
Once you have the dataset (folder structure with data.yaml), you can train.

Setup Dataset: If you verified/downloaded a dataset, place it in datasets/cnts_data. Ensure datasets/cnts_data/data.yaml exists.

Run Training Command: Run this in your terminal:

yolo detect train data=datasets/cnts_data/data.yaml model=yolov8n.pt epochs=50 imgsz=640
Note: If you have a GPU, this takes ~5 mins. On CPU, it might take 30-60 mins.

Result: After training finishes, it will say "Results saved to runs/detect/train...". Find the file: runs/detect/train/weights/best.pt.

Phase 4: Integration
Copy Model: Copy best.pt to your project's models/ folder.
copy runs\detect\train\weights\best.pt models\best.pt
Run Application:
python src/main.py
The application will now automatically find models/best.pt and enable detection!
