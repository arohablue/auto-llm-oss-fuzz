# auto-llm-oss-fuzz

`auto-llm-oss-fuzz` is a repository dedicated to automated fuzz testing of open-source projects using large language models (LLMs). The project is structured to support fuzzing across multiple programming languages, including C++, Python, Java (JVM), and manual fuzzing setups.

## Overview

This repository integrates with Google's OSS-Fuzz to enhance security testing by identifying crashes, undefined behavior, and security vulnerabilities in software components. The repository is structured to accommodate different fuzzing environments tailored for specific programming languages.


## Getting Started

### Prerequisites

To use this repository effectively, you should have the following installed:

- Docker
- Google’s OSS-Fuzz environment (optional but recommended)
- Compilers and interpreters for the target languages (GCC, JDK, Python, etc.)

### Setting Up and Running Fuzzing Targets

Each fuzzing target follows a similar setup process. Navigate to the desired language-specific directory and use the provided specific instructions.

Example for JVM:

```sh
# Prepare
# Vertex: Follow the steps at:
# https://github.com/google/oss-fuzz-gen/blob/main/USAGE.md#vertex-ai
export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_CREDS_FILE

# ChatGPT:
export OPENAI_API_KEY=your-api-key

# Prepare folder and set current working directory
git clone https://github.com/google/oss-fuzz-gen
cd oss-fuzz-gen/experimental/jvm

# Run end-to-end generation:
# 1) Create an OSS-Fuzz project
# 2) Extract additional harnesses using OSS-Fuzz-gen
MODEL=gpt-3.5-turbo TARGETS=https://github.com/jdereg/java-util ./run_e2e.sh

# You now have an auto-generated OSS-Fuzz project in workdir/auto-generated-projects
ls workdir/auto-generated-projects/
java-util

# Build the project using the OSS-Fuzz CLI
cd workdir/oss-fuzz
cp -rf ../auto-generated-projects/java-util projects/java-util
python3 infra/helper.py build_fuzzers java-util
```


## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for details.


