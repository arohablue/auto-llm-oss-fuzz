"""Templates of base python project files"""


DOCKERFILE_PYTHON = """
FROM gcr.io/oss-fuzz-base/base-builder-python
RUN apt-get update && apt-get install -y make autoconf automake libtool
RUN git clone --depth 1 {TARGET_REPO} {PROJECT_NAME}
WORKDIR {PROJECT_NAME}
COPY build.sh *.py $SRC/
"""


BUILD_PYTHON_BASE = """
#!/bin/bash -eu

# Generalized Build Script for Python OSS-Fuzz Projects
# Licensed under the Apache License, Version 2.0

# Install project dependencies
pip3 install --upgrade pip
pip3 install .

# Enable optional sanitizer-specific configurations
if [ "$SANITIZER" = "address" ]; then
  export ENABLE_PYSECSAN="1"
fi

# Optional: Set up additional environment variables or flags
export ORIG_CFLAGS="$CFLAGS"
export ORIG_CXXFLAGS="$CXXFLAGS"
export CFLAGS=""
export CXXFLAGS=""

# Install additional dependencies if required (example: numpy, tf-nightly, etc.)
# Uncomment and modify as needed:
# python3 -m pip install numpy
# python3 -m pip install tf-nightly-cpu

# Restore original flags after dependency installation
export CFLAGS=$ORIG_CFLAGS
export CXXFLAGS=$ORIG_CXXFLAGS

# Build fuzzers in $OUT directory
for fuzzer in $(find $SRC -name 'fuzz_*.py'); do
  compile_python_fuzzer $fuzzer
done

# Optional: Handle seed corpus creation if applicable
if [ -d "$SRC/tests" ]; then
  zip -rj $OUT/seed_corpus.zip $SRC/tests/*
fi

# Optional: Handle dictionary creation if applicable
if [ -f "$SRC/fuzzing/dictionaries/example.dict" ]; then
  cp $SRC/fuzzing/dictionaries/example.dict $OUT/fuzzer_example.dict
fi

# Clean up or finalize build steps if necessary (e.g., file renaming)

"""


YAML_PYTHON= """homepage: https://github.com/google/oss-fuzz-gen
main_repo: {TARGET_REPO}
language: python
fuzzing_engines:
- libfuzzer
sanitizers:
- address
primary_contacts: amit42308@gmail.com
"""

FUZZER_PYTHON = """import com.code_intelligence.jazzer.api.FuzzedDataProvider;

public class Fuzz {
  public static void fuzzerInitialize() {
  }

  public static void fuzzerTearDown() {
  }

  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
  }
}
"""
