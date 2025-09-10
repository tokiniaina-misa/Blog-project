pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        POSTGRES_USER = 'bloguser'
        POSTGRES_PASSWORD = 'blogpassword'
        POSTGRES_DB = 'blogdb'
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_REGION = 'eu-north-1'
        DOCKERHUB_USERNAME = credentials('DOCKERHUB_USERNAME')
        DOCKERHUB_PASSWORD = credentials('DOCKERHUB_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-django pytest-cov
                '''
            }
        }

        stage('Setup Database') {
            steps {
                sh 'docker-compose up -d db'
                sh '''
                    for i in $(seq 1 30); do
                        docker-compose exec -T db pg_isready && break
                        sleep 1
                    done
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py migrate --noinput
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKERHUB_USERNAME/blogproject:latest .
                    echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                    docker push $DOCKERHUB_USERNAME/blogproject:latest
                '''
            }
        }

        stage('Terraform Deploy') {
            steps {
                sh '''
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    unzip awscliv2.zip
                    sudo ./aws/install
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                    export AWS_REGION=$AWS_REGION
                    terraform -chdir=infra init
                    terraform -chdir=infra apply -auto-approve -var="aws_access_key=$AWS_ACCESS_KEY_ID" -var="aws_secret_key=$AWS_SECRET_ACCESS_KEY" -var="aws_region=$AWS_REGION"
                '''
            }
        }

        stage('Smoke Test EC2') {
            steps {
                script {
                    def ec2_ip = sh(script: "terraform -chdir=infra output -raw public_ip", returnStdout: true).trim()
                    sh "curl -f http://${ec2_ip}:8000 || exit 1"
                }
            }
        }

        stage('Run Core Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
                    pytest tests/core_tests/test_units.py tests/core_tests/test_integration.py -v
                    pytest tests/core_tests/test_performance.py -v
                    pytest tests/core_tests/test_database.py -v
                    pytest tests/core_tests/ --junitxml=test-results/junit.xml --cov=./ --cov-report=xml
                '''
            }
            post {
                always {
                    junit 'test-results/junit.xml'
                    publishCoverage(
                        adapters: [coberturaAdapter('coverage.xml')]
                    )
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker-compose down
                rm -rf venv
            '''
            cleanWs()
        }
        success {
            echo 'Les tests essentiels ont réussi !'
        }
        failure {
            echo 'Les tests essentiels ont échoué !'
        }
    }
}