

if [ "$#" -lt 1 ]
then
    # Did not provide a video file.
    echo "$0: video file must be provided"
    exit 1
fi

dirname="./.frames_$1"

if [ -d $dirname ]
then
    # Thank the user for the free directory.
    echo "Directory '$dirname' already exists. Thanks, bro!"
else
    # Make a directory to hold the frames.
    mkdir $dirname
    echo "Created directory '$dirname'"

    # Split the video into frames.
    ffmpeg -i $1 $dirname/frame%d.png  > /dev/null 2>&1

    if [ $? -ne 0 ]
    then
        # Clean up whatever mess was left behind
        echo "Error extracting frames from $1 using ffmpeg"
        rm $dirname/*
        rmdir $dirname
        exit 1
    fi

fi

# Get the number of files in the frames directory
num_files=0
for f in $dirname/*
do
    num_files=$((num_files+1))
done

echo "Found $num_files frames"

# Use the frames to perform clustering.
out_file=output.png
if [ "$#" -gt 1 ]
then
    out_file=$2
fi

# Create the image
python main.py $num_files $dirname $out_file

if [ $? -ne 0 ]
then
    echo "Failed to perform clustering on $1"
else
    echo "Conversion complete!"
fi

# Perform cleanup
rm $dirname/*
rmdir $dirname

