pipeline {
    agent any

    environment {
        PATH = "/Users/muhammadmasood/.docker/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        DOCKER_IMAGE = "muhammadmasood107/flask-users"
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

        stage('Check Kubernetes') {
            steps {
                sh 'kubectl version --client'
                sh 'kubectl config current-context'
                sh 'kubectl get nodes'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
            kubectl apply -f deployment.yaml
            kubectl apply -f service.yaml
            '''
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                sh '''
                kubectl rollout status deployment/flask-users
                kubectl get pods -o wide
                kubectl get service flask-users-service
            '''
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

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                    '''
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh 'docker tag flask-users:latest ${DOCKER_IMAGE}:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push ${DOCKER_IMAGE}:latest'
            }
        }
    }
}