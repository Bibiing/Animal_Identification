from rembg import remove
import argparse
import os

def process_dataset_structure(input_root, output_root):
    if not os.path.exists(input_root):
        print(f"folder {input_root} not found.")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    # get all animal category folders
    animal_folders = [f for f in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, f))]

    print(f"Found {len(animal_folders)} animal categories: {animal_folders}")

    # loop through each animal folder
    for animal in animal_folders:
        path_to_animal = os.path.join(input_root, animal)      
        path_to_save = os.path.join(output_root, animal)       

        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        
        print(f"\nprocessing: {animal}...")
        
        files = os.listdir(path_to_animal)
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(path_to_animal, filename)
                
                filename_no_ext = os.path.splitext(filename)[0]
                output_filename = filename_no_ext + ".png"
                output_path = os.path.join(path_to_save, output_filename)

                if os.path.exists(output_path):
                    continue

                try:
                    with open(input_path, 'rb') as i:
                        input_data = i.read()

                    # alpha_matting=True bagus untuk bulu, tapi agak lambat.
                    # if to slow, set alpha_matting=False
                    subject = remove(input_data, alpha_matting=True, alpha_matting_foreground_threshold=240)

                    with open(output_path, 'wb') as o:
                        o.write(subject)
                    
                except Exception as e:
                    print(f"\nfailed to process {filename}: {e}")
        
        print(f"\n done brodii {animal}.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Preprocess dataset by removing backgrounds from images.")
    parser.add_argument("--input_folder", type=str, default="animal_data", help="Path to the input dataset folder.")
    parser.add_argument("--output_folder", type=str, default="processed_data", help="Path to save the processed dataset.")
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    process_dataset_structure(args.input_folder, args.output_folder)
    print("\nAll done brodii..!")

if __name__ == "__main__":
    main()