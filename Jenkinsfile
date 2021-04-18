Jenkinsfile (Declarative Pipeline)
pipeline{
    agent any
    stages {

        stage('build') {
            when {
                branch 'Docker'
            }
            steps {
                python ./Cloud-Computations/Unit_tests/tests.py
                sh 'test_deploy.sh'

            }
        }

    }




}