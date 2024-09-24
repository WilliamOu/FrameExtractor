import cv2
import os

def fix_path(path):
    path = path.replace("\\", "/")
    path = path.strip('"')
    return path

def crop_frame(frame, center_x, center_y, width, height, full_frame=False):
    if full_frame:
        return frame

    start_x = max(center_x - width // 2, 0)
    start_y = max(center_y - height // 2, 0)

    cropped_frame = frame[start_y:start_y + height, start_x:start_x + width]

    return cropped_frame

def extract_frames(mp4_path, output_folder, start_frame, end_frame, center_x, center_y, crop_width, crop_height, full_frame):
    video_capture = cv2.VideoCapture(mp4_path)

    if not video_capture.isOpened():
        print(f"Error: Could not open video file {mp4_path}")
        return

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Original frame size: {frame_width}x{frame_height}")
    print(f"Center of the original frame: ({frame_width // 2}, {frame_height // 2})")

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in the video: {total_frames}")

    if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
        print(f"Invalid frame range: {start_frame} to {end_frame}. Total frames: {total_frames}")
        return

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_number = start_frame
    series_index = 1 
    while frame_number <= end_frame:
        success, frame = video_capture.read()

        if not success:
            print(f"Error: Failed to read frame {frame_number}.")
            break

        cropped_frame = crop_frame(frame, center_x, center_y, crop_width, crop_height, full_frame)

        frame_filename = os.path.join(output_folder, f"Frame {series_index}.png")
        try:
            cv2.imwrite(frame_filename, cropped_frame)
            print(f"Saved frame {frame_number} to {frame_filename}")
        except Exception as e:
            print(f"Error saving frame {frame_number}: {e}")
            break

        frame_number += 1
        series_index += 1 

    video_capture.release()
    print("Frame extraction completed.")

def get_valid_paths():
    while True:
        mp4_file_path = input("Enter the path to the MP4 video file: ")
        output_dir = input("Enter the output folder path (it will be created if it doesn't exist): ")

        mp4_file_path = fix_path(mp4_file_path)
        output_dir = fix_path(output_dir)

        if not os.path.isfile(mp4_file_path):
            print(f"Error: The file {mp4_file_path} does not exist. Please try again.")
            continue

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created output folder: {output_dir}")
            except OSError as e:
                print(f"Error creating output folder: {e}. Please try again.")
                continue

        return mp4_file_path, output_dir

def main():
    mp4_file_path, output_dir = get_valid_paths()

    video_capture = cv2.VideoCapture(mp4_file_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {mp4_file_path}")
        exit()

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Original frame size: {frame_width}x{frame_height}")
    print(f"Center of the original frame: ({frame_width // 2}, {frame_height // 2})")
    video_capture.release()

    while True:
        while True:
            try:
                start_frame = int(input("Enter the starting frame number (0-based): "))
                end_frame = int(input("Enter the ending frame number: "))
                break
            except ValueError:
                print("Please enter valid frame numbers.")

        full_frame = False
        while True:
            try:
                center_x_input = input(f"Enter the X coordinate for the center point (default: {frame_width // 2}, press Enter to use full frame): ")
                center_y_input = input(f"Enter the Y coordinate for the center point (default: {frame_height // 2}, press Enter to use full frame): ")
                crop_width_input = input(f"Enter the width of the cropped image (press Enter to use full frame): ")
                crop_height_input = input(f"Enter the height of the cropped image (press Enter to use full frame): ")

                if not center_x_input and not center_y_input and not crop_width_input and not crop_height_input:
                    print("No cropping will be applied. Using full frame.")
                    full_frame = True
                    center_x, center_y, crop_width, crop_height = frame_width // 2, frame_height // 2, frame_width, frame_height
                else:
                    center_x = int(center_x_input or frame_width // 2)
                    center_y = int(center_y_input or frame_height // 2)
                    crop_width = int(crop_width_input or frame_width)
                    crop_height = int(crop_height_input or frame_height)

                break
            except ValueError:
                print("Please enter valid numbers for the center point, width, and height.")

        extract_frames(mp4_file_path, output_dir, start_frame, end_frame, center_x, center_y, crop_width, crop_height, full_frame)

        while True:
            adjust_choice = input("Do you want to adjust parameters and reprocess (Y/N)? ").lower()
            if adjust_choice == 'y':
                break
            elif adjust_choice == 'n':
                print("Exiting the program.")
                return
            else:
                print("Invalid input. Please enter 'Y' to adjust or 'N' to exit.")

main()
