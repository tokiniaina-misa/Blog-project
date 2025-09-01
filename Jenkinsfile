pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'blogproject.settings'
        PIP_CACHE_DIR = '.pip-cache'
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        // ...

        stage('Migrate DB') {
            steps {
                sh '. venv/bin/activate && python manage.py migrate'
            }
        }

        stage('Collectstatic') {
            steps {
                sh '. venv/bin/activate && python manage.py collectstatic --noinput'
            }
        }

        stage('Unit tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/test_accounts_models.py tests/test_blog_models.py --ds=blogproject.settings --junitxml=unit-test-results.xml --cov=accounts --cov=blog --cov-report=xml'
            }
            post {
                always {
                    junit 'unit-test-results.xml'
                }
            }
        }

        stage('Integration tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/test_accounts_integration.py tests/test_blog_integration.py --ds=blogproject.settings --junitxml=integration-test-results.xml'
            }
            post {
                always {
                    junit 'integration-test-results.xml'
                }
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t blogproject:latest .'
            }
        }

        stage('Docker smoke test') {
            steps {
                sh 'docker run -d --rm -p 8000:8000 --name blog_smoke_test blogproject:latest'
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000 || (docker logs blog_smoke_test && exit 1)'
                sh 'docker stop blog_smoke_test'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
