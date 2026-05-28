# Deployment Guide - Countries & Continents Dashboard

## Deploy to Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest and most direct way to deploy your Streamlit app.

### Prerequisites
- GitHub account
- Streamlit account (sign up at streamlit.io/cloud)

### Step-by-Step Deployment

#### 1. Push your code to GitHub
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit: Countries & Continents Dashboard"

# Create a repository on GitHub and add the remote
git remote add origin https://github.com/YOUR_USERNAME/dashboard_project.git
git branch -M main
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"New app"** button
3. Select:
   - **Repository:** `dashboard_project` (your GitHub repo)
   - **Branch:** `main`
   - **Main file path:** `dashboard_project/app.py`
4. Click **"Deploy!"**

#### 3. Your app will be live at:
```
https://YOUR_USERNAME-dashboard-project.streamlit.app/
```

---

## Alternative: Deploy on Other Platforms

### Heroku Deployment
Add a `Procfile` to your repo:
```
web: streamlit run dashboard_project/app.py --logger.level=error
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard_project/app.py"]
```

Then deploy to AWS, Google Cloud, or any container registry.

---

## Useful Links
- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Integration:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/connect-an-app-repository
- **Streamlit Deployment:** https://docs.streamlit.io/deploy

