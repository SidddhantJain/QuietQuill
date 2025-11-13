# Jenkins CI/CD Setup for QuietQuill

This guide covers essential Jenkins tasks for your project as per Unit II & III requirements.

---

## Unit II

### 1. Install Jenkins and Create a New Job

- **Verify Jenkins Installation:**  
  Access Jenkins at `http://localhost:8080` (or your configured port).
- **Create Freestyle Project:**  
  - Go to **New Item** > **Freestyle project** > Name: `HelloJenkins`
  - In **Build** section, add a build step:  
    - **Execute shell**:  
      ```sh
      echo "Hello, Jenkins!"
      ```
  - Save and **Build Now**.  
  - Check console output for "Hello, Jenkins!"

---

### 2. Source Code Management

- **Configure Git SCM:**  
  - In your job, go to **Source Code Management** > **Git**
  - Enter your repository URL (e.g., `https://github.com/yourusername/QuietQuill.git`)
  - Specify branch (e.g., `main`)
  - **Install Git plugin** if prompted.

---

### 3. Build Triggers

- **Enable GitHub hook trigger for GITScm polling:**  
  - In job config, **Build Triggers** > check **GitHub hook trigger for GITScm polling**
  - Set up webhook in your GitHub repo:  
    - URL: `http://<jenkins-server>:8080/github-webhook/`
  - On push, Jenkins will trigger a build.

---

### 4. Manage Plugins

- **Install Plugins:**  
  - Go to **Manage Jenkins** > **Manage Plugins**
  - Search and install:
    - **Git plugin** (for SCM)
    - **Email Extension Plugin** (for notifications)
    - Optionally: **Docker plugin**, **JUnit plugin**

---

### 5. Build Automation

- **Add Build Script:**  
  - In job config, **Build** > **Execute shell**:  
    ```sh
    python -m unittest discover
    ```
  - This will run Python unit tests.

---

### 6. Email Notifications

- **Configure Email:**  
  - In **Post-build Actions** > **Editable Email Notification**
  - Set SMTP server (e.g., Gmail SMTP)
  - Add recipient list.
  - Jenkins will send emails on build success/failure.

---

### 7. Pipeline Creation

- **Create Pipeline Job:**  
  - New Item > Pipeline > Name: `QuietQuillPipeline`
  - Add a `Jenkinsfile` to your repo:
    ```groovy
    pipeline {
      agent any
      stages {
        stage('Build') {
          steps {
            sh 'echo "Building..."'
          }
        }
        stage('Test') {
          steps {
            sh 'python -m unittest discover'
          }
        }
        stage('Deploy') {
          steps {
            sh 'echo "Deploy stage (customize as needed)"'
          }
        }
      }
    }
    ```
  - In job config, point to your `Jenkinsfile`.

---

### 8. Build with Maven/Gradle

- **Java Project Example:**  
  - In job config, **Build** > **Invoke top-level Maven targets**  
    - Goals: `clean install`
  - Ensure `pom.xml` is present in your repo.

---

### 9. Scheduled Builds

- **Configure Schedule:**  
  - In job config, **Build Triggers** > **Build periodically**
  - Example schedule:  
    ```
    H 0 * * *   # Every day at midnight
    ```

---

## Unit III

### 1. Install & Verify Docker

- **Install Docker:**  
  - `sudo apt install docker.io` (Linux) or download from [docker.com](https://www.docker.com/)
  - Verify:  
    ```sh
    docker --version
    docker run hello-world
    ```

---

### 2. Docker Commands

- **Start/Stop Containers:**  
  ```sh
  docker run -d --name mycontainer ubuntu
  docker ps
  docker stop mycontainer
  docker start mycontainer
  docker rm mycontainer
  ```

---

## Next Steps

- Integrate Jenkins with Docker for build/test environments if needed.
- Use Jenkins pipelines for automated CI/CD.
- Document all steps/screenshots for your submission.

---




