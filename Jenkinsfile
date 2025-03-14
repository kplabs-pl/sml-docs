@Library('oryx-jpl') _

pipeline {
    agent { label 'sml-build' }
    options {
        ansiColor('xterm')
        checkoutToSubdirectory 'src'
    }
    stages {
        stage('Check quality') {
            steps {
                dir('src') {
                    withPipxInstalled('3.12', ['hatch==1.12.0']) {
                        runCommand('hatch env prune')
                        runCommand('hatch run dev:check')
                    }
                }
            }
        }
        stage('Build') {
            steps {
                dir('src/build') {
                    deleteDir()
                }
                dir('src') {
                    withPipxInstalled('3.12', ['hatch==1.12.0']) {
                        runCommand('hatch run dev:build -W -a -E')
                    }
                }
            }
            post {
                success {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: false,
                        reportDir: 'src/build/html',
                        reportFiles: 'index.html',
                        reportName: 'Docs',
                        reportTitles: '',
                        useWrapperFileDirectly: true
                    ])
                }
            }
        }
    }
}
