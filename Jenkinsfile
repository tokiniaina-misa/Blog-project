pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'blogproject.settings'
        POSTGRES_USER = 'bloguser'
        POSTGRES_PASSWORD = 'blogpassword'
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

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results/junit.xml --cov=./ --cov-report=xml
                '''
            }
        }

        stage('Generate Reports') {
            steps {
                junit 'test-results/junit.xml'
                publishCoverage(
                    adapters: [coberturaAdapter('coverage.xml')]
                )
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'test-results/junit.xml, coverage.xml', fingerprint: true
            }
        }
    }

    post {
        always {
            sh 'docker-compose down'
            cleanWs()
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}