pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: [
                'smoke',
                'usability',
                'negative',
                'edge',
                'authentication',
                'all-regression',
                'all-ui',
            ],
            description: 'Pytest suite or marker selection for this Jenkins run.',
        )
        booleanParam(
            name: 'KEEP_STACK_UP',
            defaultValue: false,
            description: 'Keep the Docker Compose stack running after the build for troubleshooting.',
        )
    }

    environment {
        PORTAL_BASE_URL = 'http://localhost:8000'
        PORTAL_BROWSER = 'chrome'
        PORTAL_HEADLESS = 'true'
        PYTEST_VENV = '.venv-jenkins'
        PYTEST_REPORT_DIR = 'reports'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Agent Tooling') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail

                    python3 --version
                    docker --version
                    docker compose version

                    if command -v google-chrome >/dev/null 2>&1; then
                      google-chrome --version
                    elif command -v google-chrome-stable >/dev/null 2>&1; then
                      google-chrome-stable --version
                    elif command -v chromium-browser >/dev/null 2>&1; then
                      chromium-browser --version
                    elif command -v chromium >/dev/null 2>&1; then
                      chromium --version
                    else
                      echo "Chrome or Chromium must be installed on the Jenkins agent."
                      exit 1
                    fi
                '''
            }
        }

        stage('Start Portal Stack') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    docker compose up -d --build
                    docker compose ps
                '''
            }
        }

        stage('Prepare Python Test Environment') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    python3 -m venv "${PYTEST_VENV}"
                    "${PYTEST_VENV}/bin/python" -m pip install --upgrade pip
                    "${PYTEST_VENV}/bin/python" -m pip install -r requirements-test.txt
                '''
            }
        }

        stage('Wait For Portal Health') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    "${PYTEST_VENV}/bin/python" scripts/wait_for_portal_health.py \
                      --base-url "${PORTAL_BASE_URL}" \
                      --timeout-seconds 90 \
                      --require-storage-ready
                '''
            }
        }

        stage('Reset Portal State') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    "${PYTEST_VENV}/bin/python" scripts/reset_environment.py
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail

                    mkdir -p "${PYTEST_REPORT_DIR}"

                    case "${TEST_SUITE}" in
                      smoke)
                        set -- tests/smoke -m smoke
                        ;;
                      usability)
                        set -- tests/regression/test_usability_regression.py -m usability
                        ;;
                      negative)
                        set -- tests/regression/test_negative_regression.py -m negative
                        ;;
                      edge)
                        set -- tests/regression/test_edge_regression.py -m edge
                        ;;
                      authentication)
                        set -- -m authentication
                        ;;
                      all-regression)
                        set -- tests/regression -m regression
                        ;;
                      all-ui)
                        set -- tests -m "smoke or regression"
                        ;;
                      *)
                        echo "Unsupported TEST_SUITE: ${TEST_SUITE}"
                        exit 1
                        ;;
                    esac

                    "${PYTEST_VENV}/bin/python" -m pytest "$@" -vv -s \
                      --junitxml="${PYTEST_REPORT_DIR}/pytest-${TEST_SUITE}.xml"
                '''
            }
        }
    }

    post {
        always {
            sh '''
                #!/bin/bash
                set +e
                mkdir -p "${PYTEST_REPORT_DIR}"
                docker compose ps > "${PYTEST_REPORT_DIR}/docker-compose-ps.txt"
                docker compose logs --no-color > "${PYTEST_REPORT_DIR}/docker-compose.log"
            '''

            junit allowEmptyResults: true, testResults: 'reports/*.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true

            script {
                if (!params.KEEP_STACK_UP) {
                    sh '''
                        #!/bin/bash
                        set +e
                        docker compose down -v
                    '''
                } else {
                    echo 'KEEP_STACK_UP=true, leaving Docker Compose services running for troubleshooting.'
                }
            }
        }
    }
}
