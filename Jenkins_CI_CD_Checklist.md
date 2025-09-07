# Jenkins CI/CD Setup Checklist for QuietQuill

## 1. Jenkins Job Configuration
- Create a Pipeline job in Jenkins.
- Set GitHub repository URL in Source Code Management.
- Select branch (e.g., `main`).
- In Pipeline section, set “Pipeline script from SCM” and point to your `Jenkinsfile`.

## 2. GitHub Webhook Setup
- Go to GitHub repo > Settings > Webhooks > Add webhook.
- Payload URL: `http://<jenkins-server>:8080/github-webhook/`
- Content type: `application/json`
- Trigger: “Just the push event.”

## 3. Recommended Jenkins Plugins
- Go to **Manage Jenkins** > **Manage Plugins** > **Available** tab.
- Search and install:
  - Git plugin
  - Email Extension Plugin
  - (Optional) Docker plugin, JUnit plugin

## 4. Jenkins Email Notification Template
- In job config, go to **Post-build Actions** > **Editable Email Notification**.
- SMTP server: (e.g., Gmail: `smtp.gmail.com`)
- Add recipient list (your email).
- Example subject: `$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!`
- Example body:
  ```
  Build Status: $BUILD_STATUS
  See console output at $BUILD_URL
  ```

## 5. Docker Integration Steps (Optional)
- Install Docker on Jenkins server.
- Install Docker plugin in Jenkins.
- Add Docker build/test steps in your `Jenkinsfile` if needed:
  ```groovy
  stage('Docker Build') {
      steps {
          bat 'docker build -t quietquill .'
      }
  }
  ```

---

Follow these steps to fully automate CI/CD for QuietQuill. If you need further help with Jenkins configuration, plugin installation, or Docker setup, let me know!
