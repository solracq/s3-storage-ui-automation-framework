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
        booleanParam(
            name: 'SEND_FAILURE_EMAIL',
            defaultValue: false,
            description: 'Send email notifications for unstable or failed runs.',
        )
        string(
            name: 'EMAIL_RECIPIENTS',
            defaultValue: '',
            description: 'Comma-separated email recipients for unstable or failed build notifications.',
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
                script {
                    env.PORTAL_CHROME_BINARY = sh(
                        script: '''
                            #!/bin/bash
                            set -euo pipefail

                            if command -v google-chrome >/dev/null 2>&1; then
                              command -v google-chrome
                            elif command -v google-chrome-stable >/dev/null 2>&1; then
                              command -v google-chrome-stable
                            elif command -v chromium-browser >/dev/null 2>&1; then
                              command -v chromium-browser
                            elif command -v chromium >/dev/null 2>&1; then
                              command -v chromium
                            elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
                              echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                            elif [ -x "/Applications/Chromium.app/Contents/MacOS/Chromium" ]; then
                              echo "/Applications/Chromium.app/Contents/MacOS/Chromium"
                            else
                              echo "Chrome or Chromium must be installed on the Jenkins agent." >&2
                              exit 1
                            fi
                        ''',
                        returnStdout: true,
                    ).trim()
                }

                sh '''
                    #!/bin/bash
                    set -euo pipefail

                    python3 --version
                    docker --version
                    docker compose version
                    echo "Using browser binary: ${PORTAL_CHROME_BINARY}"
                    "${PORTAL_CHROME_BINARY}" --version
                '''
            }
        }

        // `docker compose up -d --build` already builds the app image before starting the stack.
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

        stage('Run Smoke Tests') {
            when {
                expression {
                    params.TEST_SUITE in ['smoke', 'all-ui']
                }
            }
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    mkdir -p "${PYTEST_REPORT_DIR}"
                    "${PYTEST_VENV}/bin/python" -m pytest tests/smoke -m smoke -vv -s \
                      --junitxml="${PYTEST_REPORT_DIR}/pytest-smoke.xml"
                '''
            }
        }

        stage('Run Usability Regression Tests') {
            when {
                expression {
                    params.TEST_SUITE in ['usability', 'all-regression', 'all-ui']
                }
            }
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    mkdir -p "${PYTEST_REPORT_DIR}"
                    "${PYTEST_VENV}/bin/python" -m pytest \
                      tests/regression/test_usability_regression.py -m usability -vv -s \
                      --junitxml="${PYTEST_REPORT_DIR}/pytest-usability.xml"
                '''
            }
        }

        stage('Run Negative Regression Tests') {
            when {
                expression {
                    params.TEST_SUITE in ['negative', 'all-regression', 'all-ui']
                }
            }
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    mkdir -p "${PYTEST_REPORT_DIR}"
                    "${PYTEST_VENV}/bin/python" -m pytest \
                      tests/regression/test_negative_regression.py -m negative -vv -s \
                      --junitxml="${PYTEST_REPORT_DIR}/pytest-negative.xml"
                '''
            }
        }

        stage('Run Edge Regression Tests') {
            when {
                expression {
                    params.TEST_SUITE in ['edge', 'all-regression', 'all-ui']
                }
            }
            steps {
                sh '''
                    #!/bin/bash
                    set -euo pipefail
                    mkdir -p "${PYTEST_REPORT_DIR}"
                    "${PYTEST_VENV}/bin/python" -m pytest \
                      tests/regression/test_edge_regression.py -m edge -vv -s \
                      --junitxml="${PYTEST_REPORT_DIR}/pytest-edge.xml"
                '''
            }
        }

        stage('Run Authentication Tests') {
            when {
                expression {
                    params.TEST_SUITE in ['authentication', 'all-regression', 'all-ui']
                }
            }
            steps {
                script {
                    if (params.TEST_SUITE == 'authentication') {
                        sh '''
                            #!/bin/bash
                            set -euo pipefail
                            mkdir -p "${PYTEST_REPORT_DIR}"
                            "${PYTEST_VENV}/bin/python" -m pytest \
                              tests/smoke/test_curated_smoke_scenarios.py \
                              tests/regression/test_authentication_regression.py \
                              -m authentication -vv -s \
                              --junitxml="${PYTEST_REPORT_DIR}/pytest-authentication.xml"
                        '''
                    } else {
                        sh '''
                            #!/bin/bash
                            set -euo pipefail
                            mkdir -p "${PYTEST_REPORT_DIR}"
                            "${PYTEST_VENV}/bin/python" -m pytest \
                              tests/regression/test_authentication_regression.py \
                              -m authentication -vv -s \
                              --junitxml="${PYTEST_REPORT_DIR}/pytest-authentication.xml"
                        '''
                    }
                }
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
                find "${PYTEST_REPORT_DIR}" -type f | LC_ALL=C sort > "${PYTEST_REPORT_DIR}/artifact-manifest.txt"
            '''

            junit allowEmptyResults: true, keepLongStdio: true, testResults: 'reports/*.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true, fingerprint: true
        }

        success {
            echo 'UI test stages completed successfully. JUnit reports and archived artifacts are available on this build.'
        }

        unstable {
            script {
                if (params.SEND_FAILURE_EMAIL && params.EMAIL_RECIPIENTS?.trim()) {
                    mail(
                        to: params.EMAIL_RECIPIENTS.trim(),
                        subject: "[${env.JOB_NAME}] UNSTABLE: Build #${env.BUILD_NUMBER}",
                        body: """Jenkins build notification

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status: UNSTABLE
Build URL: ${env.BUILD_URL}
Test Report: ${env.BUILD_URL}testReport/
Artifacts: ${env.BUILD_URL}artifact/

One or more test stages completed with unstable results. Please review Stage View, test reports, and archived artifacts.
""",
                    )
                }
            }
        }

        failure {
            script {
                if (params.SEND_FAILURE_EMAIL && params.EMAIL_RECIPIENTS?.trim()) {
                    mail(
                        to: params.EMAIL_RECIPIENTS.trim(),
                        subject: "[${env.JOB_NAME}] FAILED: Build #${env.BUILD_NUMBER}",
                        body: """Jenkins build notification

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status: FAILED
Build URL: ${env.BUILD_URL}
Test Report: ${env.BUILD_URL}testReport/
Artifacts: ${env.BUILD_URL}artifact/

One or more stages failed. Please review Stage View, console logs, test reports, and archived artifacts.
""",
                    )
                }
            }
        }

        unsuccessful {
            echo 'One or more UI test stages failed. Review Stage View, test reports, and archived artifacts for details.'
        }

        cleanup {
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
