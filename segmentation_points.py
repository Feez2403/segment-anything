import cv2
import json
import os
import sys

# Initialize the dictionary to store coordinates
coordinates = {}
img_id = 0
images_folder = './notebooks/wildtrack_processed/images/'


def click_event(event, x, y, flags, params):
    # Check if left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates[img_id].append([x, y])
        print(f'Point annotated at: {x}, {y}')
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow(f'image', img)

# Driver Code
if __name__=="__main__":
    # Load all images in the 'images' directory
    images = os.listdir(images_folder)
    i = 0                          
    #eventually load existing annotations from a json file
    if os.path.exists('annotations.json'):
        with open('annotations.json', 'r') as json_file: 
            coordinates = json.load(json_file)
            
    while i < len(images):
        img_id = images[i]
        if img_id not in coordinates:
            prev_img_id = images[i-1] if i > 0 else None
            coordinates[img_id] = coordinates[prev_img_id].copy() if prev_img_id is not None else []
        # Reading the image
        img = cv2.imread(f'{images_folder}{img_id}')
        # Draw points from previous images
        for x, y in coordinates[img_id]:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        # Display the image
        cv2.putText(img, f'Image {img_id}/{len(images)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow(f'image', img)
        # Set mouse callback function for window
        cv2.setMouseCallback(f'image', click_event)
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('c'):  # clear points
                img = cv2.imread(f'{images_folder}{img_id}')
                coordinates[img_id].clear()
                cv2.imshow(f'image', img)
            elif key == 32:  # Enter key
                i += 1 
                break
            elif key == ord('z'):  # undo
                if i > 0:
                    i -= 1
                break
            elif key == ord('q'):  # quit
                sys.exit()
            if cv2.getWindowProperty(f'image', cv2.WND_PROP_VISIBLE) < 1:  
                sys.exit()
        cv2.destroyAllWindows()

    # Save coordinates to a json file
    with open('annotations.json', 'w') as json_file:
        json.dump(coordinates, json_file, indent=4)