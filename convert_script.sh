for folder in */; do
  # Navigate into the subfolder
  cd "$folder" || exit

  # Check if the subfolder has WMV files
  if [ -n "$(find . -maxdepth 1 -type f -name '*.wmv')" ]; then
    # Convert WMV files to MP4 in the subfolder
    for file in *.wmv; do
      ffmpeg -i "$file" -c:v libx264 -c:a aac -strict experimental "${file%.wmv}.mp4"
    done

    echo "mp4 변환완료: $folder"
  else
    echo "wmv파일이 없습니다: $folder"
  fi

  # Move back to the parent directory
  cd ..
done
