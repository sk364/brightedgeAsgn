# Installation  
> pip install -r requirements.txt 

> sudo apt-get install libtidy-0.99-0   

# Usage
> python app.py  

Create a POST request on `localhost:5000/` with data as key `url` and value as any valid url.  
For eg -  
> curl -X POST -d "url=https://www.google.com/" http://localhost:5000/
