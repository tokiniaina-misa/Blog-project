pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        POSTGRES_USER = 'bloguser'
        POSTGRES_PASSWORD = 'blogpass'
        POSTGRES_DB = 'blogdb'
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

        stage('Run Core Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
                    
                    echo "Running Unit and Integration Tests..."
                    pytest tests/core_tests/test_units.py tests/core_tests/test_integration.py -v
                    
                    echo "Running Performance Tests..."
                    pytest tests/core_tests/test_performance.py -v
                    
                    echo "Running Database Integration Tests..."
                    pytest tests/core_tests/test_database.py -v
                    
                    echo "Generating Coverage Report..."
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