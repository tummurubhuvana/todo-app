pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Getting Todo application code from GitHub'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'

                sh '''
                    docker build -t tummurubhuvana/todo-api:latest .
                '''
            }
        }

        stage('Docker Image Check') {
            steps {
                echo 'Checking the Docker image'

                sh '''
                    docker images tummurubhuvana/todo-api
                '''
            }
        }
    }
}