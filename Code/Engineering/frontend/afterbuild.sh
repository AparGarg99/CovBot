cd ../backend
if [ ! -d "./static" ]; then
    mkdir static
    echo '/backend/static creacted successfully'
else
    echo '/backend/static exits'
fi

echo "Start moving the build result to backend!"
cd ../frontend
rm -rf ../backend/static/*
mv ./dist/* ../backend/static
echo "Moving Finish!"