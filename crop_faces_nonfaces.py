import os
import cv2
import random



def load_annotations(annotation_path):
    """
    Returns a dictionary:
        { 
          'filename.jpg': [(xmin, ymin, xmax, ymax, label), (xmin2, ymin2, ...), ...], 
          'other.jpg': [...]
        }
    """
    annotations_by_image = {}
    with open(annotation_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            image_name = parts[0]
            xmin, ymin, xmax, ymax = map(int, parts[1:5])
            label = parts[5] if len(parts) > 5 else "unknown"
            
            if image_name not in annotations_by_image:
                annotations_by_image[image_name] = []
            
           
            annotations_by_image[image_name].append((xmin, ymin, xmax, ymax, label))
    return annotations_by_image

def boxes_do_not_overlap(xmin1, ymin1, xmax1, ymax1, xmin2, ymin2, xmax2, ymax2):
    """
    Returns True if the two boxes do NOT overlap at all.
    """
  
    if xmax1 <= xmin2 or xmin1 >= xmax2:
        return True
    if ymax1 <= ymin2 or ymin1 >= ymax2:
        return True
    return False

def generate_nonface_patch(image, face_width, face_height, all_faces):
    """
    Tries up to 10 random times to find a valid non-face patch of size
    face_width x face_height that does not overlap ANY face in `all_faces`.
    Returns the cropped patch or None if none found.
    """
    h, w = image.shape[:2]
    
    for _ in range(10): 
        crop_xmin = random.randint(0, w - face_width)
        crop_ymin = random.randint(0, h - face_height)
        crop_xmax = crop_xmin + face_width
        crop_ymax = crop_ymin + face_height

       
        overlap_any_face = False
        for (fxmin, fymin, fxmax, fymax, label) in all_faces:
            if not boxes_do_not_overlap(crop_xmin, crop_ymin, crop_xmax, crop_ymax, fxmin, fymin, fxmax, fymax):
              
                overlap_any_face = True
                break
        
        if overlap_any_face:
            continue 

       
        non_face_patch = image[crop_ymin:crop_ymax, crop_xmin:crop_xmax]
        return non_face_patch
   
    return None

def crop_faces_and_nonfaces(
    base_dir, image_folder, annotation_file, output_dir, face_counter, nonface_counter,
    resize_dim=(64,64) 
):
    """
    Processes the given image folder + annotation file:
      - Crops each face
      - Creates non-face patches for each face (3 per face) with no overlap to ANY face in that image
    """
    annotation_path = os.path.join(base_dir, annotation_file)
    annotations_by_image = load_annotations(annotation_path)

   
    face_dir = os.path.join(output_dir, "faces")
    nonface_dir = os.path.join(output_dir, "non_faces")
    os.makedirs(face_dir, exist_ok=True)
    os.makedirs(nonface_dir, exist_ok=True)

   
    for image_name, face_bboxes in annotations_by_image.items():
       
        image_path = os.path.join(base_dir, image_folder, image_name)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not load image {image_path}")
            continue

        for idx, (xmin, ymin, xmax, ymax, label) in enumerate(face_bboxes):
           
            face = image[ymin:ymax, xmin:xmax]
            if face.size == 0:
                print(f"Warning: Invalid face crop in {image_name}, skipping...")
                continue

           
            face_resized = cv2.resize(face, resize_dim)
            face_output_path = os.path.join(face_dir, f"{face_counter}.jpg")
            cv2.imwrite(face_output_path, face_resized)
            print(f"[Face] {image_name} => {face_output_path}")
            face_counter += 1

          
            face_width = xmax - xmin
            face_height = ymax - ymin
            for _ in range(3): 
                non_face_patch = generate_nonface_patch(image, face_width, face_height, face_bboxes)
                if non_face_patch is not None:
                    non_face_resized = cv2.resize(non_face_patch, resize_dim)
                    nonface_output_path = os.path.join(nonface_dir, f"{nonface_counter}.jpg")
                    cv2.imwrite(nonface_output_path, non_face_resized)
                    print(f"[Non-Face] {image_name} => {nonface_output_path}")
                    nonface_counter += 1

    return face_counter, nonface_counter

if __name__ == "__main__":
  
    BASE_DIR = "C:/Users/alexn/Downloads/cava_tema_2/antrenare/"
    IMAGE_FOLDERS = ["mom", "dad", "dexter", "deedee"]
    ANNOTATION_FILES = ["mom_annotations.txt", "dad_annotations.txt", "dexter_annotations.txt", "deedee_annotations.txt"]
    OUTPUT_DIR = "C:/Users/alexn/Downloads/cava_tema_2/cropped_faces_64x64_v2/"

    face_counter = 1
    nonface_counter = 1

    for image_folder, annotation_file in zip(IMAGE_FOLDERS, ANNOTATION_FILES):
        print(f"\nProcessing folder: {image_folder} with annotations: {annotation_file}")
        face_counter, nonface_counter = crop_faces_and_nonfaces(
            base_dir=BASE_DIR,
            image_folder=image_folder,
            annotation_file=annotation_file,
            output_dir=OUTPUT_DIR,
            face_counter=face_counter,
            nonface_counter=nonface_counter,
            resize_dim=(64, 64)  
        )
    print("Face and non-face cropping complete.")
