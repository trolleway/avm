import subprocess
import os

def concatenate_clips(input_dir, output_file):
    # 1. Gather and sort all generated .ts slide files
    clips = [f for f in os.listdir(input_dir) if f.startswith("slide_") and f.endswith(".ts")]
    clips.sort()
    
    if not clips:
        print("No clip files found to concatenate.")
        return

    # 2. Path for the temporary text file FFmpeg requires
    concat_list_path = os.path.join(input_dir, "concat_list.txt")
    
    # 3. Write paths into the text file using FFmpeg's strict syntax
    # Note: Using forward slashes for cross-platform compatibility
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")
            
    print(f"Created concatenation manifest with {len(clips)} files.")

    # 4. Build the lossless copy command
    cmd = [
        'ffmpeg',
        '-y',                           # Overwrite final file if it exists
        '-f', 'concat',                 # Use the concat demuxer
        '-safe', '0',                   # Allow absolute/relative paths
        '-i', concat_list_path,         # Pass the text file list
        '-c', 'copy',                   # Stream copy video/audio directly (NO RE-COMPRESSION)
        output_file
    ]
    
    # 5. Execute the operation
    try:
        print("Stitching clips together losslessly...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Final video successfully created: {output_file}")
        
        # Clean up the manifest file after successful merge
        os.remove(concat_list_path)
        
    except subprocess.CalledProcessError as e:
        print(f"Error during concatenation: {e.stderr}")
        
def create_crossfade_slideshow(img1_path, img2_path, output_path):
    # FFmpeg command split into a list for safe execution
    cmd = [
        'ffmpeg',
        '-y', # Overwrite output file if it exists
        '-loop', '1', '-t', '3', '-i', img1_path, # Image 1 loops for 5 seconds
        '-loop', '1', '-t', '3', '-i', img2_path, # Image 2 loops for 5 seconds
        '-filter_complex', 
        # Scale and pad image 1 to exactly 4K (3840x2160) with black bars
        #'[0:v]scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];'
        '[0:v]crop=in_w:in_w*9/16:0:(in_h-(in_w*9/16))/2,scale=3840:2160[v1];'
        # Scale and pad image 2 to exactly 4K
        #'[1:v]scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1[v2];'
        '[1:v]crop=in_w:in_w*9/16:0:(in_h-(in_w*9/16))/2,scale=3840:2160[v2];'
        # Crossfade transition: 1 second long, starting at the 1.5-second mark
        '[v1][v2]xfade=transition=fade:duration=0.5:offset=1.5[v]',
        '-map', '[v]',
        '-g', '10',                         # Force a keyframe every 30 frames (0.5 seconds at 60fps)
        '-force_key_frames', 'expr:eq(t,3)',# Force a pristine Keyframe exactly at the 3-second mark (fade start)
        '-x264-params', 'aq-mode=3:no-mbtree=1', # Improve handling of dark areas/bi-directional fades
        
        '-r', '48',            # Set output frame rate to 60 FPS
        '-c:v', 'libx264',     # Use H.264 codec for high compatibility during concatenation
        '-preset', 'veryslow',     # Use H.264 codec for high compatibility during concatenation
        '-crf', '20',     # Use H.264 codec for high compatibility during concatenation
        '-pix_fmt', 'yuv420p', # Ensure universal playback compatibility
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Video successfully created: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution: {e}")


dir_path = "img"
file_paths = []

# Loop through the directory contents
for item in os.listdir(dir_path):
    # Construct the full path
    full_path = os.path.join(dir_path, item)
    
    # Check if the item is a file (skips directories)
    if os.path.isfile(full_path):
        file_paths.append(full_path)

# Sort the paths alphabetically
file_paths.sort()

for i in range(len(file_paths)-1):
    create_crossfade_slideshow(file_paths[i], file_paths[i+1], f'slide_{i:06d}.ts')
    
directory_of_slides = "."  
final_output = "slideshow.mp4"

concatenate_clips(directory_of_slides, final_output)