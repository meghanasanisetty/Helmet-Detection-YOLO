import os
import shutil

# === CHANGE THESE PATHS IF NEEDED ===
base_dir = r'C:\Users\megha\Downloads\basic_project\HelmetDetectionYolo\data'
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')

# train & val image directories
train_img_dir = os.path.join(images_dir, 'train')
val_img_dir = os.path.join(images_dir, 'val')

# corresponding label directories (to create)
train_label_dir = os.path.join(labels_dir, 'train')
val_label_dir = os.path.join(labels_dir, 'val')

# Create label subdirectories if they don’t exist
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

def move_labels(image_dir, target_label_dir):
    for img_file in os.listdir(image_dir):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            label_file = os.path.splitext(img_file)[0] + '.txt'
            src_label_path = os.path.join(labels_dir, label_file)
            dest_label_path = os.path.join(target_label_dir, label_file)

            # Move label file if it exists
            if os.path.exists(src_label_path):
                shutil.move(src_label_path, dest_label_path)
                print(f"✅ Moved: {label_file}")
            else:
                print(f"⚠️ Label missing for: {img_file}")

# Move labels to correct subfolders
move_labels(train_img_dir, train_label_dir)
move_labels(val_img_dir, val_label_dir)

print("\n🎉 Label organization complete!")
