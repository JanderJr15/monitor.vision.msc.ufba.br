pipeline {
    agent {
        kubernetes {
            inheritFrom 'arguspod'
            defaultContainer 'agent'
        }
    }
    triggers {
        githubPush()
    }
    stages {
        stage('Install Poetry') {
            steps {
                sh 'pipx install poetry'
            }
        }

        stage('Install Python dependencies') {
            steps {
                sh 'poetry install'
            }
        }

        stage('Run TEMPY'){
            steps{
                sh 'poetry run python tests/test_smell_tempy_cli/main_final_version.py tests/unit'
                archiveArtifacts artifacts: 'tests/test_smell_tempy_cli/report/test_smell_report_web_page.html, tests/test_smell_tempy_cli/report/test_smell_csv_log.csv'
            }
        }

        stage('Run Pytest-cov'){
            steps{
                sh 'poetry run pytest --cov=vision --cov-report json:tests/unit/cov_report/report_cov.json' 
                archiveArtifacts artifacts: 'tests/unit/cov_report/report_cov.json'
            }
        }

        stage('Code Verification') {
            failFast false
            parallel {
                stage('Run MyPy') {
                    steps {
                        sh 'poetry run mypy vision'
                        sh 'poetry run mypy test'
                    }
                }

                stage('Run PyLint') {
                    steps {
                        sh 'poetry run pylint vision'
                        sh 'poetry run pylint test'
                    }
                }
            }
        }

        stage('Run pdoc') {
            steps {
                sh 'poetry run pdoc --output-dir docs vision'
            }
        }
    }
    post {
        always {
            script {
                def buildResult = currentBuild.result ?: 'SUCCESS'
                def descriptionMessage = buildResult == 'SUCCESS' ? 
                    "Jenkins Pipeline Build succeeded" : 
                    "Jenkins Pipeline Build failed"
                discordSend(
                    description: descriptionMessage,
                    footer: "Módulo de visão",
                    link: env.BUILD_URL,
                    result: buildResult,
                    title: JOB_NAME,
                    webhookURL: "https://discord.com/api/webhooks/1258471856223289375/fgoq-5SUcC10g1xCuIBevBT-MIZFdNh6vY9AyBm9ZkhSjbGiAXmCwNxQsQzZpUB5Kh0u"
                )
            }
        }
    }
}

