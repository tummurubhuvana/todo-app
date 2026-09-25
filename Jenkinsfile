// Runs automatically after this job has executed once and Jenkins
// is polling GitHub. A new commit on the watched branch starts:
// checkout -> docker build -> confirm the Todo API answers.
//
// One-time Jenkins job setup (Pipeline script from SCM):
//   Repository URL: https://github.com/tummurubhuvana/todo-app
//   Branch: */main
//   Script Path: Jenkinsfile
// Then click Build Now once so Jenkins loads the poll trigger below.
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'tummurubhuvana/todo-api'
    }

    triggers {
        // About every 2 minutes, build only when GitHub has new commits.
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Getting Todo application code from GitHub'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image from the Dockerfile'
                sh '''
                    SHORT_SHA=$(git rev-parse --short HEAD)
                    echo "Building ${IMAGE_NAME}:${SHORT_SHA} from commit ${SHORT_SHA}"
                    docker build \
                        -t "${IMAGE_NAME}:${SHORT_SHA}" \
                        -t "${IMAGE_NAME}:latest" \
                        .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                echo 'Starting the image and checking the Todo API'
                sh '''
                    docker images "${IMAGE_NAME}"
                    docker rm -f todo-api-smoke >/dev/null 2>&1 || true
                    docker run -d --name todo-api-smoke "${IMAGE_NAME}:latest"

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
                        if docker exec todo-api-smoke python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2).read()"; then
                            echo "Todo API is up"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Todo API did not become ready"
                    docker logs todo-api-smoke
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f todo-api-smoke >/dev/null 2>&1 || true'
        }
    }
}
