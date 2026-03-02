# Without Docker

Please install uv first: 
```curl -LsSf https://astral.sh/uv/install.sh | sh```

To get started, clone the repository.
Then, move to the nevus_app directory and start the app:
```
cd nevus_app
uv run app.py
```
In your browser, navigate to ```http://localhost:5050``` and you can start submitting photos.

# With Docker

## Building the image

Run the following commands:
```
sudo docker build -t nevus_app . --no-cache
sudo docker run -d --rm -p 5050:5050 nevus_app
```
In your browser, navigate to ```http://localhost:5050``` and you can start submitting photos.

## Downloading the image

Run the following command:
```
sudo docker run -d --rm -p 5050:5050 dimdim38/nevus_app:latest
```
In your browser, navigate to ```http://localhost:5050``` and you can start submitting photos.