pipeline {
    agent any

    environment {
        PATH = "/Users/muhammadmasood/.docker/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {

        stage('Test Jenkins') {
            steps {
                echo 'Jenkins is working!'
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-users:latest .'
            }
        }

        stage('Run Flask Container') {
            steps {
                sh '''
                    docker rm -f flask-users-test 2>/dev/null || true
                    docker run -d --name flask-users-test -p 5001:5000 flask-users:latest
                    sleep 5
                '''
            }
        }

        stage('Test Flask Application') {
            steps {
                sh 'curl -f http://localhost:5001'
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker rm -f flask-users-test'
            }
        }
    }
}