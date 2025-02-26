# NavFlow
## Smart Traffic Congestion Prediction and Navigation using Camera Data in Ho Chi Minh City

### Data Crawling for Dataset Collection
To collect images for training the dataset, follow these steps:

```
Step 1: Navigate to the `data_crawl_demo` folder.
Step 2: Activate the virtual environment:
        venv/Scripts/activate.bat
Step 3: Run the data crawling script:
        python data_crawl_demo.py
Step 4: Images will be organized by camera and stored in the `dataset_raw` folder.
```

### Running the Trained Model
To run the pre-trained model for vehicle detection and congestion prediction:

```
Step 1: Navigate to the `data_crawl_demo` folder.
Step 2: Activate the virtual environment:
        venv/Scripts/activate.bat
Step 3: Open `yolo_detection.py` and verify the number of images to be processed (default is 2).
Step 4: Run the main script:
        python yolo_detection.py
Step 5: Detection results will be displayed in the terminal.
        Processed images with detected vehicles will be saved in the `detections` folder.
```

This project aims to enhance traffic navigation by utilizing camera data to predict congestion and suggest alternative routes.

### Libraries used in this project
#### Core Libraries:
numpy, scipy, pandas, matplotlib, seaborn
requests, urllib3, certifi
#### Machine Learning & Deep Learning:
torch, torchvision, torchaudio, ultralytics, ultralytics-thop
#### Computer Vision:
opencv-python, pillow
#### Web Scraping & Parsing:
beautifulsoup4, soupsieve, lxml, Jinja2, MarkupSafe
#### Utilities & Others:
tqdm, psutil, py-cpuinfo, filelock, python-dateutil, pytz, tzdata
#### Testing & Packaging:
pytest, iniconfig, pluggy, setuptools, packaging
