# jik-api-v2.0-Alpha
[![Github Issues](https://img.shields.io/github/issues-raw/Njoguu/jik-api-v2.0-Alpha)](https://github.com/Njoguu/jik-api-v2.0-Alpha/issues) 
[![Github pull requests](https://img.shields.io/github/issues-pr-raw/Njoguu/jik-api-v2.0-Alpha?color=yellow)](https://github.com/Njoguu/jik-api-v2.0-Alpha/pulls)

### Description:
jik-api Data Scraper is the easiest way to get access to the latest job opportunities in Kenya, link to the job posting/application page, date posted and returns this data in JSON format.

### Features
- GET All Job Postings with the link to application page, the date posted, and its description 
- GET Jobs with specific keywords
- GET Jobs posted on a specific date
- Use Query Parameters to get specific jobs

## Development:
### Setup & Installtion

Clone the repository using the following command.

```bash
git clone https://github.com/Njoguu/jik-api-v2.0-Alpha.git
```

### Viewing The App: with Docker
1. Make sure you have docker installed.

2. Navigate to the folder structure then build the container with the command 
```bash 
docker build -t <your-image-name> .
```

3. Run the container with the command 
```bash 
docker run -d -p 5000:5000 <your-image-name>
```

### To view the app

Go to `http://127.0.0.1:5000`
