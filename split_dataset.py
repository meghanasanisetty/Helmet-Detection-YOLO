import os
import random
import shutil

# Paths
image_dir = "data/images"
label_dir = "data/labels"

train_img_dir = "data/images/train"
val_img_dir = "data/images/val"
train_lbl_dir = "data/labels/train"
val_lbl_dir = "data/labels/val"

# Create folders if they don't exist
os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(val_img_dir, exist_ok=True)
os.makedirs(train_lbl_dir, exist_ok=True)
os.makedirs(val_lbl_dir, exist_ok=True)

# Get all image filenames
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg") or f.endswith(".png")]
random.shuffle(images)
split_index = int(0.8 * len(images))  # 80% train, 20% val

for i, img in enumerate(images):
    label = img.rsplit('.', 1)[0] + ".txt"
    src_img = os.path.join(image_dir, img)
    src_lbl = os.path.join(label_dir, label)
    
    if not os.path.exists(src_lbl):
        print(f"⚠️ Missing label for {img}, skipping...")
        continue
    
    if i < split_index:
        shutil.move(src_img, train_img_dir)
        shutil.move(src_lbl, train_lbl_dir)
    else:
        shutil.move(src_img, val_img_dir)
        shutil.move(src_lbl, val_lbl_dir)

print("✅ Dataset split complete!")
print(f"Training images: {len(os.listdir(train_img_dir))}")
print(f"Validation images: {len(os.listdir(val_img_dir))}")
