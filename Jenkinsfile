pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'echo Building...'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m unittest discover'
            }
        }
        stage('Deploy') {
            steps {
                bat 'echo Deploy stage (customize as needed)'
            }
        }
            stage('Docker Build') {
                steps {
                    bat 'docker build -t quietquill .'
                }
            }
    }
}
