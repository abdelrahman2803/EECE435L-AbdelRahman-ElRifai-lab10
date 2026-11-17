# Lab 10 Jenkins CI/CD for Python

**Student:** Abdel Rahman El Rifai  
**Course:** EECE435L

This project uses Jenkins to check, test, measure coverage, scan, and locally
deploy a Python greeting application on Windows.

## Application

Running `python app.py` prints:

```text
Hello, World from Abdel Rahman El Rifai!
```

## Run locally

Use Command Prompt in the project folder with Python and Git installed:

```bat
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m flake8 app.py deploy.py tests
venv\Scripts\python.exe -m pytest -v --junitxml=reports/tests.xml
venv\Scripts\python.exe -m coverage run -m pytest -v
venv\Scripts\python.exe -m coverage report
venv\Scripts\python.exe -m bandit app.py deploy.py
```

## Jenkins configuration

1. Run Jenkins with Java 21 and complete initial setup.
2. Install Git, Pipeline, SSH Agent, Workspace Cleanup, and Pipeline: Stage View.
   JUnit is also required to publish test results and is a Pipeline dependency.
3. Create a **Pipeline** job named **Python-CI-CD**.
4. Choose **Pipeline script from SCM**, then **Git**.
5. Repository URL:
   `https://github.com/abdelrahman2803/EECE435L-AbdelRahman-ElRifai-lab10.git`
6. Branch: `*/main`.
7. Script Path: `Jenkinsfile_Abdel_Rahman_El_Rifai`.
8. Save and click **Build Now**. Subsequent builds expose parameters for the
   Python executable and the deployment directory. Their defaults target the
   Windows lab machine; change them when using a different machine.

## Pipeline stages

| Stage | Action | Failure condition |
| --- | --- | --- |
| Setup | Create `venv` and install pinned tools | Environment or installation error |
| Lint | Check application, deployment script, and tests with flake8 | Any lint violation |
| Test | Run three unit tests and publish JUnit XML | Any failed test |
| Coverage | Measure application statement and branch coverage; save XML, HTML, and text | Coverage below 100% |
| Security Scan | Scan `app.py` and `deploy.py` with Bandit; save JSON | Any reported finding |
| Deploy | Copy `app.py` into a release directory and execute smoke checks | Incorrect greeting or execution failure |

All reports are archived before workspace cleanup. Coverage measures `app.py`;
it does not claim coverage of the deployment script. Bandit results describe
static checks of the two production scripts, not a guarantee of security.

## Local deployment

The pipeline writes to the `DEPLOY_DIR` parameter, outside the Jenkins workspace:

```text
deployment/
  current.json
  releases/
    <build number>/
      app.py
      manifest.json
```

Each manifest records the build number, UTC timestamp, file hash, greeting, and
smoke-test result. Old releases remain available. `current.json` is updated only
after the greeting check succeeds. The pipeline also executes the copied script.
This is a local deployment of a command-line application; no web server or SSH
server is needed. SSH Agent is installed to satisfy Part 1 of the lab.

## Corrections to the supplied sample

- The greeting and expected test output both include the student's name.
- Dependencies include pytest, coverage, and Bandit as well as flake8.
- Windows `bat` steps call the virtual environment's Python directly.
- Deployment performs a real copy and verification instead of only an echo.
- JUnit and report archiving run before `cleanWs()` removes the workspace.

## References

- https://www.jenkins.io/doc/book/installing/war-file/
- https://www.jenkins.io/doc/book/pipeline/syntax/
- https://coverage.readthedocs.io/
- https://bandit.readthedocs.io/
