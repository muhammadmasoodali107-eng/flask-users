pipeline {

    agent any

    environment {
        PATH = "/Users/muhammadmasood/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
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
                sh '''
                    docker --version
                    docker info
                '''
            }
        }

        stage('Check Kubernetes / Minikube') {
            steps {
                withKubeConfig([credentialsId: 'minikube-kubeconfig']) {
                sh '''
                echo "Kubernetes Client:"
                kubectl version --client

                echo "Current Context:"
                kubectl config current-context

                echo "Kubernetes Nodes:"
                kubectl get nodes
                '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t $DOCKER_IMAGE:$BUILD_NUMBER \
                        -t $DOCKER_IMAGE:latest .
                '''
            }
        }

        stage('Test Docker Container') {
            steps {
                sh '''
                    docker rm -f flask-users-test || true

                    docker run -d \
                        --name flask-users-test \
                        -p 5001:5000 \
                        $DOCKER_IMAGE:$BUILD_NUMBER

                    sleep 5

                    curl -f http://localhost:5001
                '''
            }
        }

        stage('Cleanup Test Container') {
            steps {
                sh '''
                    docker rm -f flask-users-test || true
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push $DOCKER_IMAGE:$BUILD_NUMBER
                        docker push $DOCKER_IMAGE:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withKubeConfig([credentialsId: 'minikube-kubeconfig']) {
                sh '''
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                kubectl set image deployment/flask-users \
                    flask-users=$DOCKER_IMAGE:$BUILD_NUMBER

                kubectl rollout status deployment/flask-users --timeout=120s
                '''
                }
            }
        }


        stage('Verify Kubernetes Deployment') {
            steps {
                withKubeConfig([credentialsId: 'minikube-kubeconfig']) {
                sh '''
                echo "Pods:"
                kubectl get pods -o wide

                echo "Deployment:"
                kubectl get deployment flask-users

                echo "Service:"
                kubectl get service flask-users-service
                '''
                }
            }
       }


    post {
        success {
            echo '======================================'
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
            echo '======================================'
            echo "Docker Image: $DOCKER_IMAGE:$BUILD_NUMBER"
            echo "Kubernetes: Minikube"
        }

        failure {
            echo '======================================'
            echo 'CI/CD PIPELINE FAILED'
            echo '======================================'
        }
    }
}