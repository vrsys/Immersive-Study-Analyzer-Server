[![Build](https://github.com/vrsys/Immersive-Study-Analyzer-Server/actions/workflows/run.yml/badge.svg)](https://github.com/vrsys/Immersive-Study-Analyzer-Server/actions/workflows/run.yml)

# Immersive Study Analyzer Server

This rest server can be used to store and retrieve data such as recordings and annotations.
It was designed for use with the Immersive Study Analyzer (ISA), which Unity implementation can be found [here](https://github.com/vrsys/Immersive-Study-Analyzer-Server).

Setup:
========================
**Step 1**: Clone the repository
```
git clone https://github.com/AnBenLa/UnityRecordingRestAPI
```

**Step 2**: Install dependencies (optional: using a conda environment)
```
pip install -r requirements.txt
```

**Step 3**: Start the flask server. Example start commands can be found [here](https://flask.palletsprojects.com/en/1.1.x/cli/#).
```
python -m flask run
```
