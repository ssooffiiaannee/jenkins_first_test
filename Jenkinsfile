pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['none', 'staging', 'production'],
            description: 'Optional deploy target (example only)'
        )
        booleanParam(
            name: 'RUN_SMOKE',
            defaultValue: true,
            description: 'Run post-build smoke check'
        )
    }

    environment {
        PYTHON = 'python3'
        VENV_DIR = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    set -e
                    ${PYTHON} -m venv "${VENV_DIR}"
                    . "${VENV_DIR}/bin/activate"
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . "${VENV_DIR}/bin/activate"
                    mkdir -p test-results
                    pytest -v --junitxml=test-results/junit.xml tests/
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
                }
            }
        }

        stage('Package') {
            steps {
                sh '''
                    . "${VENV_DIR}/bin/activate"
                    mkdir -p dist
                    tar -czf dist/app-${BUILD_NUMBER}.tar.gz app/ requirements.txt
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOY_ENV != 'none' }
            }
            steps {
                echo "Example deploy to ${params.DEPLOY_ENV} (build ${env.BUILD_NUMBER})"
                sh '''
                    echo "Would deploy dist/app-${BUILD_NUMBER}.tar.gz here"
                '''
            }
        }

        stage('Smoke') {
            when {
                expression { params.RUN_SMOKE }
            }
            steps {
                sh '''
                    . "${VENV_DIR}/bin/activate"
                    python -c "from app.main import greet; assert greet('Jenkins') == 'Hello, Jenkins!'"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully.'
        }
        failure {
            echo 'Pipeline failed — check stage logs above.'
        }
        cleanup {
            sh 'rm -rf "${VENV_DIR}" || true'
        }
    }
}
