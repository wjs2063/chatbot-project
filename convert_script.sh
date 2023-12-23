#!/bin/bash

# Iterate through each subfolder in the current directory
for folder in */; do
  # Navigate into the subfolder
  cd "$folder" || exit

  # Check if the subfolder has WMV files
  if [ -n "$(find . -maxdepth 1 -type f -name '*.wmv')" ]; then
    # Convert WMV files to MP4 in the subfolder
    for file in *.wmv; do
      ffmpeg -i "$file" -c:v libx264 -c:a aac -strict experimental "${file%.wmv}.mp4"
      
      # 성공여부 체크
      if [ $? -eq 0 ]; then
        rm "$file"  # Remove the original WMV file if the conversion was successful
        echo "wmv 파일 삭제 완료: $file"
      else
        echo "변환 실패: $file"
      fi
    done

    echo "Conversion completed for folder: $folder"
  else
    echo "No WMV files found in folder: $folder"
  fi

  # Move back to the parent directory
  cd ..
done

