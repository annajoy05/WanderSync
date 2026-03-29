from PIL import Image

def remove_white_bg(input_path, output_path, tolerance=220):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Check if pixel is close to white (R, G, B > tolerance)
            if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
                # Replace with transparent pixel
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Successfully removed background and saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == "__main__":
    import sys
    import os
    
    input_file = "static/logo-source.png"
    output_file = "static/logo.png"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please ensure the image is saved in the correct location.")
        sys.exit(1)
        
    remove_white_bg(input_file, output_file)
