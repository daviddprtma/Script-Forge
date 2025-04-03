├── .github
    └── workflows
    │   ├── build_documentation.yml
    │   ├── build_pr_documentation.yml
    │   ├── quality.yml
    │   └── upload_pr_documentation.yml
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── docs
    ├── README.md
    └── source
    │   └── en
    │       ├── _config.py
    │       ├── _toctree.yml
    │       ├── conceptual_guides
    │           ├── intro_agents.md
    │           └── react.md
    │       ├── examples
    │           ├── multiagents.md
    │           ├── rag.md
    │           └── text_to_sql.md
    │       ├── guided_tour.md
    │       ├── index.md
    │       ├── reference
    │           ├── agents.md
    │           └── tools.md
    │       └── tutorials
    │           ├── building_good_agents.md
    │           ├── secure_code_execution.md
    │           └── tools.md
├── e2b.Dockerfile
├── e2b.toml
├── examples
    ├── benchmark.ipynb
    ├── e2b_example.py
    ├── rag.py
    ├── text_to_sql.py
    ├── tool_calling_agent_from_any_llm.py
    └── tool_calling_agent_ollama.py
├── package-lock.json
├── package.json
├── pyproject.toml
├── server.py
├── src
    └── smolagents
    │   ├── __init__.py
    │   ├── agents.py
    │   ├── default_tools.py
    │   ├── e2b_executor.py
    │   ├── gradio_ui.py
    │   ├── local_python_executor.py
    │   ├── models.py
    │   ├── monitoring.py
    │   ├── prompts.py
    │   ├── tool_validation.py
    │   ├── tools.py
    │   ├── types.py
    │   └── utils.py
└── tests
    ├── __init__.py
    ├── fixtures
        └── 000000039769.png
    ├── test_agents.py
    ├── test_all_docs.py
    ├── test_final_answer.py
    ├── test_models.py
    ├── test_monitoring.py
    ├── test_python_interpreter.py
    ├── test_search.py
    ├── test_tools.py
    ├── test_types.py
    └── test_utils.py


/.github/workflows/build_documentation.yml:
--------------------------------------------------------------------------------
 1 | name: Build documentation
 2 | 
 3 | on:
 4 |   push:
 5 |     branches:
 6 |       - main
 7 |       - doc-builder*
 8 |       - v*-release
 9 |       - use_templates
10 |     paths:
11 |       - 'docs/source/**'
12 |       - 'assets/**'
13 |       - '.github/workflows/doc-build.yml'
14 | 
15 | jobs:
16 |    build:
17 |     uses: huggingface/doc-builder/.github/workflows/build_main_documentation.yml@main
18 |     with:
19 |       commit_sha: ${{ github.sha }}
20 |       package: smolagents
21 |       languages: en
22 |       # additional_args: --not_python_module # use this arg if repository is documentation only
23 |     secrets:
24 |       token: ${{ secrets.HUGGINGFACE_PUSH }}
25 |       hf_token: ${{ secrets.HF_DOC_BUILD_PUSH }}


--------------------------------------------------------------------------------
/.github/workflows/build_pr_documentation.yml:
--------------------------------------------------------------------------------
 1 | name: Build PR Documentation
 2 | 
 3 | on:
 4 |   pull_request:
 5 |     paths:
 6 |       - 'docs/source/**'
 7 |       - 'assets/**'
 8 |       - '.github/workflows/doc-pr-build.yml'
 9 | 
10 | concurrency:
11 |   group: ${{ github.workflow }}-${{ github.head_ref || github.run_id }}
12 |   cancel-in-progress: true
13 | 
14 | jobs:
15 |   build:
16 |     uses: huggingface/doc-builder/.github/workflows/build_pr_documentation.yml@main
17 |     with:
18 |       commit_sha: ${{ github.event.pull_request.head.sha }}
19 |       pr_number: ${{ github.event.number }}
20 |       package: smolagents
21 |       languages: en
22 |       # additional_args: --not_python_module # use this arg if repository is documentation only


--------------------------------------------------------------------------------
/.github/workflows/quality.yml:
--------------------------------------------------------------------------------
 1 | name: Quality Check
 2 | 
 3 | on: [pull_request]
 4 | 
 5 | jobs:
 6 |   quality:
 7 |     runs-on: ubuntu-latest
 8 |     steps:
 9 |     - uses: actions/checkout@v3.1.0
10 |     - name: Set up Python 3.9
11 |       uses: actions/setup-python@v3
12 |       with:
13 |         python-version: 3.10
14 |         cache: 'pip'
15 |         cache-dependency-path: 'setup.py'
16 |     - name: Install Python dependencies
17 |       run: pip install -e .[quality]
18 |     - name: Run Quality check
19 |       run: make quality
20 |     - name: Check if failure
21 |       if: ${{ failure() }}
22 |       run: |
23 |         echo "Quality check failed. Please ensure the right dependency versions are installed with 'pip install -e .[quality]' and rerun 'make style; make quality;'" >> $GITHUB_STEP_SUMMARY


--------------------------------------------------------------------------------
/.github/workflows/upload_pr_documentation.yml:
--------------------------------------------------------------------------------
 1 | name: Upload PR Documentation
 2 | 
 3 | on:
 4 |   workflow_run:
 5 |     workflows: ["Build PR Documentation"]
 6 |     types:
 7 |       - completed
 8 | 
 9 | jobs:
10 |   build:
11 |     uses: huggingface/doc-builder/.github/workflows/upload_pr_documentation.yml@main
12 |     with:
13 |       package_name: smolagents
14 |     secrets:
15 |       hf_token: ${{ secrets.HF_DOC_BUILD_PUSH }}
16 |       comment_bot_token: ${{ secrets.COMMENT_BOT_TOKEN }}


--------------------------------------------------------------------------------
/.gitignore:
--------------------------------------------------------------------------------
  1 | # Logging
  2 | logs
  3 | tmp
  4 | wandb
  5 | 
  6 | # Data
  7 | data
  8 | outputs
  9 | 
 10 | # Apple
 11 | .DS_Store
 12 | 
 13 | # VS Code
 14 | .vscode
 15 | 
 16 | # Byte-compiled / optimized / DLL files
 17 | __pycache__/
 18 | *.py[cod]
 19 | *$py.class
 20 | 
 21 | # C extensions
 22 | *.so
 23 | 
 24 | # Distribution / packaging
 25 | .Python
 26 | build/
 27 | develop-eggs/
 28 | dist/
 29 | downloads/
 30 | eggs/
 31 | .eggs/
 32 | lib/
 33 | lib64/
 34 | parts/
 35 | sdist/
 36 | var/
 37 | wheels/
 38 | share/python-wheels/
 39 | node_modules/
 40 | *.egg-info/
 41 | .installed.cfg
 42 | *.egg
 43 | MANIFEST
 44 | 
 45 | # PyInstaller
 46 | *.manifest
 47 | *.spec
 48 | 
 49 | # Installer logs
 50 | pip-log.txt
 51 | pip-delete-this-directory.txt
 52 | 
 53 | # Unit test / coverage reports
 54 | htmlcov/
 55 | .tox/
 56 | .nox/
 57 | .coverage
 58 | .coverage.*
 59 | .cache
 60 | nosetests.xml
 61 | coverage.xml
 62 | *.cover
 63 | *.py,cover
 64 | .hypothesis/
 65 | .pytest_cache/
 66 | cover/
 67 | uv.lock
 68 | 
 69 | # Translations
 70 | *.mo
 71 | *.pot
 72 | 
 73 | # Sphinx documentation
 74 | docs/_build/
 75 | 
 76 | # PyBuilder
 77 | .pybuilder/
 78 | target/
 79 | 
 80 | # Jupyter Notebook
 81 | .ipynb_checkpoints
 82 | 
 83 | # IPython
 84 | profile_default/
 85 | ipython_config.py
 86 | 
 87 | # pyenv
 88 | # .python-version
 89 | 
 90 | # pipenv
 91 | #Pipfile.lock
 92 | 
 93 | # UV
 94 | #uv.lock
 95 | 
 96 | # poetry
 97 | #poetry.lock
 98 | 
 99 | # pdm
100 | .pdm.toml
101 | .pdm-python
102 | .pdm-build/
103 | 
104 | # PEP 582
105 | __pypackages__/
106 | 
107 | # Celery stuff
108 | celerybeat-schedule
109 | celerybeat.pid
110 | 
111 | # SageMath parsed files
112 | *.sage.py
113 | 
114 | # Environments
115 | .env
116 | .venv
117 | env/
118 | venv/
119 | ENV/
120 | env.bak/
121 | venv.bak/
122 | 
123 | 
124 | # mkdocs documentation
125 | /site
126 | 
127 | # mypy
128 | .mypy_cache/
129 | .dmypy.json
130 | dmypy.json
131 | 
132 | # Pyre type checker
133 | .pyre/
134 | 
135 | # pytype static type analyzer
136 | .pytype/
137 | 
138 | # Cython debug symbols
139 | cython_debug/
140 | 
141 | # PyCharm
142 | #.idea/
143 | 
144 | # Interpreter
145 | interpreter_workspace/
146 | 
147 | # Archive
148 | archive/
149 | savedir/
150 | output/
151 | tool_output/


--------------------------------------------------------------------------------
/.pre-commit-config.yaml:
--------------------------------------------------------------------------------
 1 | repos:
 2 |   - repo: https://github.com/astral-sh/ruff-pre-commit
 3 |     rev: v0.2.1
 4 |     hooks:
 5 |       - id: ruff
 6 |         args:
 7 |           - --fix
 8 |       - id: ruff-format
 9 |   - repo: https://github.com/pre-commit/pre-commit-hooks
10 |     rev: v4.5.0
11 |     hooks:
12 |       - id: check-merge-conflict
13 |       - id: check-yaml
14 | 


--------------------------------------------------------------------------------
/Dockerfile:
--------------------------------------------------------------------------------
 1 | # Base Python image
 2 | FROM python:3.12-slim
 3 | 
 4 | # Set working directory
 5 | WORKDIR /app
 6 | 
 7 | # Install build dependencies
 8 | RUN apt-get update && apt-get install -y \
 9 |     build-essential \
10 |     zlib1g-dev \
11 |     libjpeg-dev \
12 |     libpng-dev \
13 |     && rm -rf /var/lib/apt/lists/*
14 | 
15 | # Copy package files
16 | COPY . /app/
17 | 
18 | # Install dependencies
19 | RUN pip install --no-cache-dir -r requirements.txt
20 | 
21 | # Install the package
22 | RUN pip install -e .
23 | 
24 | COPY server.py /app/server.py
25 | 
26 | # Expose the port your server will run on
27 | EXPOSE 65432
28 | 
29 | CMD ["python", "/app/server.py"]
30 | 


--------------------------------------------------------------------------------
/LICENSE:
--------------------------------------------------------------------------------
  1 |                                  Apache License
  2 |                            Version 2.0, January 2004
  3 |                         http://www.apache.org/licenses/
  4 | 
  5 |    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
  6 | 
  7 |    1. Definitions.
  8 | 
  9 |       "License" shall mean the terms and conditions for use, reproduction,
 10 |       and distribution as defined by Sections 1 through 9 of this document.
 11 | 
 12 |       "Licensor" shall mean the copyright owner or entity authorized by
 13 |       the copyright owner that is granting the License.
 14 | 
 15 |       "Legal Entity" shall mean the union of the acting entity and all
 16 |       other entities that control, are controlled by, or are under common
 17 |       control with that entity. For the purposes of this definition,
 18 |       "control" means (i) the power, direct or indirect, to cause the
 19 |       direction or management of such entity, whether by contract or
 20 |       otherwise, or (ii) ownership of fifty percent (50%) or more of the
 21 |       outstanding shares, or (iii) beneficial ownership of such entity.
 22 | 
 23 |       "You" (or "Your") shall mean an individual or Legal Entity
 24 |       exercising permissions granted by this License.
 25 | 
 26 |       "Source" form shall mean the preferred form for making modifications,
 27 |       including but not limited to software source code, documentation
 28 |       source, and configuration files.
 29 | 
 30 |       "Object" form shall mean any form resulting from mechanical
 31 |       transformation or translation of a Source form, including but
 32 |       not limited to compiled object code, generated documentation,
 33 |       and conversions to other media types.
 34 | 
 35 |       "Work" shall mean the work of authorship, whether in Source or
 36 |       Object form, made available under the License, as indicated by a
 37 |       copyright notice that is included in or attached to the work
 38 |       (an example is provided in the Appendix below).
 39 | 
 40 |       "Derivative Works" shall mean any work, whether in Source or Object
 41 |       form, that is based on (or derived from) the Work and for which the
 42 |       editorial revisions, annotations, elaborations, or other modifications
 43 |       represent, as a whole, an original work of authorship. For the purposes
 44 |       of this License, Derivative Works shall not include works that remain
 45 |       separable from, or merely link (or bind by name) to the interfaces of,
 46 |       the Work and Derivative Works thereof.
 47 | 
 48 |       "Contribution" shall mean any work of authorship, including
 49 |       the original version of the Work and any modifications or additions
 50 |       to that Work or Derivative Works thereof, that is intentionally
 51 |       submitted to Licensor for inclusion in the Work by the copyright owner
 52 |       or by an individual or Legal Entity authorized to submit on behalf of
 53 |       the copyright owner. For the purposes of this definition, "submitted"
 54 |       means any form of electronic, verbal, or written communication sent
 55 |       to the Licensor or its representatives, including but not limited to
 56 |       communication on electronic mailing lists, source code control systems,
 57 |       and issue tracking systems that are managed by, or on behalf of, the
 58 |       Licensor for the purpose of discussing and improving the Work, but
 59 |       excluding communication that is conspicuously marked or otherwise
 60 |       designated in writing by the copyright owner as "Not a Contribution."
 61 | 
 62 |       "Contributor" shall mean Licensor and any individual or Legal Entity
 63 |       on behalf of whom a Contribution has been received by Licensor and
 64 |       subsequently incorporated within the Work.
 65 | 
 66 |    2. Grant of Copyright License. Subject to the terms and conditions of
 67 |       this License, each Contributor hereby grants to You a perpetual,
 68 |       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
 69 |       copyright license to reproduce, prepare Derivative Works of,
 70 |       publicly display, publicly perform, sublicense, and distribute the
 71 |       Work and such Derivative Works in Source or Object form.
 72 | 
 73 |    3. Grant of Patent License. Subject to the terms and conditions of
 74 |       this License, each Contributor hereby grants to You a perpetual,
 75 |       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
 76 |       (except as stated in this section) patent license to make, have made,
 77 |       use, offer to sell, sell, import, and otherwise transfer the Work,
 78 |       where such license applies only to those patent claims licensable
 79 |       by such Contributor that are necessarily infringed by their
 80 |       Contribution(s) alone or by combination of their Contribution(s)
 81 |       with the Work to which such Contribution(s) was submitted. If You
 82 |       institute patent litigation against any entity (including a
 83 |       cross-claim or counterclaim in a lawsuit) alleging that the Work
 84 |       or a Contribution incorporated within the Work constitutes direct
 85 |       or contributory patent infringement, then any patent licenses
 86 |       granted to You under this License for that Work shall terminate
 87 |       as of the date such litigation is filed.
 88 | 
 89 |    4. Redistribution. You may reproduce and distribute copies of the
 90 |       Work or Derivative Works thereof in any medium, with or without
 91 |       modifications, and in Source or Object form, provided that You
 92 |       meet the following conditions:
 93 | 
 94 |       (a) You must give any other recipients of the Work or
 95 |           Derivative Works a copy of this License; and
 96 | 
 97 |       (b) You must cause any modified files to carry prominent notices
 98 |           stating that You changed the files; and
 99 | 
100 |       (c) You must retain, in the Source form of any Derivative Works
101 |           that You distribute, all copyright, patent, trademark, and
102 |           attribution notices from the Source form of the Work,
103 |           excluding those notices that do not pertain to any part of
104 |           the Derivative Works; and
105 | 
106 |       (d) If the Work includes a "NOTICE" text file as part of its
107 |           distribution, then any Derivative Works that You distribute must
108 |           include a readable copy of the attribution notices contained
109 |           within such NOTICE file, excluding those notices that do not
110 |           pertain to any part of the Derivative Works, in at least one
111 |           of the following places: within a NOTICE text file distributed
112 |           as part of the Derivative Works; within the Source form or
113 |           documentation, if provided along with the Derivative Works; or,
114 |           within a display generated by the Derivative Works, if and
115 |           wherever such third-party notices normally appear. The contents
116 |           of the NOTICE file are for informational purposes only and
117 |           do not modify the License. You may add Your own attribution
118 |           notices within Derivative Works that You distribute, alongside
119 |           or as an addendum to the NOTICE text from the Work, provided
120 |           that such additional attribution notices cannot be construed
121 |           as modifying the License.
122 | 
123 |       You may add Your own copyright statement to Your modifications and
124 |       may provide additional or different license terms and conditions
125 |       for use, reproduction, or distribution of Your modifications, or
126 |       for any such Derivative Works as a whole, provided Your use,
127 |       reproduction, and distribution of the Work otherwise complies with
128 |       the conditions stated in this License.
129 | 
130 |    5. Submission of Contributions. Unless You explicitly state otherwise,
131 |       any Contribution intentionally submitted for inclusion in the Work
132 |       by You to the Licensor shall be under the terms and conditions of
133 |       this License, without any additional terms or conditions.
134 |       Notwithstanding the above, nothing herein shall supersede or modify
135 |       the terms of any separate license agreement you may have executed
136 |       with Licensor regarding such Contributions.
137 | 
138 |    6. Trademarks. This License does not grant permission to use the trade
139 |       names, trademarks, service marks, or product names of the Licensor,
140 |       except as required for reasonable and customary use in describing the
141 |       origin of the Work and reproducing the content of the NOTICE file.
142 | 
143 |    7. Disclaimer of Warranty. Unless required by applicable law or
144 |       agreed to in writing, Licensor provides the Work (and each
145 |       Contributor provides its Contributions) on an "AS IS" BASIS,
146 |       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
147 |       implied, including, without limitation, any warranties or conditions
148 |       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
149 |       PARTICULAR PURPOSE. You are solely responsible for determining the
150 |       appropriateness of using or redistributing the Work and assume any
151 |       risks associated with Your exercise of permissions under this License.
152 | 
153 |    8. Limitation of Liability. In no event and under no legal theory,
154 |       whether in tort (including negligence), contract, or otherwise,
155 |       unless required by applicable law (such as deliberate and grossly
156 |       negligent acts) or agreed to in writing, shall any Contributor be
157 |       liable to You for damages, including any direct, indirect, special,
158 |       incidental, or consequential damages of any character arising as a
159 |       result of this License or out of the use or inability to use the
160 |       Work (including but not limited to damages for loss of goodwill,
161 |       work stoppage, computer failure or malfunction, or any and all
162 |       other commercial damages or losses), even if such Contributor
163 |       has been advised of the possibility of such damages.
164 | 
165 |    9. Accepting Warranty or Additional Liability. While redistributing
166 |       the Work or Derivative Works thereof, You may choose to offer,
167 |       and charge a fee for, acceptance of support, warranty, indemnity,
168 |       or other liability obligations and/or rights consistent with this
169 |       License. However, in accepting such obligations, You may act only
170 |       on Your own behalf and on Your sole responsibility, not on behalf
171 |       of any other Contributor, and only if You agree to indemnify,
172 |       defend, and hold each Contributor harmless for any liability
173 |       incurred by, or claims asserted against, such Contributor by reason
174 |       of your accepting any such warranty or additional liability.
175 | 
176 |    END OF TERMS AND CONDITIONS
177 | 
178 |    APPENDIX: How to apply the Apache License to your work.
179 | 
180 |       To apply the Apache License to your work, attach the following
181 |       boilerplate notice, with the fields enclosed by brackets "[]"
182 |       replaced with your own identifying information. (Don't include
183 |       the brackets!)  The text should be enclosed in the appropriate
184 |       comment syntax for the file format. We also recommend that a
185 |       file or class name and description of purpose be included on the
186 |       same "printed page" as the copyright notice for easier
187 |       identification within third-party archives.
188 | 
189 |    Copyright [yyyy] [name of copyright owner]
190 | 
191 |    Licensed under the Apache License, Version 2.0 (the "License");
192 |    you may not use this file except in compliance with the License.
193 |    You may obtain a copy of the License at
194 | 
195 |        http://www.apache.org/licenses/LICENSE-2.0
196 | 
197 |    Unless required by applicable law or agreed to in writing, software
198 |    distributed under the License is distributed on an "AS IS" BASIS,
199 |    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
200 |    See the License for the specific language governing permissions and
201 |    limitations under the License.
202 | 


--------------------------------------------------------------------------------
/Makefile:
--------------------------------------------------------------------------------
 1 | .PHONY: quality style test docs utils
 2 | 
 3 | check_dirs := .
 4 | 
 5 | # Check that source code meets quality standards
 6 | 
 7 | extra_quality_checks:
 8 | 	python utils/check_copies.py
 9 | 	python utils/check_dummies.py
10 | 	python utils/check_repo.py
11 | 	doc-builder style smolagents docs/source --max_len 119
12 | 
13 | # this target runs checks on all files
14 | quality:
15 | 	ruff check $(check_dirs)
16 | 	ruff format --check $(check_dirs)
17 | 	doc-builder style smolagents docs/source --max_len 119 --check_only
18 | 
19 | # Format source code automatically and check is there are any problems left that need manual fixing
20 | style:
21 | 	ruff check $(check_dirs) --fix
22 | 	ruff format $(check_dirs)
23 | 	doc-builder style smolagents docs/source --max_len 119
24 | 	
25 | # Run tests for the library
26 | test_big_modeling:
27 | 	python -m pytest -s -v ./tests/test_big_modeling.py ./tests/test_modeling_utils.py $(if $(IS_GITHUB_CI),--report-log "$(PYTORCH_VERSION)_big_modeling.log",)
28 | 
29 | test_core:
30 | 	python -m pytest -s -v ./tests/ --ignore=./tests/test_examples.py $(if $(IS_GITHUB_CI),--report-log "$(PYTORCH_VERSION)_core.log",)
31 | 
32 | test_cli:
33 | 	python -m pytest -s -v ./tests/test_cli.py $(if $(IS_GITHUB_CI),--report-log "$(PYTORCH_VERSION)_cli.log",)
34 | 
35 | 
36 | # Since the new version of pytest will *change* how things are collected, we need `deepspeed` to 
37 | # run after test_core and test_cli
38 | test:
39 | 	$(MAKE) test_core
40 | 	$(MAKE) test_cli
41 | 	$(MAKE) test_big_modeling
42 | 	$(MAKE) test_deepspeed
43 | 	$(MAKE) test_fsdp
44 | 
45 | test_examples:
46 | 	python -m pytest -s -v ./tests/test_examples.py $(if $(IS_GITHUB_CI),--report-log "$(PYTORCH_VERSION)_examples.log",)
47 | 
48 | # Same as test but used to install only the base dependencies
49 | test_prod:
50 | 	$(MAKE) test_core
51 | 
52 | test_rest:
53 | 	python -m pytest -s -v ./tests/test_examples.py::FeatureExamplesTests $(if $(IS_GITHUB_CI),--report-log "$(PYTORCH_VERSION)_rest.log",)
54 | 


--------------------------------------------------------------------------------
/README.md:
--------------------------------------------------------------------------------
 1 | <!---
 2 | Copyright 2024 The HuggingFace Team. All rights reserved.
 3 | 
 4 | Licensed under the Apache License, Version 2.0 (the "License");
 5 | you may not use this file except in compliance with the License.
 6 | You may obtain a copy of the License at
 7 | 
 8 |     http://www.apache.org/licenses/LICENSE-2.0
 9 | 
10 | Unless required by applicable law or agreed to in writing, software
11 | distributed under the License is distributed on an "AS IS" BASIS,
12 | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
13 | See the License for the specific language governing permissions and
14 | limitations under the License.
15 | -->
16 | <p align="center">
17 |     <!-- Uncomment when CircleCI is set up
18 |     <a href="https://circleci.com/gh/huggingface/accelerate"><img alt="Build" src="https://img.shields.io/circleci/build/github/huggingface/transformers/master"></a>
19 |     -->
20 |     <a href="https://github.com/huggingface/smolagents/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/huggingface/smolagents.svg?color=blue"></a>
21 |     <a href="https://huggingface.co/docs/smolagents/index.html"><img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/smolagents/index.html.svg?down_color=red&down_message=offline&up_message=online"></a>
22 |     <a href="https://github.com/huggingface/smolagents/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/smolagents.svg"></a>
23 |     <a href="https://github.com/huggingface/smolagents/blob/main/CODE_OF_CONDUCT.md"><img alt="Contributor Covenant" src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg"></a>
24 | </p>
25 | 
26 | <h3 align="center">
27 |   <p>🤗 smolagents - a smol library to build great agents!</p>
28 | </h3>
29 | 
30 | `smolagents` is a library that enables you to run powerful agents in a few lines of code. It offers:
31 | 
32 | ✨ **Simplicity**: the logic for agents fits in ~thousand lines of code (see [agents.py](https://github.com/huggingface/smolagents/blob/main/src/smolagents/agents.py)). We kept abstractions to their minimal shape above raw code!
33 | 
34 | 🧑‍💻 **First-class support for Code Agents**, i.e. agents that write their actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via [E2B](https://e2b.dev/).
35 |  - On top of this [`CodeAgent`](https://huggingface.co/docs/smolagents/reference/agents#smolagents.CodeAgent) class, we still support the standard [`ToolCallingAgent`](https://huggingface.co/docs/smolagents/reference/agents#smolagents.ToolCallingAgent) that writes actions as JSON/text blobs.
36 | 
37 | 🤗 **Hub integrations**: you can share and load tools to/from the Hub, and more is to come!
38 | 
39 | 🌐 **Support for any LLM**: it supports models hosted on the Hub loaded in their `transformers` version or through our inference API, but also supports models from OpenAI, Anthropic and many others via our [LiteLLM](https://www.litellm.ai/) integration.
40 | 
41 | ## Quick demo
42 | 
43 | First install the package.
44 | ```bash
45 | pip install smolagents
46 | ```
47 | Then define your agent, give it the tools it needs and run it!
48 | ```py
49 | from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
50 | 
51 | agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())
52 | 
53 | agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")
54 | ```
55 | 
56 | https://github.com/user-attachments/assets/cd0226e2-7479-4102-aea0-57c22ca47884
57 | 
58 | ## Code agents?
59 | 
60 | In our `CodeAgent`,  the LLM engine writes its actions in code. This approach is demonstrated to work better than the current industry practice of letting the LLM output a dictionary of the tools it wants to calls: [uses 30% fewer steps](https://huggingface.co/papers/2402.01030) (thus 30% fewer LLM calls)
61 | and [reaches higher performance on difficult benchmarks](https://huggingface.co/papers/2411.01747). Head to [our high-level intro to agents](https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents) to learn more on that.
62 | 
63 | Especially, since code execution can be a security concern (arbitrary code execution!), we provide options at runtime:
64 |   - a secure python interpreter to run code more safely in your environment
65 |   - a sandboxed environment using [E2B](https://e2b.dev/).
66 | 
67 | ## How smol is it really?
68 | 
69 | We strived to keep abstractions to a strict minimum: the main code in `agents.py` is only ~1,000 lines of code.
70 | Still, we implement several types of agents: `CodeAgent` writes its actions as Python code snippets, and the more classic `ToolCallingAgent` leverages built-in tool calling methods.
71 | 
72 | By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework handles this complexity for you. But of course we still encourage you to hack into the source code and use only the bits that you need, to the exclusion of everything else!
73 | 
74 | ## How strong are open models for agentic workflows?
75 | 
76 | We've created [`CodeAgent`](https://huggingface.co/docs/smolagents/reference/agents#smolagents.CodeAgent) instances with some leading models, and compared them on [this benchmark](https://huggingface.co/datasets/m-ric/agents_medium_benchmark_2) that gathers questions from a few different benchmarks to propose a varied blend of challenges.
77 | 
78 | [Find the benchmarking code here](https://github.com/huggingface/smolagents/blob/main/examples/benchmark.ipynb) for more detail on the agentic setup used, and see a comparison of using LLMs code agents compared to vanilla (spoilers: code agents works better).
79 | 
80 | <p align="center">
81 |     <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/smolagents/benchmark_code_agents.png" alt="benchmark of different models on agentic workflows" width=70%>
82 | </p>
83 | 
84 | This comparison shows that open source models can now take on the best closed models!
85 | 
86 | ## Citing smolagents
87 | 
88 | If you use `smolagents` in your publication, please cite it by using the following BibTeX entry.
89 | 
90 | ```bibtex
91 | @Misc{smolagents,
92 |   title =        {`smolagents`: The easiest way to build efficient agentic systems.},
93 |   author =       {Aymeric Roucher and Thomas Wolf and Leandro von Werra and Erik Kaunismäki},
94 |   howpublished = {\url{https://github.com/huggingface/smolagents}},
95 |   year =         {2025}
96 | }
97 | ```
98 | 


--------------------------------------------------------------------------------
/docs/README.md:
--------------------------------------------------------------------------------
  1 | <!---
  2 | Copyright 2024 The HuggingFace Team. All rights reserved.
  3 | 
  4 | Licensed under the Apache License, Version 2.0 (the "License");
  5 | you may not use this file except in compliance with the License.
  6 | You may obtain a copy of the License at
  7 | 
  8 |     http://www.apache.org/licenses/LICENSE-2.0
  9 | 
 10 | Unless required by applicable law or agreed to in writing, software
 11 | distributed under the License is distributed on an "AS IS" BASIS,
 12 | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | See the License for the specific language governing permissions and
 14 | limitations under the License.
 15 | -->
 16 | 
 17 | # Generating the documentation
 18 | 
 19 | To generate the documentation, you have to build it. Several packages are necessary to build the doc.
 20 | 
 21 | First, you need to install the project itself by running the following command at the root of the code repository:
 22 | 
 23 | ```bash
 24 | pip install -e .
 25 | ```
 26 | 
 27 | You also need to install 2 extra packages:
 28 | 
 29 | ```bash
 30 | # `hf-doc-builder` to build the docs
 31 | pip install git+https://github.com/huggingface/doc-builder@main
 32 | # `watchdog` for live reloads
 33 | pip install watchdog
 34 | ```
 35 | 
 36 | ---
 37 | **NOTE**
 38 | 
 39 | You only need to generate the documentation to inspect it locally (if you're planning changes and want to
 40 | check how they look before committing for instance). You don't have to commit the built documentation.
 41 | 
 42 | ---
 43 | 
 44 | ## Building the documentation
 45 | 
 46 | Once you have setup the `doc-builder` and additional packages with the pip install command above,
 47 | you can generate the documentation by typing the following command:
 48 | 
 49 | ```bash
 50 | doc-builder build smolagents docs/source/en/ --build_dir ~/tmp/test-build
 51 | ```
 52 | 
 53 | You can adapt the `--build_dir` to set any temporary folder that you prefer. This command will create it and generate
 54 | the MDX files that will be rendered as the documentation on the main website. You can inspect them in your favorite
 55 | Markdown editor.
 56 | 
 57 | ## Previewing the documentation
 58 | 
 59 | To preview the docs, run the following command:
 60 | 
 61 | ```bash
 62 | doc-builder preview smolagents docs/source/en/
 63 | ```
 64 | 
 65 | The docs will be viewable at [http://localhost:5173](http://localhost:5173). You can also preview the docs once you
 66 | have opened a PR. You will see a bot add a comment to a link where the documentation with your changes lives.
 67 | 
 68 | ---
 69 | **NOTE**
 70 | 
 71 | The `preview` command only works with existing doc files. When you add a completely new file, you need to update
 72 | `_toctree.yml` & restart `preview` command (`ctrl-c` to stop it & call `doc-builder preview ...` again).
 73 | 
 74 | ---
 75 | 
 76 | ## Adding a new element to the navigation bar
 77 | 
 78 | Accepted files are Markdown (.md).
 79 | 
 80 | Create a file with its extension and put it in the source directory. You can then link it to the toc-tree by putting
 81 | the filename without the extension in the [`_toctree.yml`](https://github.com/huggingface/smolagents/blob/main/docs/source/_toctree.yml) file.
 82 | 
 83 | ## Renaming section headers and moving sections
 84 | 
 85 | It helps to keep the old links working when renaming the section header and/or moving sections from one document to another. This is because the old links are likely to be used in Issues, Forums, and Social media and it'd make for a much more superior user experience if users reading those months later could still easily navigate to the originally intended information.
 86 | 
 87 | Therefore, we simply keep a little map of moved sections at the end of the document where the original section was. The key is to preserve the original anchor.
 88 | 
 89 | So if you renamed a section from: "Section A" to "Section B", then you can add at the end of the file:
 90 | 
 91 | ```
 92 | Sections that were moved:
 93 | 
 94 | [ <a href="#section-b">Section A</a><a id="section-a"></a> ]
 95 | ```
 96 | and of course, if you moved it to another file, then:
 97 | 
 98 | ```
 99 | Sections that were moved:
100 | 
101 | [ <a href="../new-file#section-b">Section A</a><a id="section-a"></a> ]
102 | ```
103 | 
104 | Use the relative style to link to the new file so that the versioned docs continue to work.
105 | 
106 | For an example of a rich moved section set please see the very end of [the transformers Trainer doc](https://github.com/huggingface/transformers/blob/main/docs/source/en/main_classes/trainer.md).
107 | 
108 | 
109 | ## Writing Documentation - Specification
110 | 
111 | The `huggingface/smolagents` documentation follows the
112 | [Google documentation](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) style for docstrings,
113 | although we can write them directly in Markdown.
114 | 
115 | ### Adding a new tutorial
116 | 
117 | Adding a new tutorial or section is done in two steps:
118 | 
119 | - Add a new Markdown (.md) file under `./source`.
120 | - Link that file in `./source/_toctree.yml` on the correct toc-tree.
121 | 
122 | Make sure to put your new file under the proper section. If you have a doubt, feel free to ask in a Github Issue or PR.
123 | 
124 | ### Translating
125 | 
126 | When translating, refer to the guide at [./TRANSLATING.md](https://github.com/huggingface/smolagents/blob/main/docs/TRANSLATING.md).
127 | 
128 | ### Writing source documentation
129 | 
130 | Values that should be put in `code` should either be surrounded by backticks: \`like so\`. Note that argument names
131 | and objects like True, None, or any strings should usually be put in `code`.
132 | 
133 | When mentioning a class, function, or method, it is recommended to use our syntax for internal links so that our tool
134 | adds a link to its documentation with this syntax: \[\`XXXClass\`\] or \[\`function\`\]. This requires the class or
135 | function to be in the main package.
136 | 
137 | If you want to create a link to some internal class or function, you need to
138 | provide its path. For instance: \[\`utils.ModelOutput\`\]. This will be converted into a link with
139 | `utils.ModelOutput` in the description. To get rid of the path and only keep the name of the object you are
140 | linking to in the description, add a ~: \[\`~utils.ModelOutput\`\] will generate a link with `ModelOutput` in the description.
141 | 
142 | The same works for methods so you can either use \[\`XXXClass.method\`\] or \[~\`XXXClass.method\`\].
143 | 
144 | #### Defining arguments in a method
145 | 
146 | Arguments should be defined with the `Args:` (or `Arguments:` or `Parameters:`) prefix, followed by a line return and
147 | an indentation. The argument should be followed by its type, with its shape if it is a tensor, a colon, and its
148 | description:
149 | 
150 | ```
151 |     Args:
152 |         n_layers (`int`): The number of layers of the model.
153 | ```
154 | 
155 | If the description is too long to fit in one line, another indentation is necessary before writing the description
156 | after the argument.
157 | 
158 | Here's an example showcasing everything so far:
159 | 
160 | ```
161 |     Args:
162 |         input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
163 |             Indices of input sequence tokens in the vocabulary.
164 | 
165 |             Indices can be obtained using [`AlbertTokenizer`]. See [`~PreTrainedTokenizer.encode`] and
166 |             [`~PreTrainedTokenizer.__call__`] for details.
167 | 
168 |             [What are input IDs?](../glossary#input-ids)
169 | ```
170 | 
171 | For optional arguments or arguments with defaults we follow the following syntax: imagine we have a function with the
172 | following signature:
173 | 
174 | ```
175 | def my_function(x: str = None, a: float = 1):
176 | ```
177 | 
178 | then its documentation should look like this:
179 | 
180 | ```
181 |     Args:
182 |         x (`str`, *optional*):
183 |             This argument controls ...
184 |         a (`float`, *optional*, defaults to 1):
185 |             This argument is used to ...
186 | ```
187 | 
188 | Note that we always omit the "defaults to \`None\`" when None is the default for any argument. Also note that even
189 | if the first line describing your argument type and its default gets long, you can't break it on several lines. You can
190 | however write as many lines as you want in the indented description (see the example above with `input_ids`).
191 | 
192 | #### Writing a multi-line code block
193 | 
194 | Multi-line code blocks can be useful for displaying examples. They are done between two lines of three backticks as usual in Markdown:
195 | 
196 | 
197 | ````
198 | ```
199 | # first line of code
200 | # second line
201 | # etc
202 | ```
203 | ````
204 | 
205 | #### Writing a return block
206 | 
207 | The return block should be introduced with the `Returns:` prefix, followed by a line return and an indentation.
208 | The first line should be the type of the return, followed by a line return. No need to indent further for the elements
209 | building the return.
210 | 
211 | Here's an example of a single value return:
212 | 
213 | ```
214 |     Returns:
215 |         `List[int]`: A list of integers in the range [0, 1] --- 1 for a special token, 0 for a sequence token.
216 | ```
217 | 
218 | Here's an example of a tuple return, comprising several objects:
219 | 
220 | ```
221 |     Returns:
222 |         `tuple(torch.FloatTensor)` comprising various elements depending on the configuration ([`BertConfig`]) and inputs:
223 |         - ** loss** (*optional*, returned when `masked_lm_labels` is provided) `torch.FloatTensor` of shape `(1,)` --
224 |           Total loss is the sum of the masked language modeling loss and the next sequence prediction (classification) loss.
225 |         - **prediction_scores** (`torch.FloatTensor` of shape `(batch_size, sequence_length, config.vocab_size)`) --
226 |           Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).
227 | ```
228 | 
229 | #### Adding an image
230 | 
231 | Due to the rapidly growing repository, it is important to make sure that no files that would significantly weigh down the repository are added. This includes images, videos, and other non-text files. We prefer to leverage a hf.co hosted `dataset` like
232 | the ones hosted on [`hf-internal-testing`](https://huggingface.co/hf-internal-testing) in which to place these files and reference
233 | them by URL. We recommend putting them in the following dataset: [huggingface/documentation-images](https://huggingface.co/datasets/huggingface/documentation-images).
234 | If an external contribution, feel free to add the images to your PR and ask a Hugging Face member to migrate your images
235 | to this dataset.
236 | 
237 | #### Writing documentation examples
238 | 
239 | The syntax for Example docstrings can look as follows:
240 | 
241 | ```
242 |     Example:
243 | 
244 |     ```python
245 |     >>> from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
246 |     >>> from datasets import load_dataset
247 |     >>> import torch
248 | 
249 |     >>> dataset = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
250 |     >>> dataset = dataset.sort("id")
251 |     >>> sampling_rate = dataset.features["audio"].sampling_rate
252 | 
253 |     >>> processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
254 |     >>> model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
255 | 
256 |     >>> # audio file is decoded on the fly
257 |     >>> inputs = processor(dataset[0]["audio"]["array"], sampling_rate=sampling_rate, return_tensors="pt")
258 |     >>> with torch.no_grad():
259 |     ...     logits = model(**inputs).logits
260 |     >>> predicted_ids = torch.argmax(logits, dim=-1)
261 | 
262 |     >>> # transcribe speech
263 |     >>> transcription = processor.batch_decode(predicted_ids)
264 |     >>> transcription[0]
265 |     'MISTER QUILTER IS THE APOSTLE OF THE MIDDLE CLASSES AND WE ARE GLAD TO WELCOME HIS GOSPEL'
266 |     ```
267 | ```
268 | 
269 | The docstring should give a minimal, clear example of how the respective model
270 | is to be used in inference and also include the expected (ideally sensible)
271 | output.
272 | Often, readers will try out the example before even going through the function
273 | or class definitions. Therefore, it is of utmost importance that the example
274 | works as expected.


--------------------------------------------------------------------------------
/docs/source/en/_config.py:
--------------------------------------------------------------------------------
 1 | # docstyle-ignore
 2 | INSTALL_CONTENT = """
 3 | # Installation
 4 | ! pip install smolagents
 5 | # To install from source instead of the last release, comment the command above and uncomment the following one.
 6 | # ! pip install git+https://github.com/huggingface/smolagents.git
 7 | """
 8 | 
 9 | notebook_first_cells = [{"type": "code", "content": INSTALL_CONTENT}]
10 | black_avoid_patterns = {
11 |     "{processor_class}": "FakeProcessorClass",
12 |     "{model_class}": "FakeModelClass",
13 |     "{object_class}": "FakeObjectClass",
14 | }
15 | 


--------------------------------------------------------------------------------
/docs/source/en/_toctree.yml:
--------------------------------------------------------------------------------
 1 | - title: Get started
 2 |   sections:
 3 |   - local: index
 4 |     title: 🤗 Agents
 5 |   - local: guided_tour
 6 |     title: Guided tour
 7 | - title: Tutorials
 8 |   sections:
 9 |   - local: tutorials/building_good_agents
10 |     title: ✨ Building good agents
11 |   - local: tutorials/tools
12 |     title: 🛠️ Tools - in-depth guide
13 |   - local: tutorials/secure_code_execution
14 |     title: 🛡️ Secure your code execution with E2B
15 | - title: Conceptual guides
16 |   sections:
17 |   - local: conceptual_guides/intro_agents
18 |     title: 🤖 An introduction to agentic systems
19 |   - local: conceptual_guides/react
20 |     title: 🤔 How do Multi-step agents work?
21 | - title: Examples
22 |   sections:
23 |   - local: examples/text_to_sql
24 |     title: Self-correcting Text-to-SQL
25 |   - local: examples/rag
26 |     title: Master you knowledge base with agentic RAG
27 |   - local: examples/multiagents
28 |     title: Orchestrate a multi-agent system
29 | - title: Reference
30 |   sections:
31 |   - local: reference/agents
32 |     title: Agent-related objects
33 |   - local: reference/tools
34 |     title: Tool-related objects
35 | 


--------------------------------------------------------------------------------
/docs/source/en/conceptual_guides/intro_agents.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Introduction to Agents
 17 | 
 18 | ## 🤔 What are agents?
 19 | 
 20 | Any efficient system using AI will need to provide LLMs some kind of access to the real world: for instance the possibility to call a search tool to get external information, or to act on certain programs in order to solve a task. In other words, LLMs should have ***agency***. Agentic programs are the gateway to the outside world for LLMs.
 21 | 
 22 | > [!TIP]
 23 | > AI Agents are **programs where LLM outputs control the workflow**.
 24 | 
 25 | Any system leveraging LLMs will integrate the LLM outputs into code. The influence of the LLM's input on the code workflow is the level of agency of LLMs in the system.
 26 | 
 27 | Note that with this definition, "agent" is not a discrete, 0 or 1 definition: instead, "agency" evolves on a continuous spectrum, as you give more or less power to the LLM on your workflow.
 28 | 
 29 | See in the table below how agency can vary across systems:
 30 | 
 31 | | Agency Level | Description                                             | How that's called | Example Pattern                                    |
 32 | | ------------ | ------------------------------------------------------- | ----------------- | -------------------------------------------------- |
 33 | | ☆☆☆          | LLM output has no impact on program flow                | Simple Processor  | `process_llm_output(llm_response)`                 |
 34 | | ★☆☆          | LLM output determines an if/else switch                 | Router            | `if llm_decision(): path_a() else: path_b()`       |
 35 | | ★★☆          | LLM output determines function execution                | Tool Caller       | `run_function(llm_chosen_tool, llm_chosen_args)`   |
 36 | | ★★★          | LLM output controls iteration and program continuation  | Multi-step Agent  | `while llm_should_continue(): execute_next_step()` |
 37 | | ★★★          | One agentic workflow can start another agentic workflow | Multi-Agent       | `if llm_trigger(): execute_agent()`                |
 38 | 
 39 | The multi-step agent has this code structure:
 40 | 
 41 | ```python
 42 | memory = [user_defined_task]
 43 | while llm_should_continue(memory): # this loop is the multi-step part
 44 |     action = llm_get_next_action(memory) # this is the tool-calling part
 45 |     observations = execute_action(action)
 46 |     memory += [action, observations]
 47 | ```
 48 | 
 49 | This agentic system runs in a loop, executing a new action at each step (the action can involve calling some pre-determined *tools* that are just functions), until its observations make it apparent that a satisfactory state has been reached to solve the given task. Here’s an example of how a multi-step agent can solve a simple math question:
 50 | 
 51 | <div class="flex justify-center">
 52 |     <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/Agent_ManimCE.gif"/>
 53 | </div>
 54 | 
 55 | 
 56 | ## ✅ When to use agents / ⛔ when to avoid them
 57 | 
 58 | Agents are useful when you need an LLM to determine the workflow of an app. But they’re often overkill. The question is: do I really need flexibility in the workflow to efficiently solve the task at hand?
 59 | If the pre-determined workflow falls short too often, that means you need more flexibility.
 60 | Let's take an example: say you're making an app that handles customer requests on a surfing trip website.
 61 | 
 62 | You could know in advance that the requests will can belong to either of 2 buckets (based on user choice), and you have a predefined workflow for each of these 2 cases.
 63 | 
 64 | 1. Want some knowledge on the trips? ⇒ give them access to a search bar to search your knowledge base
 65 | 2. Wants to talk to sales? ⇒ let them type in a contact form.
 66 | 
 67 | If that deterministic workflow fits all queries, by all means just code everything! This will give you a 100% reliable system with no risk of error introduced by letting unpredictable LLMs meddle in your workflow. For the sake of simplicity and robustness, it's advised to regularize towards not using any agentic behaviour. 
 68 | 
 69 | But what if the workflow can't be determined that well in advance? 
 70 | 
 71 | For instance, a user wants to ask : `"I can come on Monday, but I forgot my passport so risk being delayed to Wednesday, is it possible to take me and my stuff to surf on Tuesday morning, with a cancellation insurance?"` This question hinges on many factors, and probably none of the predetermined criteria above will suffice for this request.
 72 | 
 73 | If the pre-determined workflow falls short too often, that means you need more flexibility.
 74 | 
 75 | That is where an agentic setup helps.
 76 | 
 77 | In the above example, you could just make a multi-step agent that has access to a weather API for weather forecasts, Google Maps API to compute travel distance, an employee availability dashboard and a RAG system on your knowledge base.
 78 | 
 79 | Until recently, computer programs were restricted to pre-determined workflows, trying to handle complexity by piling up  if/else switches. They focused on extremely narrow tasks, like "compute the sum of these numbers" or "find the shortest path in this graph". But actually, most real-life tasks, like our trip example above, do not fit in pre-determined workflows. Agentic systems open up the vast world of real-world tasks to programs!
 80 | 
 81 | ## Why `smolagents`?
 82 | 
 83 | For some low-level agentic use cases, like chains or routers, you can write all the code yourself. You'll be much better that way, since it will let you control and understand your system better.
 84 | 
 85 | But once you start going for more complicated behaviours like letting an LLM call a function (that's "tool calling") or letting an LLM run a while loop ("multi-step agent"), some abstractions become necessary:
 86 | - for tool calling, you need to parse the agent's output, so this output needs a predefined format like "Thought: I should call tool 'get_weather'. Action: get_weather(Paris).", that you parse with a predefined function, and system prompt given to the LLM should notify it about this format.
 87 | - for a multi-step agent where the LLM output determines the loop, you need to give a different prompt to the LLM based on what happened in the last loop iteration: so you need some kind of memory.
 88 | 
 89 | See? With these two examples, we already found the need for a few items to help us:
 90 | 
 91 | - Of course, an LLM that acts as the engine powering the system
 92 | - A list of tools that the agent can access
 93 | - A parser that extracts tool calls from the LLM output
 94 | - A system prompt synced with the parser
 95 | - A memory
 96 | 
 97 | But wait, since we give room to LLMs in decisions, surely they will make mistakes: so we need error logging and retry mechanisms.
 98 | 
 99 | All these elements need tight coupling to make a well-functioning system. That's why we decided we needed to make basic building blocks to make all this stuff work together.
100 | 
101 | ## Code agents
102 | 
103 | In a multi-step agent, at each step, the LLM can write an action, in the form of some calls to external tools. A common format (used by Anthropic, OpenAI, and many others) for writing these actions is generally different shades of "writing actions as a JSON of tools names and arguments to use, which you then parse to know which tool to execute and with which arguments".
104 | 
105 | [Multiple](https://huggingface.co/papers/2402.01030) [research](https://huggingface.co/papers/2411.01747) [papers](https://huggingface.co/papers/2401.00812) have shown that having the tool calling LLMs in code is much better.
106 | 
107 | The reason for this simply that *we crafted our code languages specifically to be the best possible way to express actions performed by a computer*. If JSON snippets were a better expression, JSON would be the top programming language and programming would be hell on earth.
108 | 
109 | The figure below, taken from [Executable Code Actions Elicit Better LLM Agents](https://huggingface.co/papers/2402.01030), illustrate some advantages of writing actions in code:
110 | 
111 | <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/code_vs_json_actions.png">
112 | 
113 | Writing actions in code rather than JSON-like snippets provides better:
114 | 
115 | - **Composability:** could you nest JSON actions within each other, or define a set of JSON actions to re-use later, the same way you could just define a python function?
116 | - **Object management:** how do you store the output of an action like `generate_image` in JSON?
117 | - **Generality:** code is built to express simply anything you can have a computer do.
118 | - **Representation in LLM training data:** plenty of quality code actions is already included in LLMs’ training data which means they’re already trained for this!
119 | 


--------------------------------------------------------------------------------
/docs/source/en/conceptual_guides/react.md:
--------------------------------------------------------------------------------
 1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
 2 | 
 3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 4 | the License. You may obtain a copy of the License at
 5 | 
 6 | http://www.apache.org/licenses/LICENSE-2.0
 7 | 
 8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
10 | specific language governing permissions and limitations under the License.
11 | 
12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
13 | rendered properly in your Markdown viewer.
14 | 
15 | -->
16 | # How do multi-step agents work?
17 | 
18 | The ReAct framework ([Yao et al., 2022](https://huggingface.co/papers/2210.03629)) is currently the main approach to building agents.
19 | 
20 | The name is based on the concatenation of two words, "Reason" and "Act." Indeed, agents following this architecture will solve their task in as many steps as needed, each step consisting of a Reasoning step, then an Action step where it formulates tool calls that will bring it closer to solving the task at hand.
21 | 
22 | React process involves keeping a memory of past steps.
23 | 
24 | > [!TIP]
25 | > Read [Open-source LLMs as LangChain Agents](https://huggingface.co/blog/open-source-llms-as-agents) blog post to learn more about multi-step agents.
26 | 
27 | Here is a video overview of how that works:
28 | 
29 | <div class="flex justify-center">
30 |     <img
31 |         class="block dark:hidden"
32 |         src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/Agent_ManimCE.gif"
33 |     />
34 |     <img
35 |         class="hidden dark:block"
36 |         src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/Agent_ManimCE.gif"
37 |     />
38 | </div>
39 | 
40 | ![Framework of a React Agent](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/open-source-llms-as-agents/ReAct.png)
41 | 
42 | We implement two versions of ToolCallingAgent: 
43 | - [`ToolCallingAgent`] generates tool calls as a JSON in its output.
44 | - [`CodeAgent`] is a new type of ToolCallingAgent that generates its tool calls as blobs of code, which works really well for LLMs that have strong coding performance.
45 | 
46 | > [!TIP]
47 | > We also provide an option to run agents in one-shot: just pass `single_step=True` when launching the agent, like `agent.run(your_task, single_step=True)`


--------------------------------------------------------------------------------
/docs/source/en/examples/multiagents.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Orchestrate a multi-agent system 🤖🤝🤖
 17 | 
 18 | [[open-in-colab]]
 19 | 
 20 | In this notebook we will make a **multi-agent web browser: an agentic system with several agents collaborating to solve problems using the web!**
 21 | 
 22 | It will be a simple hierarchy, using a `ManagedAgent` object to wrap the managed web search agent:
 23 | 
 24 | ```
 25 |               +----------------+
 26 |               | Manager agent  |
 27 |               +----------------+
 28 |                        |
 29 |         _______________|______________
 30 |        |                              |
 31 |   Code interpreter   +--------------------------------+
 32 |        tool          |         Managed agent          |
 33 |                      |      +------------------+      |
 34 |                      |      | Web Search agent |      |
 35 |                      |      +------------------+      |
 36 |                      |         |            |         |
 37 |                      |  Web Search tool     |         |
 38 |                      |             Visit webpage tool |
 39 |                      +--------------------------------+
 40 | ```
 41 | Let's set up this system. 
 42 | 
 43 | Run the line below to install the required dependencies:
 44 | 
 45 | ```
 46 | !pip install markdownify duckduckgo-search smolagents --upgrade -q
 47 | ```
 48 | 
 49 | Let's login in order to call the HF Inference API:
 50 | 
 51 | ```py
 52 | from huggingface_hub import notebook_login
 53 | 
 54 | notebook_login()
 55 | ```
 56 | 
 57 | ⚡️ Our agent will be powered by [Qwen/Qwen2.5-Coder-32B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct) using `HfApiModel` class that uses HF's Inference API: the Inference API allows to quickly and easily run any OS model.
 58 | 
 59 | _Note:_ The Inference API hosts models based on various criteria, and deployed models may be updated or replaced without prior notice. Learn more about it [here](https://huggingface.co/docs/api-inference/supported-models).
 60 | 
 61 | ```py
 62 | model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"
 63 | ```
 64 | 
 65 | ## 🔍 Create a web search tool
 66 | 
 67 | For web browsing, we can already use our pre-existing [`DuckDuckGoSearchTool`](https://github.com/huggingface/smolagents/blob/main/src/smolagents/default_tools/search.py) tool to provide a Google search equivalent.
 68 | 
 69 | But then we will also need to be able to peak into the page found by the `DuckDuckGoSearchTool`.
 70 | To do so, we could import the library's built-in `VisitWebpageTool`, but we will build it again to see how it's done.
 71 | 
 72 | So let's create our `VisitWebpageTool` tool from scratch using `markdownify`.
 73 | 
 74 | ```py
 75 | import re
 76 | import requests
 77 | from markdownify import markdownify
 78 | from requests.exceptions import RequestException
 79 | from smolagents import tool
 80 | 
 81 | 
 82 | @tool
 83 | def visit_webpage(url: str) -> str:
 84 |     """Visits a webpage at the given URL and returns its content as a markdown string.
 85 | 
 86 |     Args:
 87 |         url: The URL of the webpage to visit.
 88 | 
 89 |     Returns:
 90 |         The content of the webpage converted to Markdown, or an error message if the request fails.
 91 |     """
 92 |     try:
 93 |         # Send a GET request to the URL
 94 |         response = requests.get(url)
 95 |         response.raise_for_status()  # Raise an exception for bad status codes
 96 | 
 97 |         # Convert the HTML content to Markdown
 98 |         markdown_content = markdownify(response.text).strip()
 99 | 
100 |         # Remove multiple line breaks
101 |         markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
102 | 
103 |         return markdown_content
104 | 
105 |     except RequestException as e:
106 |         return f"Error fetching the webpage: {str(e)}"
107 |     except Exception as e:
108 |         return f"An unexpected error occurred: {str(e)}"
109 | ```
110 | 
111 | Ok, now let's initialize and test our tool!
112 | 
113 | ```py
114 | print(visit_webpage("https://en.wikipedia.org/wiki/Hugging_Face")[:500])
115 | ```
116 | 
117 | ## Build our multi-agent system 🤖🤝🤖
118 | 
119 | Now that we have all the tools `search` and `visit_webpage`, we can use them to create the web agent.
120 | 
121 | Which configuration to choose for this agent?
122 | - Web browsing is a single-timeline task that does not require parallel tool calls, so JSON tool calling works well for that. We thus choose a `JsonAgent`.
123 | - Also, since sometimes web search requires exploring many pages before finding the correct answer, we prefer to increase the number of `max_iterations` to 10.
124 | 
125 | ```py
126 | from smolagents import (
127 |     CodeAgent,
128 |     ToolCallingAgent,
129 |     HfApiModel,
130 |     ManagedAgent,
131 |     DuckDuckGoSearchTool,
132 |     LiteLLMModel,
133 | )
134 | 
135 | model = HfApiModel(model_id)
136 | 
137 | web_agent = ToolCallingAgent(
138 |     tools=[DuckDuckGoSearchTool(), visit_webpage],
139 |     model=model,
140 |     max_iterations=10,
141 | )
142 | ```
143 | 
144 | We then wrap this agent into a `ManagedAgent` that will make it callable by its manager agent.
145 | 
146 | ```py
147 | managed_web_agent = ManagedAgent(
148 |     agent=web_agent,
149 |     name="search",
150 |     description="Runs web searches for you. Give it your query as an argument.",
151 | )
152 | ```
153 | 
154 | Finally we create a manager agent, and upon initialization we pass our managed agent to it in its `managed_agents` argument.
155 | 
156 | Since this agent is the one tasked with the planning and thinking, advanced reasoning will be beneficial, so a `CodeAgent` will be the best choice.
157 | 
158 | Also, we want to ask a question that involves the current year and does additional data calculations: so let us add `additional_authorized_imports=["time", "numpy", "pandas"]`, just in case the agent needs these packages.
159 | 
160 | ```py
161 | manager_agent = CodeAgent(
162 |     tools=[],
163 |     model=model,
164 |     managed_agents=[managed_web_agent],
165 |     additional_authorized_imports=["time", "numpy", "pandas"],
166 | )
167 | ```
168 | 
169 | That's all! Now let's run our system! We select a question that requires both some calculation and research:
170 | 
171 | ```py
172 | answer = manager_agent.run("If LLM trainings continue to scale up at the current rythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What does that correspond to, compared to some contries? Please provide a source for any number used.")
173 | ```
174 | 
175 | We get this report as the answer:
176 | ```
177 | Based on current growth projections and energy consumption estimates, if LLM trainings continue to scale up at the 
178 | current rhythm until 2030:
179 | 
180 | 1. The electric power required to power the biggest training runs by 2030 would be approximately 303.74 GW, which 
181 | translates to about 2,660,762 GWh/year.
182 | 
183 | 2. Comparing this to countries' electricity consumption:
184 |    - It would be equivalent to about 34% of China's total electricity consumption.
185 |    - It would exceed the total electricity consumption of India (184%), Russia (267%), and Japan (291%).
186 |    - It would be nearly 9 times the electricity consumption of countries like Italy or Mexico.
187 | 
188 | 3. Source of numbers:
189 |    - The initial estimate of 5 GW for future LLM training comes from AWS CEO Matt Garman.
190 |    - The growth projection used a CAGR of 79.80% from market research by Springs.
191 |    - Country electricity consumption data is from the U.S. Energy Information Administration, primarily for the year 
192 | 2021.
193 | ```
194 | 
195 | Seems like we'll need some sizeable powerplants if the [scaling hypothesis](https://gwern.net/scaling-hypothesis) continues to hold true.
196 | 
197 | Our agents managed to efficiently collaborate towards solving the task! ✅
198 | 
199 | 💡 You can easily extend this orchestration to more agents: one does the code execution, one the web search, one handles file loadings...


--------------------------------------------------------------------------------
/docs/source/en/examples/rag.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Agentic RAG
 17 | 
 18 | [[open-in-colab]]
 19 | 
 20 | Retrieval-Augmented-Generation (RAG) is “using an LLM to answer a user query, but basing the answer on information retrieved from a knowledge base”. It has many advantages over using a vanilla or fine-tuned LLM: to name a few, it allows to ground the answer on true facts and reduce confabulations, it allows to provide the LLM with domain-specific knowledge, and it allows fine-grained control of access to information from the knowledge base.
 21 | 
 22 | But vanilla RAG has limitations, most importantly these two:
 23 | - It performs only one retrieval step: if the results are bad, the generation in turn will be bad.
 24 | - Semantic similarity is computed with the user query as a reference, which might be suboptimal: for instance, the user query will often be a question and the document containing the true answer will be in affirmative voice, so its similarity score will be downgraded compared to other source documents in the interrogative form, leading to a risk of missing the relevant information.
 25 | 
 26 | We can alleviate these problems by making a RAG agent: very simply, an agent armed with a retriever tool!
 27 | 
 28 | This agent will: ✅ Formulate the query itself and ✅ Critique to re-retrieve if needed.
 29 | 
 30 | So it should naively recover some advanced RAG techniques!
 31 | - Instead of directly using the user query as the reference in semantic search, the agent formulates itself a reference sentence that can be closer to the targeted documents, as in [HyDE](https://huggingface.co/papers/2212.10496).
 32 | The agent can the generated snippets and re-retrieve if needed, as in [Self-Query](https://docs.llamaindex.ai/en/stable/examples/evaluation/RetryQuery/).
 33 | 
 34 | Let's build this system. 🛠️
 35 | 
 36 | Run the line below to install required dependencies:
 37 | ```bash
 38 | !pip install smolagents pandas langchain langchain-community sentence-transformers faiss-cpu --upgrade -q
 39 | ```
 40 | To call the HF Inference API, you will need a valid token as your environment variable `HF_TOKEN`.
 41 | We use python-dotenv to load it.
 42 | ```py
 43 | from dotenv import load_dotenv
 44 | load_dotenv()
 45 | ```
 46 | 
 47 | We first load a knowledge base on which we want to perform RAG: this dataset is a compilation of the documentation pages for many Hugging Face libraries, stored as markdown. We will keep only the documentation for the `transformers` library.
 48 | 
 49 | Then prepare the knowledge base by processing the dataset and storing it into a vector database to be used by the retriever.
 50 | 
 51 | We use [LangChain](https://python.langchain.com/docs/introduction/) for its excellent vector database utilities.
 52 | 
 53 | ```py
 54 | import datasets
 55 | from langchain.docstore.document import Document
 56 | from langchain.text_splitter import RecursiveCharacterTextSplitter
 57 | from langchain_community.retrievers import BM25Retriever
 58 | 
 59 | knowledge_base = datasets.load_dataset("m-ric/huggingface_doc", split="train")
 60 | knowledge_base = knowledge_base.filter(lambda row: row["source"].startswith("huggingface/transformers"))
 61 | 
 62 | source_docs = [
 63 |     Document(page_content=doc["text"], metadata={"source": doc["source"].split("/")[1]})
 64 |     for doc in knowledge_base
 65 | ]
 66 | 
 67 | text_splitter = RecursiveCharacterTextSplitter(
 68 |     chunk_size=500,
 69 |     chunk_overlap=50,
 70 |     add_start_index=True,
 71 |     strip_whitespace=True,
 72 |     separators=["\n\n", "\n", ".", " ", ""],
 73 | )
 74 | docs_processed = text_splitter.split_documents(source_docs)
 75 | ```
 76 | 
 77 | Now the documents are ready.
 78 | 
 79 | So let’s build our agentic RAG system!
 80 | 
 81 | 👉 We only need a RetrieverTool that our agent can leverage to retrieve information from the knowledge base.
 82 | 
 83 | Since we need to add a vectordb as an attribute of the tool, we cannot simply use the simple tool constructor with a `@tool` decorator: so we will follow the advanced setup highlighted in the [tools tutorial](../tutorials/tools).
 84 | 
 85 | ```py
 86 | from smolagents import Tool
 87 | 
 88 | class RetrieverTool(Tool):
 89 |     name = "retriever"
 90 |     description = "Uses semantic search to retrieve the parts of transformers documentation that could be most relevant to answer your query."
 91 |     inputs = {
 92 |         "query": {
 93 |             "type": "string",
 94 |             "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
 95 |         }
 96 |     }
 97 |     output_type = "string"
 98 | 
 99 |     def __init__(self, docs, **kwargs):
100 |         super().__init__(**kwargs)
101 |         self.retriever = BM25Retriever.from_documents(
102 |             docs, k=10
103 |         )
104 | 
105 |     def forward(self, query: str) -> str:
106 |         assert isinstance(query, str), "Your search query must be a string"
107 | 
108 |         docs = self.retriever.invoke(
109 |             query,
110 |         )
111 |         return "\nRetrieved documents:\n" + "".join(
112 |             [
113 |                 f"\n\n===== Document {str(i)} =====\n" + doc.page_content
114 |                 for i, doc in enumerate(docs)
115 |             ]
116 |         )
117 | 
118 | retriever_tool = RetrieverTool(docs_processed)
119 | ```
120 | We have used BM25, a classic retrieval method, because it's lightning fast to setup.
121 | To improve retrieval accuracy, you could use replace BM25 with semantic search using vector representations for documents: thus you can head to the [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) to select a good embedding model.
122 | 
123 | Now it’s straightforward to create an agent that leverages this `retriever_tool`!
124 | 
125 | The agent will need these arguments upon initialization:
126 | - `tools`: a list of tools that the agent will be able to call.
127 | - `model`: the LLM that powers the agent.
128 | Our `model` must be a callable that takes as input a list of messages and returns text. It also needs to accept a stop_sequences argument that indicates when to stop its generation. For convenience, we directly use the HfEngine class provided in the package to get a LLM engine that calls Hugging Face's Inference API.
129 | 
130 | And we use [meta-llama/Llama-3.3-70B-Instruct](meta-llama/Llama-3.3-70B-Instruct) as the llm engine because:
131 | - It has a long 128k context, which is helpful for processing long source documents
132 | - It is served for free at all times on HF's Inference API!
133 | 
134 | _Note:_ The Inference API hosts models based on various criteria, and deployed models may be updated or replaced without prior notice. Learn more about it [here](https://huggingface.co/docs/api-inference/supported-models).
135 | 
136 | ```py
137 | from smolagents import HfApiModel, CodeAgent
138 | 
139 | agent = CodeAgent(
140 |     tools=[retriever_tool], model=HfApiModel("meta-llama/Llama-3.3-70B-Instruct"), max_iterations=4, verbose=True
141 | )
142 | ```
143 | 
144 | Upon initializing the CodeAgent, it has been automatically given a default system prompt that tells the LLM engine to process step-by-step and generate tool calls as code snippets, but you could replace this prompt template with your own as needed.
145 | 
146 | Then when its `.run()` method is launched, the agent takes care of calling the LLM engine, and executing the tool calls, all in a loop that ends only when tool `final_answer` is called with the final answer as its argument.
147 | 
148 | ```py
149 | agent_output = agent.run("For a transformers model training, which is slower, the forward or the backward pass?")
150 | 
151 | print("Final output:")
152 | print(agent_output)
153 | ```
154 | 
155 | 
156 | 
157 | 


--------------------------------------------------------------------------------
/docs/source/en/examples/text_to_sql.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Text-to-SQL
 17 | 
 18 | [[open-in-colab]]
 19 | 
 20 | In this tutorial, we’ll see how to implement an agent that leverages SQL using `smolagents`.
 21 | 
 22 | > Let's start with the golden question: why not keep it simple and use a standard text-to-SQL pipeline?
 23 | 
 24 | A standard text-to-sql pipeline is brittle, since the generated SQL query can be incorrect. Even worse, the query could be incorrect, but not raise an error, instead giving some incorrect/useless outputs without raising an alarm.
 25 | 
 26 | 👉 Instead, an agent system is able to critically inspect outputs and decide if the query needs to be changed or not, thus giving it a huge performance boost.
 27 | 
 28 | Let’s build this agent! 💪
 29 | 
 30 | First, we setup the SQL environment:
 31 | ```py
 32 | from sqlalchemy import (
 33 |     create_engine,
 34 |     MetaData,
 35 |     Table,
 36 |     Column,
 37 |     String,
 38 |     Integer,
 39 |     Float,
 40 |     insert,
 41 |     inspect,
 42 |     text,
 43 | )
 44 | 
 45 | engine = create_engine("sqlite:///:memory:")
 46 | metadata_obj = MetaData()
 47 | 
 48 | # create city SQL table
 49 | table_name = "receipts"
 50 | receipts = Table(
 51 |     table_name,
 52 |     metadata_obj,
 53 |     Column("receipt_id", Integer, primary_key=True),
 54 |     Column("customer_name", String(16), primary_key=True),
 55 |     Column("price", Float),
 56 |     Column("tip", Float),
 57 | )
 58 | metadata_obj.create_all(engine)
 59 | 
 60 | rows = [
 61 |     {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
 62 |     {"receipt_id": 2, "customer_name": "Alex Mason", "price": 23.86, "tip": 0.24},
 63 |     {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
 64 |     {"receipt_id": 4, "customer_name": "Margaret James", "price": 21.11, "tip": 1.00},
 65 | ]
 66 | for row in rows:
 67 |     stmt = insert(receipts).values(**row)
 68 |     with engine.begin() as connection:
 69 |         cursor = connection.execute(stmt)
 70 | ```
 71 | 
 72 | ### Build our agent
 73 | 
 74 | Now let’s make our SQL table retrievable by a tool.
 75 | 
 76 | The tool’s description attribute will be embedded in the LLM’s prompt by the agent system: it gives the LLM information about how to use the tool. This is where we want to describe the SQL table.
 77 | 
 78 | ```py
 79 | inspector = inspect(engine)
 80 | columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]
 81 | 
 82 | table_description = "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
 83 | print(table_description)
 84 | ```
 85 | 
 86 | ```text
 87 | Columns:
 88 |   - receipt_id: INTEGER
 89 |   - customer_name: VARCHAR(16)
 90 |   - price: FLOAT
 91 |   - tip: FLOAT
 92 | ```
 93 | 
 94 | Now let’s build our tool. It needs the following: (read [the tool doc](../tutorials/tools) for more detail)
 95 | - A docstring with an `Args:` part listing arguments.
 96 | - Type hints on both inputs and output.
 97 | 
 98 | ```py
 99 | from smolagents import tool
100 | 
101 | @tool
102 | def sql_engine(query: str) -> str:
103 |     """
104 |     Allows you to perform SQL queries on the table. Returns a string representation of the result.
105 |     The table is named 'receipts'. Its description is as follows:
106 |         Columns:
107 |         - receipt_id: INTEGER
108 |         - customer_name: VARCHAR(16)
109 |         - price: FLOAT
110 |         - tip: FLOAT
111 | 
112 |     Args:
113 |         query: The query to perform. This should be correct SQL.
114 |     """
115 |     output = ""
116 |     with engine.connect() as con:
117 |         rows = con.execute(text(query))
118 |         for row in rows:
119 |             output += "\n" + str(row)
120 |     return output
121 | ```
122 | 
123 | Now let us create an agent that leverages this tool.
124 | 
125 | We use the `CodeAgent`, which is transformers.agents’ main agent class: an agent that writes actions in code and can iterate on previous output according to the ReAct framework.
126 | 
127 | The model is the LLM that powers the agent system. HfApiModel allows you to call LLMs using HF’s Inference API, either via Serverless or Dedicated endpoint, but you could also use any proprietary API.
128 | 
129 | ```py
130 | from smolagents import CodeAgent, HfApiModel
131 | 
132 | agent = CodeAgent(
133 |     tools=[sql_engine],
134 |     model=HfApiModel("meta-llama/Meta-Llama-3.1-8B-Instruct"),
135 | )
136 | agent.run("Can you give me the name of the client who got the most expensive receipt?")
137 | ```
138 | 
139 | ### Level 2: Table joins
140 | 
141 | Now let’s make it more challenging! We want our agent to handle joins across multiple tables.
142 | 
143 | So let’s make a second table recording the names of waiters for each receipt_id!
144 | 
145 | ```py
146 | table_name = "waiters"
147 | receipts = Table(
148 |     table_name,
149 |     metadata_obj,
150 |     Column("receipt_id", Integer, primary_key=True),
151 |     Column("waiter_name", String(16), primary_key=True),
152 | )
153 | metadata_obj.create_all(engine)
154 | 
155 | rows = [
156 |     {"receipt_id": 1, "waiter_name": "Corey Johnson"},
157 |     {"receipt_id": 2, "waiter_name": "Michael Watts"},
158 |     {"receipt_id": 3, "waiter_name": "Michael Watts"},
159 |     {"receipt_id": 4, "waiter_name": "Margaret James"},
160 | ]
161 | for row in rows:
162 |     stmt = insert(receipts).values(**row)
163 |     with engine.begin() as connection:
164 |         cursor = connection.execute(stmt)
165 | ```
166 | Since we changed the table, we update the `SQLExecutorTool` with this table’s description to let the LLM properly leverage information from this table.
167 | 
168 | ```py
169 | updated_description = """Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
170 | It can use the following tables:"""
171 | 
172 | inspector = inspect(engine)
173 | for table in ["receipts", "waiters"]:
174 |     columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]
175 | 
176 |     table_description = f"Table '{table}':\n"
177 | 
178 |     table_description += "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
179 |     updated_description += "\n\n" + table_description
180 | 
181 | print(updated_description)
182 | ```
183 | Since this request is a bit harder than the previous one, we’ll switch the LLM engine to use the more powerful [Qwen/Qwen2.5-Coder-32B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)!
184 | 
185 | ```py
186 | sql_engine.description = updated_description
187 | 
188 | agent = CodeAgent(
189 |     tools=[sql_engine],
190 |     model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),
191 | )
192 | 
193 | agent.run("Which waiter got more total money from tips?")
194 | ```
195 | It directly works! The setup was surprisingly simple, wasn’t it?
196 | 
197 | This example is done! We've touched upon these concepts:
198 | - Building new tools.
199 | - Updating a tool's description.
200 | - Switching to a stronger LLM helps agent reasoning.
201 | 
202 | ✅ Now you can go build this text-to-SQL system you’ve always dreamt of! ✨


--------------------------------------------------------------------------------
/docs/source/en/index.md:
--------------------------------------------------------------------------------
 1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
 2 | 
 3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 4 | the License. You may obtain a copy of the License at
 5 | 
 6 | http://www.apache.org/licenses/LICENSE-2.0
 7 | 
 8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
10 | specific language governing permissions and limitations under the License.
11 | 
12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
13 | rendered properly in your Markdown viewer.
14 | -->
15 | 
16 | # `smolagents`
17 | 
18 | This library is the simplest framework out there to build powerful agents! By the way, wtf are "agents"? We provide our definition [in this page](conceptual_guides/intro_agents), whe're you'll also find tips for when to use them or not (spoilers: you'll often be better off without agents).
19 | 
20 | This library offers:
21 | 
22 | ✨ **Simplicity**: the logic for agents fits in ~thousand lines of code. We kept abstractions to their minimal shape above raw code!
23 | 
24 | 🌐 **Support for any LLM**: it supports models hosted on the Hub loaded in their `transformers` version or through our inference API, but also models from OpenAI, Anthropic... it's really easy to power an agent with any LLM.
25 | 
26 | 🧑‍💻 **First-class support for Code Agents**, i.e. agents that write their actions in code (as opposed to "agents being used to write code"), [read more here](tutorials/secure_code_execution).
27 | 
28 | 🤗 **Hub integrations**: you can share and load tools to/from the Hub, and more is to come!
29 | 
30 | <div class="mt-10">
31 |   <div class="w-full flex flex-col space-y-4 md:space-y-0 md:grid md:grid-cols-2 md:gap-y-4 md:gap-x-5">
32 |     <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="./guided_tour"
33 |       ><div class="w-full text-center bg-gradient-to-br from-blue-400 to-blue-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">Guided tour</div>
34 |       <p class="text-gray-700">Learn the basics and become familiar with using Agents. Start here if you are using Agents for the first time!</p>
35 |     </a>
36 |     <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="./examples/text_to_sql"
37 |       ><div class="w-full text-center bg-gradient-to-br from-indigo-400 to-indigo-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">How-to guides</div>
38 |       <p class="text-gray-700">Practical guides to help you achieve a specific goal: create an agent to generate and test SQL queries!</p>
39 |     </a>
40 |     <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="./conceptual_guides/intro_agents"
41 |       ><div class="w-full text-center bg-gradient-to-br from-pink-400 to-pink-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">Conceptual guides</div>
42 |       <p class="text-gray-700">High-level explanations for building a better understanding of important topics.</p>
43 |    </a>
44 |     <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="./tutorials/building_good_agents"
45 |       ><div class="w-full text-center bg-gradient-to-br from-purple-400 to-purple-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">Tutorials</div>
46 |       <p class="text-gray-700">Horizontal tutorials that cover important aspects of building agents.</p>
47 |     </a>
48 |   </div>
49 | </div>
50 | 


--------------------------------------------------------------------------------
/docs/source/en/reference/agents.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Agents
 17 | 
 18 | <Tip warning={true}>
 19 | 
 20 | Smolagents is an experimental API which is subject to change at any time. Results returned by the agents
 21 | can vary as the APIs or underlying models are prone to change.
 22 | 
 23 | </Tip>
 24 | 
 25 | To learn more about agents and tools make sure to read the [introductory guide](../index). This page
 26 | contains the API docs for the underlying classes.
 27 | 
 28 | ## Agents
 29 | 
 30 | Our agents inherit from [`MultiStepAgent`], which means they can act in multiple steps, each step consisting of one thought, then one tool call and execution. Read more in [this conceptual guide](../conceptual_guides/react).
 31 | 
 32 | We provide two types of agents, based on the main [`Agent`] class.
 33 |   - [`CodeAgent`] is the default agent, it writes its tool calls in Python code.
 34 |   - [`ToolCallingAgent`] writes its tool calls in JSON.
 35 | 
 36 | Both require arguments `model` and list of tools `tools` at initialization.
 37 | 
 38 | 
 39 | ### Classes of agents
 40 | 
 41 | [[autodoc]] MultiStepAgent
 42 | 
 43 | [[autodoc]] CodeAgent
 44 | 
 45 | [[autodoc]] ToolCallingAgent
 46 | 
 47 | 
 48 | ### ManagedAgent
 49 | 
 50 | [[autodoc]] ManagedAgent
 51 | 
 52 | ### stream_to_gradio
 53 | 
 54 | [[autodoc]] stream_to_gradio
 55 | 
 56 | ### GradioUI
 57 | 
 58 | [[autodoc]] GradioUI
 59 | 
 60 | ## Models
 61 | 
 62 | You're free to create and use your own models to power your agent.
 63 | 
 64 | You could use any `model` callable for your agent, as long as:
 65 | 1. It follows the [messages format](./chat_templating) (`List[Dict[str, str]]`) for its input `messages`, and it returns a `str`.
 66 | 2. It stops generating outputs *before* the sequences passed in the argument `stop_sequences`
 67 | 
 68 | For defining your LLM, you can make a `custom_model` method which accepts a list of [messages](./chat_templating) and returns text. This callable also needs to accept a `stop_sequences` argument that indicates when to stop generating.
 69 | 
 70 | ```python
 71 | from huggingface_hub import login, InferenceClient
 72 | 
 73 | login("<YOUR_HUGGINGFACEHUB_API_TOKEN>")
 74 | 
 75 | model_id = "meta-llama/Llama-3.3-70B-Instruct"
 76 | 
 77 | client = InferenceClient(model=model_id)
 78 | 
 79 | def custom_model(messages, stop_sequences=["Task"]) -> str:
 80 |     response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1000)
 81 |     answer = response.choices[0].message.content
 82 |     return answer
 83 | ```
 84 | 
 85 | Additionally, `custom_model` can also take a `grammar` argument. In the case where you specify a `grammar` upon agent initialization, this argument will be passed to the calls to model, with the `grammar` that you defined upon initialization, to allow [constrained generation](https://huggingface.co/docs/text-generation-inference/conceptual/guidance) in order to force properly-formatted agent outputs.
 86 | 
 87 | ### TransformersModel
 88 | 
 89 | For convenience, we have added a `TransformersModel` that implements the points above by building a local `transformers` pipeline for the model_id given at initialization.
 90 | 
 91 | ```python
 92 | from smolagents import TransformersModel
 93 | 
 94 | model = TransformersModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct")
 95 | 
 96 | print(model([{"role": "user", "content": "Ok!"}], stop_sequences=["great"]))
 97 | ```
 98 | ```text
 99 | >>> What a
100 | ```
101 | 
102 | [[autodoc]] TransformersModel
103 | 
104 | ### HfApiModel
105 | 
106 | The `HfApiModel` wraps an [HF Inference API](https://huggingface.co/docs/api-inference/index) client for the execution of the LLM.
107 | 
108 | ```python
109 | from smolagents import HfApiModel
110 | 
111 | messages = [
112 |   {"role": "user", "content": "Hello, how are you?"},
113 |   {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
114 |   {"role": "user", "content": "No need to help, take it easy."},
115 | ]
116 | 
117 | model = HfApiModel()
118 | print(model(messages))
119 | ```
120 | ```text
121 | >>> Of course! If you change your mind, feel free to reach out. Take care!
122 | ```
123 | [[autodoc]] HfApiModel
124 | 
125 | ### LiteLLMModel
126 | 
127 | The `LiteLLMModel` leverages [LiteLLM](https://www.litellm.ai/) to support 100+ LLMs from various providers.
128 | 
129 | ```python
130 | from smolagents import LiteLLMModel
131 | 
132 | messages = [
133 |   {"role": "user", "content": "Hello, how are you?"},
134 |   {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
135 |   {"role": "user", "content": "No need to help, take it easy."},
136 | ]
137 | 
138 | model = LiteLLMModel("anthropic/claude-3-5-sonnet-latest")
139 | print(model(messages))
140 | ```
141 | 
142 | [[autodoc]] LiteLLMModel


--------------------------------------------------------------------------------
/docs/source/en/reference/tools.md:
--------------------------------------------------------------------------------
 1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
 2 | 
 3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 4 | the License. You may obtain a copy of the License at
 5 | 
 6 | http://www.apache.org/licenses/LICENSE-2.0
 7 | 
 8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
10 | specific language governing permissions and limitations under the License.
11 | 
12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
13 | rendered properly in your Markdown viewer.
14 | 
15 | -->
16 | # Tools
17 | 
18 | <Tip warning={true}>
19 | 
20 | Smolagents is an experimental API which is subject to change at any time. Results returned by the agents
21 | can vary as the APIs or underlying models are prone to change.
22 | 
23 | </Tip>
24 | 
25 | To learn more about agents and tools make sure to read the [introductory guide](../index). This page
26 | contains the API docs for the underlying classes.
27 | 
28 | ## Tools
29 | 
30 | ### load_tool
31 | 
32 | [[autodoc]] load_tool
33 | 
34 | ### tool
35 | 
36 | [[autodoc]] tool
37 | 
38 | ### Tool
39 | 
40 | [[autodoc]] Tool
41 | 
42 | ### Toolbox
43 | 
44 | [[autodoc]] Toolbox
45 | 
46 | ### launch_gradio_demo
47 | 
48 | [[autodoc]] launch_gradio_demo
49 | 
50 | 
51 | ### ToolCollection
52 | 
53 | [[autodoc]] ToolCollection
54 | 
55 | ## Agent Types
56 | 
57 | Agents can handle any type of object in-between tools; tools, being completely multimodal, can accept and return
58 | text, image, audio, video, among other types. In order to increase compatibility between tools, as well as to 
59 | correctly render these returns in ipython (jupyter, colab, ipython notebooks, ...), we implement wrapper classes
60 | around these types.
61 | 
62 | The wrapped objects should continue behaving as initially; a text object should still behave as a string, an image
63 | object should still behave as a `PIL.Image`.
64 | 
65 | These types have three specific purposes:
66 | 
67 | - Calling `to_raw` on the type should return the underlying object
68 | - Calling `to_string` on the type should return the object as a string: that can be the string in case of an `AgentText`
69 |   but will be the path of the serialized version of the object in other instances
70 | - Displaying it in an ipython kernel should display the object correctly
71 | 
72 | ### AgentText
73 | 
74 | [[autodoc]] smolagents.types.AgentText
75 | 
76 | ### AgentImage
77 | 
78 | [[autodoc]] smolagents.types.AgentImage
79 | 
80 | ### AgentAudio
81 | 
82 | [[autodoc]] smolagents.types.AgentAudio
83 | 


--------------------------------------------------------------------------------
/docs/source/en/tutorials/building_good_agents.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Building good agents
 17 | 
 18 | [[open-in-colab]]
 19 | 
 20 | There's a world of difference between building an agent that works and one that doesn't.
 21 | How to build into this latter category?
 22 | In this guide, we're going to see best practices for building agents.
 23 | 
 24 | > [!TIP]
 25 | > If you're new to building agents, make sure to first read the [intro to agents](../conceptual_guides/intro_agents) and the [guided tour of smolagents](../guided_tour).
 26 | 
 27 | ### The best agentic systems are the simplest: simplify the workflow as much as you can
 28 | 
 29 | Giving an LLM some agency in your workflow introducessome risk of errors.
 30 | 
 31 | Well-programmed agentic systems have good error logging and retry mechanisms anyway, so the LLM engine has a chance to self-correct their mistake. But to reduce the risk of LLM error to the maximum, you should simplify your worklow!
 32 | 
 33 | Let's take again the example from [intro_agents]: a bot that answers user queries on a surf trip company.
 34 | Instead of letting the agent do 2 different calls for "travel distance API" and "weather API" each time they are asked about a new surf spot, you could just make one unified tool "return_spot_information", a functions that calls both APIs at once and returns their concatenated outputs to the user.
 35 | 
 36 | This will reduce costs, latency, and error risk!
 37 | 
 38 | The main guideline is: Reduce the number of LLM calls as much as you can.
 39 | 
 40 | This leads to a few takeaways:
 41 | - Whenever possible, group 2 tools in one, like in our example of the two APIs.
 42 | - Whenever possible, logic should be based on deterministic functions rather than agentic decisions.
 43 | 
 44 | ### Improve the information flow to the LLM engine
 45 | 
 46 | Remember that your LLM engine is like a ~intelligent~ robot, tapped into a room with the only communication with the outside world being notes passed under a door.
 47 | 
 48 | It won't know of anything that happened if you don't explicitly put that into its prompt.
 49 | 
 50 | So first start with making your task very clear!
 51 | Since an agent is powered by an LLM, minor variations in your task formulation might yield completely different results.
 52 | 
 53 | Then, improve the information flow towards your agent in tool use.
 54 | 
 55 | Particular guidelines to follow:
 56 | - Each tool should log (by simply using `print` statements inside the tool's `forward` method) everything that could be useful for the LLM engine.
 57 |   - In particular, logging detail on tool execution errors would help a lot!
 58 | 
 59 | For instance, here's a tool that :
 60 | 
 61 | First, here's a poor version:
 62 | ```python
 63 | import datetime
 64 | from smolagents import tool
 65 | 
 66 | def get_weather_report_at_coordinates(coordinates, date_time):
 67 |     # Dummy function, returns a list of [temperature in °C, risk of rain on a scale 0-1, wave height in m]
 68 |     return [28.0, 0.35, 0.85]
 69 | 
 70 | def get_coordinates_from_location(location):
 71 |     # Returns dummy coordinates
 72 |     return [3.3, -42.0]
 73 | 
 74 | @tool
 75 | def get_weather_api(location: str, date_time: str) -> str:
 76 |     """
 77 |     Returns the weather report.
 78 | 
 79 |     Args:
 80 |         location: the name of the place that you want the weather for.
 81 |         date_time: the date and time for which you want the report.
 82 |     """
 83 |     lon, lat = convert_location_to_coordinates(location)
 84 |     date_time = datetime.strptime(date_time)
 85 |     return str(get_weather_report_at_coordinates((lon, lat), date_time))
 86 | ```
 87 | 
 88 | Why is it bad?
 89 | - there's no precision of the format that should be used for `date_time`
 90 | - there's no detail on how location should
 91 | - there's no logging mechanism tying to explicit failure cases like location not being in a proper format, or date_time not being properly formatted.
 92 | - the output format is hard to understand
 93 | 
 94 | If the tool call fails, the error trace logged in memory can help the LLM reverse engineer the tool to fix the errors. But why leave it so much heavy lifting to do?
 95 | 
 96 | A better way to build this tool would have been the following:
 97 | ```python
 98 | @tool
 99 | def get_weather_api(location: str, date_time: str) -> str:
100 |     """
101 |     Returns the weather report.
102 | 
103 |     Args:
104 |         location: the name of the place that you want the weather for. Should be a place name, followed by possibly a city name, then a country, like "Anchor Point, Taghazout, Morocco".
105 |         date_time: the date and time for which you want the report, formatted as '%m/%d/%y %H:%M:%S'.
106 |     """
107 |     lon, lat = convert_location_to_coordinates(location)
108 |     try:
109 |         date_time = datetime.strptime(date_time)
110 |     except Exception as e:
111 |         raise ValueError("Conversion of `date_time` to datetime format failed, make sure to provide a string in format '%m/%d/%y %H:%M:%S'. Full trace:" + str(e))
112 |     temperature_celsius, risk_of_rain, wave_height = get_weather_report_at_coordinates((lon, lat), date_time)
113 |     return f"Weather report for {location}, {date_time}: Temperature will be {temperature_celsius}°C, risk of rain is {risk_of_rain*100:.0f}%, wave height is {wave_height}m."
114 | ```
115 | 
116 | In general, to ease the load on your LLM, the good question to ask yourself is: "How easy would it be for me, if I was dumb and using this tool for the first time ever, to program with this tool and correct my own errors?".
117 | 
118 | ### Give more arguments to the agent
119 | 
120 | To pass some additional objects to your agent than thes smple string that tells it the task to run, you can use argument `additional_args` to pass any type of object:
121 | 
122 | ```py
123 | from smolagents import CodeAgent, HfApiModel
124 | 
125 | model_id = "meta-llama/Llama-3.3-70B-Instruct"
126 | 
127 | agent = CodeAgent(tools=[], model=HfApiModel(model_id=model_id), add_base_tools=True)
128 | 
129 | agent.run(
130 |     "Why does Mike not know many people in New York?",
131 |     additional_args={"mp3_sound_file_url":'https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/recording.mp3'}
132 | )
133 | ```
134 | For instance, you can use this `additional_args` argument to pass images or strings that you want your agent to leverage.
135 | 
136 | 
137 | 
138 | ## How to debug your agent
139 | 
140 | ### 1. Use a stronger LLM
141 | 
142 | In an agentic workflows, some of the errors are actual errors, some other are the fault of your LLM engine not reasoning properly.
143 | For instance, consider this trace for an `CodeAgent` that I asked to make me a car picture:
144 | ```
145 | ==================================================================================================== New task ====================================================================================================
146 | Make me a cool car picture
147 | ──────────────────────────────────────────────────────────────────────────────────────────────────── New step ────────────────────────────────────────────────────────────────────────────────────────────────────
148 | Agent is executing the code below: ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
149 | image_generator(prompt="A cool, futuristic sports car with LED headlights, aerodynamic design, and vibrant color, high-res, photorealistic")
150 | ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
151 | 
152 | Last output from code snippet: ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
153 | /var/folders/6m/9b1tts6d5w960j80wbw9tx3m0000gn/T/tmpx09qfsdd/652f0007-3ee9-44e2-94ac-90dae6bb89a4.png
154 | Step 1:
155 | 
156 | - Time taken: 16.35 seconds
157 | - Input tokens: 1,383
158 | - Output tokens: 77
159 | ──────────────────────────────────────────────────────────────────────────────────────────────────── New step ────────────────────────────────────────────────────────────────────────────────────────────────────
160 | Agent is executing the code below: ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
161 | final_answer("/var/folders/6m/9b1tts6d5w960j80wbw9tx3m0000gn/T/tmpx09qfsdd/652f0007-3ee9-44e2-94ac-90dae6bb89a4.png")
162 | ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
163 | Print outputs:
164 | 
165 | Last output from code snippet: ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
166 | /var/folders/6m/9b1tts6d5w960j80wbw9tx3m0000gn/T/tmpx09qfsdd/652f0007-3ee9-44e2-94ac-90dae6bb89a4.png
167 | Final answer:
168 | /var/folders/6m/9b1tts6d5w960j80wbw9tx3m0000gn/T/tmpx09qfsdd/652f0007-3ee9-44e2-94ac-90dae6bb89a4.png
169 | ```
170 | The user sees, instead of an image being returned, a path being returned to them.
171 | It could look like a bug from the system, but actually the agentic system didn't cause the error: it's just that the LLM engine tid the mistake of not saving the image output into a variable.
172 | Thus it cannot access the image again except by leveraging the path that was logged while saving the image, so it returns the path instead of an image.
173 | 
174 | The first step to debugging your agent is thus "Use a more powerful LLM". Alternatives like `Qwen2/5-72B-Instruct` wouldn't have made that mistake.
175 | 
176 | ### 2. Provide more guidance / more information
177 | 
178 | Then you can also use less powerful models but guide them better.
179 | 
180 | Put yourself in the shoes if your model: if you were the model solving the task, would you struggle with the information available to you (from the system prompt + task formulation + tool description) ?
181 | 
182 | Would you need some added claritications ? 
183 | 
184 | To provide extra information, we do not recommend to change the system prompt right away: the default system prompt has many adjustments that you do not want to mess up except if you understand the prompt very well.
185 | Better ways to guide your LLM engine are:
186 | - If it 's about the task to solve: add all these details to the task. The task could be 100s of pages long.
187 | - If it's about how to use tools: the description attribute of your tools.
188 | 
189 | If after trying the above, you still want to change the system prompt, your new system prompt passed to `system_prompt` upon agent initialization needs to contain the following placeholders that will be used to insert certain automatically generated descriptions when running the agent:
190 | - `"{{tool_descriptions}}"` to insert tool descriptions.
191 | - `"{{managed_agents_description}}"` to insert the description for managed agents if there are any.
192 | - For `CodeAgent` only: `"{{authorized_imports}}"` to insert the list of authorized imports.
193 | 
194 | 
195 | ### 3. Extra planning
196 | 
197 | We provide a model for a supplementary planning step, that an agent can run regularly in-between normal action steps. In this step, there is no tool call, the LLM is simply asked to update a list of facts it knows and to reflect on what steps it should take next based on those facts.
198 | 
199 | ```py
200 | from smolagents import load_tool, CodeAgent, HfApiModel, DuckDuckGoSearchTool
201 | from dotenv import load_dotenv
202 | 
203 | load_dotenv()
204 | 
205 | # Import tool from Hub
206 | image_generation_tool = load_tool("m-ric/text-to-image", cache=False)
207 | 
208 | search_tool = DuckDuckGoSearchTool()
209 | 
210 | agent = CodeAgent(
211 |     tools=[search_tool],
212 |     model=HfApiModel("Qwen/Qwen2.5-72B-Instruct"),
213 |     planning_interval=3 # This is where you activate planning!
214 | )
215 | 
216 | # Run it!
217 | result = agent.run(
218 |     "How long would a cheetah at full speed take to run the length of Pont Alexandre III?",
219 | )
220 | ```


--------------------------------------------------------------------------------
/docs/source/en/tutorials/secure_code_execution.md:
--------------------------------------------------------------------------------
 1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
 2 | 
 3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 4 | the License. You may obtain a copy of the License at
 5 | 
 6 | http://www.apache.org/licenses/LICENSE-2.0
 7 | 
 8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
10 | specific language governing permissions and limitations under the License.
11 | 
12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
13 | rendered properly in your Markdown viewer.
14 | 
15 | -->
16 | # Secure code execution
17 | 
18 | [[open-in-colab]]
19 | 
20 | > [!TIP]
21 | > If you're new to building agents, make sure to first read the [intro to agents](../conceptual_guides/intro_agents) and the [guided tour of smolagents](../guided_tour).
22 | 
23 | ### Code agents
24 | 
25 | [Multiple](https://huggingface.co/papers/2402.01030) [research](https://huggingface.co/papers/2411.01747) [papers](https://huggingface.co/papers/2401.00812) have shown that having the LLM write its actions (the tool calls) in code is much better than the current standard format for tool calling, which is across the industry different shades of "writing actions as a JSON of tools names and arguments to use".
26 | 
27 | Why is code better? Well, because we crafted our code languages specifically to be great at expressing actions performed by a computer. If JSON snippets was a better way, this package would have been written in JSON snippets and the devil would be laughing at us.
28 | 
29 | Code is just a better way to express actions on a computer. It has better:
30 | - **Composability:** could you nest JSON actions within each other, or define a set of JSON actions to re-use later, the same way you could just define a python function?
31 | - **Object management:** how do you store the output of an action like `generate_image` in JSON?
32 | - **Generality:** code is built to express simply anything you can do have a computer do.
33 | - **Representation in LLM training corpuses:** why not leverage this benediction of the sky that plenty of quality actions have already been included in LLM training corpuses?
34 | 
35 | This is illustrated on the figure below, taken from [Executable Code Actions Elicit Better LLM Agents](https://huggingface.co/papers/2402.01030).
36 | 
37 | <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/code_vs_json_actions.png">
38 | 
39 | This is why we put emphasis on proposing code agents, in this case python agents, which meant putting higher effort on building secure python interpreters.
40 | 
41 | ### Local python interpreter
42 | 
43 | By default, the `CodeAgent` runs LLM-generated code in your environment.
44 | This execution is not done by the vanilla Python interpreter: we've re-built a more secure `LocalPythonInterpreter` from the ground up.
45 | This interpreter is designed for security by:
46 |  - Restricting the imports to a list explicitly passed by the user
47 |  - Capping the number of operations to prevent infinite loops and resource bloating.
48 |  - Will not perform any operation that's not pre-defined.
49 | 
50 | Wev'e used this on many use cases, without ever observing any damage to the environment. 
51 | 
52 | However this solution is not watertight: one could imagine occasions where LLMs fine-tuned for malignant actions could still hurt your environment. For instance if you've allowed an innocuous package like `Pillow` to process images, the LLM could generate thousands of saves of images to bloat your hard drive.
53 | It's certainly not likely if you've chosen the LLM engine yourself, but it could happen.
54 | 
55 | So if you want to be extra cautious, you can use the remote code execution option described below.
56 | 
57 | ### E2B code executor
58 | 
59 | For maximum security, you can use our integration with E2B to run code in a sandboxed environment. This is a remote execution service that runs your code in an isolated container, making it impossible for the code to affect your local environment.
60 | 
61 | For this, you will need to setup your E2B account and set your `E2B_API_KEY` in your environment variables. Head to [E2B's quickstart documentation](https://e2b.dev/docs/quickstart) for more information.
62 | 
63 | Then you can install it with `pip install e2b-code-interpreter python-dotenv`.
64 | 
65 | Now you're set!
66 | 
67 | To set the code executor to E2B, simply pass the flag `use_e2b_executor=True` when initializing your `CodeAgent`.
68 | Note that you should add all the tool's dependencies in `additional_authorized_imports`, so that the executor installs them.
69 | 
70 | ```py
71 | from smolagents import CodeAgent, VisitWebpageTool, HfApiModel
72 | agent = CodeAgent(
73 |     tools = [VisitWebpageTool()],
74 |     model=HfApiModel(),
75 |     additional_authorized_imports=["requests", "markdownify"],
76 |     use_e2b_executor=True
77 | )
78 | 
79 | agent.run("What was Abraham Lincoln's preferred pet?")
80 | ```
81 | 
82 | E2B code execution is not compatible with multi-agents at the moment - because having an agent call in a code blob that should be executed remotely is a mess. But we're working on adding it!


--------------------------------------------------------------------------------
/docs/source/en/tutorials/tools.md:
--------------------------------------------------------------------------------
  1 | <!--Copyright 2024 The HuggingFace Team. All rights reserved.
  2 | 
  3 | Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
  4 | the License. You may obtain a copy of the License at
  5 | 
  6 | http://www.apache.org/licenses/LICENSE-2.0
  7 | 
  8 | Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
  9 | an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 10 | specific language governing permissions and limitations under the License.
 11 | 
 12 | ⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
 13 | rendered properly in your Markdown viewer.
 14 | 
 15 | -->
 16 | # Tools
 17 | 
 18 | [[open-in-colab]]
 19 | 
 20 | Here, we're going to see advanced tool usage.
 21 | 
 22 | > [!TIP]
 23 | > If you're new to building agents, make sure to first read the [intro to agents](../conceptual_guides/intro_agents) and the [guided tour of smolagents](../guided_tour).
 24 | 
 25 | - [Tools](#tools)
 26 |     - [What is a tool, and how to build one?](#what-is-a-tool-and-how-to-build-one)
 27 |     - [Share your tool to the Hub](#share-your-tool-to-the-hub)
 28 |     - [Import a Space as a tool](#import-a-space-as-a-tool)
 29 |     - [Use LangChain tools](#use-langchain-tools)
 30 |     - [Manage your agent's toolbox](#manage-your-agents-toolbox)
 31 |     - [Use a collection of tools](#use-a-collection-of-tools)
 32 | 
 33 | ### What is a tool, and how to build one?
 34 | 
 35 | A tool is mostly a function that an LLM can use in an agentic system.
 36 | 
 37 | But to use it, the LLM will need to be given an API: name, tool description, input types and descriptions, output type.
 38 | 
 39 | So it cannot be only a function. It should be a class.
 40 | 
 41 | So at core, the tool is a class that wraps a function with metadata that helps the LLM understand how to use it.
 42 | 
 43 | Here's how it looks:
 44 | 
 45 | ```python
 46 | from smolagents import Tool
 47 | 
 48 | class HFModelDownloadsTool(Tool):
 49 |     name = "model_download_counter"
 50 |     description = """
 51 |     This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
 52 |     It returns the name of the checkpoint."""
 53 |     inputs = {
 54 |         "task": {
 55 |             "type": "string",
 56 |             "description": "the task category (such as text-classification, depth-estimation, etc)",
 57 |         }
 58 |     }
 59 |     output_type = "string"
 60 | 
 61 |     def forward(self, task: str):
 62 |         from huggingface_hub import list_models
 63 | 
 64 |         model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
 65 |         return model.id
 66 | 
 67 | model_downloads_tool = HFModelDownloadsTool()
 68 | ```
 69 | 
 70 | The custom tool subclasses [`Tool`] to inherit useful methods. The child class also defines:
 71 | - An attribute `name`, which corresponds to the name of the tool itself. The name usually describes what the tool does. Since the code returns the model with the most downloads for a task, let's name it `model_download_counter`.
 72 | - An attribute `description` is used to populate the agent's system prompt.
 73 | - An `inputs` attribute, which is a dictionary with keys `"type"` and `"description"`. It contains information that helps the Python interpreter make educated choices about the input.
 74 | - An `output_type` attribute, which specifies the output type. The types for both `inputs` and `output_type` should be [Pydantic formats](https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema), they can be either of these: [`~AUTHORIZED_TYPES`].
 75 | - A `forward` method which contains the inference code to be executed.
 76 | 
 77 | And that's all it needs to be used in an agent!
 78 | 
 79 | There's another way to build a tool. In the [guided_tour](../guided_tour), we implemented a tool using the `@tool` decorator. The [`tool`] decorator is the recommended way to define simple tools, but sometimes you need more than this: using several methods in a class for more clarity, or using additional class attributes.
 80 | 
 81 | In this case, you can build your tool by subclassing [`Tool`] as described above.
 82 | 
 83 | ### Share your tool to the Hub
 84 | 
 85 | You can share your custom tool to the Hub by calling [`~Tool.push_to_hub`] on the tool. Make sure you've created a repository for it on the Hub and are using a token with read access.
 86 | 
 87 | ```python
 88 | model_downloads_tool.push_to_hub("{your_username}/hf-model-downloads", token="<YOUR_HUGGINGFACEHUB_API_TOKEN>")
 89 | ```
 90 | 
 91 | For the push to Hub to work, your tool will need to respect some rules:
 92 | - All method are self-contained, e.g. use variables that come either from their args.
 93 | - As per the above point, **all imports should be defined directky within the tool's functions**, else you will get an error when trying to call [`~Tool.save`] or [`~Tool.push_to_hub`] with your custom tool.
 94 | - If you subclass the `__init__` method, you can give it no other argument than `self`. This is because arguments set during a specific tool instance's initialization are hard to track, which prevents from sharing them properly to the hub. And anyway, the idea of making a specific class is that you can already set class attributes for anything you need to hard-code (just set `your_variable=(...)` directly under the `class YourTool(Tool):` line). And of course you can still create a class attribute anywhere in your code by assigning stuff to `self.your_variable`.
 95 | 
 96 | 
 97 | Once your tool is pushed to Hub, you can visualize it. [Here](https://huggingface.co/spaces/m-ric/hf-model-downloads) is the `model_downloads_tool` that I've pushed. It has a nice gradio interface.
 98 | 
 99 | When diving into the tool files, you can find that all the tool's logic is under [tool.py](https://huggingface.co/spaces/m-ric/hf-model-downloads/blob/main/tool.py). That is where you can inspect a tool shared by someone else.
100 | 
101 | Then you can load the tool with [`load_tool`] or create it with [`~Tool.from_hub`] and pass it to the `tools` parameter in your agent.
102 | Since running tools means running custom code, you need to make sure you trust the repository, thus we require to pass `trust_remote_code=True` to load a tool from the Hub.
103 | 
104 | ```python
105 | from smolagents import load_tool, CodeAgent
106 | 
107 | model_download_tool = load_tool(
108 |     "{your_username}/hf-model-downloads",
109 |     trust_remote_code=True
110 | )
111 | ```
112 | 
113 | ### Import a Space as a tool
114 | 
115 | You can directly import a Space from the Hub as a tool using the [`Tool.from_space`] method!
116 | 
117 | You only need to provide the id of the Space on the Hub, its name, and a description that will help you agent understand what the tool does. Under the hood, this will use [`gradio-client`](https://pypi.org/project/gradio-client/) library to call the Space.
118 | 
119 | For instance, let's import the [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) Space from the Hub and use it to generate an image.
120 | 
121 | ```python
122 | image_generation_tool = Tool.from_space(
123 |     "black-forest-labs/FLUX.1-schnell",
124 |     name="image_generator",
125 |     description="Generate an image from a prompt"
126 | )
127 | 
128 | image_generation_tool("A sunny beach")
129 | ```
130 | And voilà, here's your image! 🏖️
131 | 
132 | <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/sunny_beach.webp">
133 | 
134 | Then you can use this tool just like any other tool.  For example, let's improve the prompt  `a rabbit wearing a space suit` and generate an image of it.
135 | 
136 | ```python
137 | from smolagents import CodeAgent, HfApiModel
138 | 
139 | model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
140 | agent = CodeAgent(tools=[image_generation_tool], model=model)
141 | 
142 | agent.run(
143 |     "Improve this prompt, then generate an image of it.", prompt='A rabbit wearing a space suit'
144 | )
145 | ```
146 | 
147 | ```text
148 | === Agent thoughts:
149 | improved_prompt could be "A bright blue space suit wearing rabbit, on the surface of the moon, under a bright orange sunset, with the Earth visible in the background"
150 | 
151 | Now that I have improved the prompt, I can use the image generator tool to generate an image based on this prompt.
152 | >>> Agent is executing the code below:
153 | image = image_generator(prompt="A bright blue space suit wearing rabbit, on the surface of the moon, under a bright orange sunset, with the Earth visible in the background")
154 | final_answer(image)
155 | ```
156 | 
157 | <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/rabbit_spacesuit_flux.webp">
158 | 
159 | How cool is this? 🤩
160 | 
161 | ### Use LangChain tools
162 | 
163 | We love Langchain and think it has a very compelling suite of tools.
164 | To import a tool from LangChain, use the `from_langchain()` method.
165 | 
166 | Here is how you can use it to recreate the intro's search result using a LangChain web search tool.
167 | This tool will need `pip install langchain google-search-results -q` to work properly.
168 | ```python
169 | from langchain.agents import load_tools
170 | 
171 | search_tool = Tool.from_langchain(load_tools(["serpapi"])[0])
172 | 
173 | agent = CodeAgent(tools=[search_tool], model=model)
174 | 
175 | agent.run("How many more blocks (also denoted as layers) are in BERT base encoder compared to the encoder from the architecture proposed in Attention is All You Need?")
176 | ```
177 | 
178 | ### Manage your agent's toolbox
179 | 
180 | You can manage an agent's toolbox by adding or replacing a tool.
181 | 
182 | Let's add the `model_download_tool` to an existing agent initialized with only the default toolbox.
183 | 
184 | ```python
185 | from smolagents import HfApiModel
186 | 
187 | model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
188 | 
189 | agent = CodeAgent(tools=[], model=model, add_base_tools=True)
190 | agent.toolbox.add_tool(model_download_tool)
191 | ```
192 | Now we can leverage the new tool:
193 | 
194 | ```python
195 | agent.run(
196 |     "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub but reverse the letters?"
197 | )
198 | ```
199 | 
200 | 
201 | > [!TIP]
202 | > Beware of not adding too many tools to an agent: this can overwhelm weaker LLM engines.
203 | 
204 | 
205 | Use the `agent.toolbox.update_tool()` method to replace an existing tool in the agent's toolbox.
206 | This is useful if your new tool is a one-to-one replacement of the existing tool because the agent already knows how to perform that specific task.
207 | Just make sure the new tool follows the same API as the replaced tool or adapt the system prompt template to ensure all examples using the replaced tool are updated.
208 | 
209 | 
210 | ### Use a collection of tools
211 | 
212 | You can leverage tool collections by using the ToolCollection object, with the slug of the collection you want to use.
213 | Then pass them as a list to initialize you agent, and start using them!
214 | 
215 | ```py
216 | from transformers import ToolCollection, CodeAgent
217 | 
218 | image_tool_collection = ToolCollection(
219 |     collection_slug="huggingface-tools/diffusion-tools-6630bb19a942c2306a2cdb6f",
220 |     token="<YOUR_HUGGINGFACEHUB_API_TOKEN>"
221 | )
222 | agent = CodeAgent(tools=[*image_tool_collection.tools], model=model, add_base_tools=True)
223 | 
224 | agent.run("Please draw me a picture of rivers and lakes.")
225 | ```
226 | 
227 | To speed up the start, tools are loaded only if called by the agent.


--------------------------------------------------------------------------------
/e2b.Dockerfile:
--------------------------------------------------------------------------------
1 | # You can use most Debian-based base images
2 | FROM e2bdev/code-interpreter:latest 
3 | 
4 | # Install dependencies and customize sandbox
5 | RUN pip install git+https://github.com/huggingface/smolagents.git


--------------------------------------------------------------------------------
/e2b.toml:
--------------------------------------------------------------------------------
 1 | # This is a config for E2B sandbox template.
 2 | # You can use template ID (qywp2ctmu2q7jzprcf4j) to create a sandbox:
 3 | 
 4 | # Python SDK
 5 | # from e2b import Sandbox, AsyncSandbox
 6 | # sandbox = Sandbox("qywp2ctmu2q7jzprcf4j") # Sync sandbox
 7 | # sandbox = await AsyncSandbox.create("qywp2ctmu2q7jzprcf4j") # Async sandbox
 8 | 
 9 | # JS SDK
10 | # import { Sandbox } from 'e2b'
11 | # const sandbox = await Sandbox.create('qywp2ctmu2q7jzprcf4j')
12 | 
13 | team_id = "f8776d3a-df2f-4a1d-af48-68c2e13b3b87"
14 | start_cmd = "/root/.jupyter/start-up.sh"
15 | dockerfile = "e2b.Dockerfile"
16 | template_id = "qywp2ctmu2q7jzprcf4j"
17 | 


--------------------------------------------------------------------------------
/examples/e2b_example.py:
--------------------------------------------------------------------------------
 1 | from smolagents import Tool, CodeAgent, HfApiModel
 2 | from smolagents.default_tools import VisitWebpageTool
 3 | from dotenv import load_dotenv
 4 | 
 5 | load_dotenv()
 6 | 
 7 | class GetCatImageTool(Tool):
 8 |     name="get_cat_image"
 9 |     description = "Get a cat image"
10 |     inputs = {}
11 |     output_type = "image"
12 | 
13 |     def __init__(self):
14 |         super().__init__()
15 |         self.url = "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png"
16 | 
17 |     def forward(self):
18 |         from PIL import Image
19 |         import requests
20 |         from io import BytesIO
21 | 
22 |         response = requests.get(self.url)
23 | 
24 |         return Image.open(BytesIO(response.content))
25 | 
26 | 
27 | get_cat_image = GetCatImageTool()
28 | 
29 | agent = CodeAgent(
30 |     tools = [get_cat_image, VisitWebpageTool()],
31 |     model=HfApiModel(),
32 |     additional_authorized_imports=["Pillow", "requests", "markdownify"], # "duckduckgo-search", 
33 |     use_e2b_executor=True
34 | )
35 | 
36 | agent.run(
37 |     "Return me an image of a cat. Directly use the image provided in your state.", additional_args={"cat_image":get_cat_image()}
38 | ) # Asking to directly return the image from state tests that additional_args are properly sent to server.
39 | 
40 | # Try the agent in a Gradio UI
41 | from smolagents import GradioUI
42 | 
43 | GradioUI(agent).launch()


--------------------------------------------------------------------------------
/examples/rag.py:
--------------------------------------------------------------------------------
 1 | # from huggingface_hub import login
 2 | 
 3 | # login()
 4 | import datasets
 5 | from langchain.docstore.document import Document
 6 | from langchain.text_splitter import RecursiveCharacterTextSplitter
 7 | from langchain_community.retrievers import BM25Retriever
 8 | 
 9 | 
10 | knowledge_base = datasets.load_dataset("m-ric/huggingface_doc", split="train")
11 | knowledge_base = knowledge_base.filter(lambda row: row["source"].startswith("huggingface/transformers"))
12 | 
13 | source_docs = [
14 |     Document(page_content=doc["text"], metadata={"source": doc["source"].split("/")[1]})
15 |     for doc in knowledge_base
16 | ]
17 | 
18 | text_splitter = RecursiveCharacterTextSplitter(
19 |     chunk_size=500,
20 |     chunk_overlap=50,
21 |     add_start_index=True,
22 |     strip_whitespace=True,
23 |     separators=["\n\n", "\n", ".", " ", ""],
24 | )
25 | docs_processed = text_splitter.split_documents(source_docs)
26 | 
27 | from smolagents import Tool
28 | 
29 | class RetrieverTool(Tool):
30 |     name = "retriever"
31 |     description = "Uses semantic search to retrieve the parts of transformers documentation that could be most relevant to answer your query."
32 |     inputs = {
33 |         "query": {
34 |             "type": "string",
35 |             "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
36 |         }
37 |     }
38 |     output_type = "string"
39 | 
40 |     def __init__(self, docs, **kwargs):
41 |         super().__init__(**kwargs)
42 |         self.retriever = BM25Retriever.from_documents(
43 |             docs, k=10
44 |         )
45 | 
46 |     def forward(self, query: str) -> str:
47 |         assert isinstance(query, str), "Your search query must be a string"
48 | 
49 |         docs = self.retriever.invoke(
50 |             query,
51 |         )
52 |         return "\nRetrieved documents:\n" + "".join(
53 |             [
54 |                 f"\n\n===== Document {str(i)} =====\n" + doc.page_content
55 |                 for i, doc in enumerate(docs)
56 |             ]
57 |         )
58 | 
59 | from smolagents import HfApiModel, CodeAgent
60 | 
61 | retriever_tool = RetrieverTool(docs_processed)
62 | agent = CodeAgent(
63 |     tools=[retriever_tool], model=HfApiModel("meta-llama/Llama-3.3-70B-Instruct"), max_iterations=4, verbose=True
64 | )
65 | 
66 | agent_output = agent.run("For a transformers model training, which is slower, the forward or the backward pass?")
67 | 
68 | print("Final output:")
69 | print(agent_output)
70 | 


--------------------------------------------------------------------------------
/examples/text_to_sql.py:
--------------------------------------------------------------------------------
 1 | from sqlalchemy import (
 2 |     create_engine,
 3 |     MetaData,
 4 |     Table,
 5 |     Column,
 6 |     String,
 7 |     Integer,
 8 |     Float,
 9 |     insert,
10 |     inspect,
11 |     text,
12 | )
13 | 
14 | engine = create_engine("sqlite:///:memory:")
15 | metadata_obj = MetaData()
16 | 
17 | # create city SQL table
18 | table_name = "receipts"
19 | receipts = Table(
20 |     table_name,
21 |     metadata_obj,
22 |     Column("receipt_id", Integer, primary_key=True),
23 |     Column("customer_name", String(16), primary_key=True),
24 |     Column("price", Float),
25 |     Column("tip", Float),
26 | )
27 | metadata_obj.create_all(engine)
28 | 
29 | rows = [
30 |     {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
31 |     {"receipt_id": 2, "customer_name": "Alex Mason", "price": 23.86, "tip": 0.24},
32 |     {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
33 |     {"receipt_id": 4, "customer_name": "Margaret James", "price": 21.11, "tip": 1.00},
34 | ]
35 | for row in rows:
36 |     stmt = insert(receipts).values(**row)
37 |     with engine.begin() as connection:
38 |         cursor = connection.execute(stmt)
39 | 
40 | inspector = inspect(engine)
41 | columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]
42 | 
43 | table_description = "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
44 | print(table_description)
45 | 
46 | from smolagents import tool
47 | 
48 | @tool
49 | def sql_engine(query: str) -> str:
50 |     """
51 |     Allows you to perform SQL queries on the table. Returns a string representation of the result.
52 |     The table is named 'receipts'. Its description is as follows:
53 |         Columns:
54 |         - receipt_id: INTEGER
55 |         - customer_name: VARCHAR(16)
56 |         - price: FLOAT
57 |         - tip: FLOAT
58 | 
59 |     Args:
60 |         query: The query to perform. This should be correct SQL.
61 |     """
62 |     output = ""
63 |     with engine.connect() as con:
64 |         rows = con.execute(text(query))
65 |         for row in rows:
66 |             output += "\n" + str(row)
67 |     return output
68 | 
69 | from smolagents import CodeAgent, HfApiModel
70 | 
71 | agent = CodeAgent(
72 |     tools=[sql_engine],
73 |     model=HfApiModel("meta-llama/Meta-Llama-3.1-8B-Instruct"),
74 | )
75 | agent.run("Can you give me the name of the client who got the most expensive receipt?")


--------------------------------------------------------------------------------
/examples/tool_calling_agent_from_any_llm.py:
--------------------------------------------------------------------------------
 1 | from smolagents.agents import ToolCallingAgent
 2 | from smolagents import tool, HfApiModel, TransformersModel, LiteLLMModel
 3 | from typing import Optional
 4 | 
 5 | # Choose which LLM engine to use!
 6 | # model = HfApiModel(model_id="meta-llama/Llama-3.3-70B-Instruct")
 7 | # model = TransformersModel(model_id="meta-llama/Llama-3.2-2B-Instruct")
 8 | 
 9 | # For anthropic: change model_id below to 'anthropic/claude-3-5-sonnet-20240620'
10 | model = LiteLLMModel(model_id="gpt-4o")
11 | 
12 | @tool
13 | def get_weather(location: str, celsius: Optional[bool] = False) -> str:
14 |     """
15 |     Get weather in the next days at given location.
16 |     Secretly this tool does not care about the location, it hates the weather everywhere.
17 | 
18 |     Args:
19 |         location: the location
20 |         celsius: the temperature
21 |     """
22 |     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
23 | 
24 | agent = ToolCallingAgent(tools=[get_weather], model=model)
25 | 
26 | print(agent.run("What's the weather like in Paris?"))


--------------------------------------------------------------------------------
/examples/tool_calling_agent_ollama.py:
--------------------------------------------------------------------------------
 1 | from smolagents.agents import ToolCallingAgent
 2 | from smolagents import tool, LiteLLMModel
 3 | from typing import Optional
 4 | 
 5 | model = LiteLLMModel(
 6 |     model_id="ollama_chat/llama3.2",
 7 |     api_base="http://localhost:11434/v1", # replace with remote open-ai compatible server if necessary
 8 |     api_key="your-api-key" # replace with API key if necessary
 9 | )
10 | 
11 | @tool
12 | def get_weather(location: str, celsius: Optional[bool] = False) -> str:
13 |     """
14 |     Get weather in the next days at given location.
15 |     Secretly this tool does not care about the location, it hates the weather everywhere.
16 | 
17 |     Args:
18 |         location: the location
19 |         celsius: the temperature
20 |     """
21 |     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
22 | 
23 | agent = ToolCallingAgent(tools=[get_weather], model=model)
24 | 
25 | print(agent.run("What's the weather like in Paris?"))


--------------------------------------------------------------------------------
/package.json:
--------------------------------------------------------------------------------
1 | {
2 |   "dependencies": {
3 |     "@e2b/cli": "^1.0.9"
4 |   }
5 | }
6 | 


--------------------------------------------------------------------------------
/pyproject.toml:
--------------------------------------------------------------------------------
 1 | [build-system]
 2 | requires = ["setuptools"]
 3 | build-backend = "setuptools.build_meta"
 4 | 
 5 | [project]
 6 | name = "smolagents"
 7 | version = "1.1.0.dev0"
 8 | description = "🤗 smolagents: a barebones library for agents. Agents write python code to call tools or orchestrate other agents."
 9 | authors = [
10 |   { name="Aymeric Roucher", email="aymeric@hf.co" }, { name="Thomas Wolf"},
11 | ]
12 | readme = "README.md"
13 | requires-python = ">=3.10"
14 | dependencies = [
15 |     "torch",
16 |     "torchaudio",
17 |     "torchvision",
18 |     "transformers>=4.0.0",
19 |     "requests>=2.32.3",
20 |     "rich>=13.9.4",
21 |     "pandas>=2.2.3",
22 |     "jinja2>=3.1.4",
23 |     "pillow>=11.0.0",
24 |     "markdownify>=0.14.1",
25 |     "gradio>=5.8.0",
26 |     "duckduckgo-search>=6.3.7",
27 |     "python-dotenv>=1.0.1",
28 |     "e2b-code-interpreter>=1.0.3",
29 |     "litellm>=1.55.10",
30 | ]
31 | 
32 | [project.optional-dependencies]
33 | test = [
34 |     "pytest>=8.1.0",
35 |     "sqlalchemy"
36 | ]
37 | 


--------------------------------------------------------------------------------
/server.py:
--------------------------------------------------------------------------------
 1 | import socket
 2 | import sys
 3 | import traceback
 4 | import io
 5 | 
 6 | exec_globals = {}
 7 | exec_locals = {}
 8 | 
 9 | def execute_code(code):
10 |     stdout = io.StringIO()
11 |     stderr = io.StringIO()
12 |     sys.stdout = stdout
13 |     sys.stderr = stderr
14 | 
15 |     try:
16 |         exec(code, exec_globals, exec_locals)
17 |     except Exception as e:
18 |         traceback.print_exc(file=stderr)
19 |     
20 |     output = stdout.getvalue()
21 |     error = stderr.getvalue()
22 | 
23 |     # Restore original stdout and stderr
24 |     sys.stdout = sys.__stdout__
25 |     sys.stderr = sys.__stderr__
26 | 
27 |     return output + error
28 | 
29 | def start_server(host='0.0.0.0', port=65432):
30 |     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
31 |         s.bind((host, port))
32 |         s.listen()
33 |         print(f"Server listening on {host}:{port}")
34 |         while True:
35 |             conn, addr = s.accept()
36 |             with conn:
37 |                 print(f"Connected by {addr}")
38 |                 data = conn.recv(1024)
39 |                 if not data:
40 |                     break
41 |                 code = data.decode('utf-8')
42 |                 output = execute_code(code)
43 |                 conn.sendall(output.encode('utf-8'))
44 | 
45 | if __name__ == "__main__":
46 |     start_server() 


--------------------------------------------------------------------------------
/src/smolagents/__init__.py:
--------------------------------------------------------------------------------
 1 | #!/usr/bin/env python
 2 | # coding=utf-8
 3 | 
 4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
 5 | #
 6 | # Licensed under the Apache License, Version 2.0 (the "License");
 7 | # you may not use this file except in compliance with the License.
 8 | # You may obtain a copy of the License at
 9 | #
10 | #     http://www.apache.org/licenses/LICENSE-2.0
11 | #
12 | # Unless required by applicable law or agreed to in writing, software
13 | # distributed under the License is distributed on an "AS IS" BASIS,
14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
15 | # See the License for the specific language governing permissions and
16 | # limitations under the License.
17 | __version__ = "1.1.0.dev0"
18 | 
19 | from typing import TYPE_CHECKING
20 | 
21 | from transformers.utils import _LazyModule
22 | from transformers.utils.import_utils import define_import_structure
23 | 
24 | 
25 | if TYPE_CHECKING:
26 |     from .agents import *
27 |     from .default_tools import *
28 |     from .gradio_ui import *
29 |     from .models import *
30 |     from .local_python_executor import *
31 |     from .e2b_executor import *
32 |     from .monitoring import *
33 |     from .prompts import *
34 |     from .tools import *
35 |     from .types import *
36 |     from .utils import *
37 | 
38 | 
39 | else:
40 |     import sys
41 | 
42 |     _file = globals()["__file__"]
43 |     import_structure = define_import_structure(_file)
44 |     import_structure[""] = {"__version__": __version__}
45 |     sys.modules[__name__] = _LazyModule(
46 |         __name__,
47 |         _file,
48 |         import_structure,
49 |         module_spec=__spec__,
50 |         extra_objects={"__version__": __version__},
51 |     )
52 | 


--------------------------------------------------------------------------------
/src/smolagents/default_tools.py:
--------------------------------------------------------------------------------
  1 | #!/usr/bin/env python
  2 | # coding=utf-8
  3 | 
  4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
  5 | #
  6 | # Licensed under the Apache License, Version 2.0 (the "License");
  7 | # you may not use this file except in compliance with the License.
  8 | # You may obtain a copy of the License at
  9 | #
 10 | #     http://www.apache.org/licenses/LICENSE-2.0
 11 | #
 12 | # Unless required by applicable law or agreed to in writing, software
 13 | # distributed under the License is distributed on an "AS IS" BASIS,
 14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 15 | # See the License for the specific language governing permissions and
 16 | # limitations under the License.
 17 | import json
 18 | import re
 19 | from dataclasses import dataclass
 20 | from typing import Dict, Optional
 21 | from huggingface_hub import hf_hub_download, list_spaces
 22 | 
 23 | from transformers.utils import is_offline_mode
 24 | from transformers.models.whisper import (
 25 |     WhisperProcessor,
 26 |     WhisperForConditionalGeneration,
 27 | )
 28 | 
 29 | from .local_python_executor import (
 30 |     BASE_BUILTIN_MODULES,
 31 |     BASE_PYTHON_TOOLS,
 32 |     evaluate_python_code,
 33 | )
 34 | from .tools import TOOL_CONFIG_FILE, Tool, PipelineTool
 35 | from .types import AgentAudio
 36 | 
 37 | 
 38 | @dataclass
 39 | class PreTool:
 40 |     name: str
 41 |     inputs: Dict[str, str]
 42 |     output_type: type
 43 |     task: str
 44 |     description: str
 45 |     repo_id: str
 46 | 
 47 | 
 48 | def get_remote_tools(logger, organization="huggingface-tools"):
 49 |     if is_offline_mode():
 50 |         logger.info("You are in offline mode, so remote tools are not available.")
 51 |         return {}
 52 | 
 53 |     spaces = list_spaces(author=organization)
 54 |     tools = {}
 55 |     for space_info in spaces:
 56 |         repo_id = space_info.id
 57 |         resolved_config_file = hf_hub_download(
 58 |             repo_id, TOOL_CONFIG_FILE, repo_type="space"
 59 |         )
 60 |         with open(resolved_config_file, encoding="utf-8") as reader:
 61 |             config = json.load(reader)
 62 |         task = repo_id.split("/")[-1]
 63 |         tools[config["name"]] = PreTool(
 64 |             task=task,
 65 |             description=config["description"],
 66 |             repo_id=repo_id,
 67 |             name=task,
 68 |             inputs=config["inputs"],
 69 |             output_type=config["output_type"],
 70 |         )
 71 | 
 72 |     return tools
 73 | 
 74 | 
 75 | class PythonInterpreterTool(Tool):
 76 |     name = "python_interpreter"
 77 |     description = "This is a tool that evaluates python code. It can be used to perform calculations."
 78 |     inputs = {
 79 |         "code": {
 80 |             "type": "string",
 81 |             "description": "The python code to run in interpreter",
 82 |         }
 83 |     }
 84 |     output_type = "string"
 85 | 
 86 |     def __init__(self, *args, authorized_imports=None, **kwargs):
 87 |         if authorized_imports is None:
 88 |             self.authorized_imports = list(set(BASE_BUILTIN_MODULES))
 89 |         else:
 90 |             self.authorized_imports = list(
 91 |                 set(BASE_BUILTIN_MODULES) | set(authorized_imports)
 92 |             )
 93 |         self.inputs = {
 94 |             "code": {
 95 |                 "type": "string",
 96 |                 "description": (
 97 |                     "The code snippet to evaluate. All variables used in this snippet must be defined in this same snippet, "
 98 |                     f"else you will get an error. This code can only import the following python libraries: {authorized_imports}."
 99 |                 ),
100 |             }
101 |         }
102 |         self.base_python_tools = BASE_PYTHON_TOOLS
103 |         self.python_evaluator = evaluate_python_code
104 |         super().__init__(*args, **kwargs)
105 | 
106 |     def forward(self, code: str) -> str:
107 |         state = {}
108 |         try:
109 |             output = str(
110 |                 self.python_evaluator(
111 |                     code,
112 |                     state=state,
113 |                     static_tools=self.base_python_tools,
114 |                     authorized_imports=self.authorized_imports,
115 |                 )
116 |             )
117 |             return f"Stdout:\n{state['print_outputs']}\nOutput: {output}"
118 |         except Exception as e:
119 |             return f"Error: {str(e)}"
120 | 
121 | 
122 | class FinalAnswerTool(Tool):
123 |     name = "final_answer"
124 |     description = "Provides a final answer to the given problem."
125 |     inputs = {
126 |         "answer": {"type": "any", "description": "The final answer to the problem"}
127 |     }
128 |     output_type = "any"
129 | 
130 |     def forward(self, answer):
131 |         return answer
132 | 
133 | 
134 | class UserInputTool(Tool):
135 |     name = "user_input"
136 |     description = "Asks for user's input on a specific question"
137 |     inputs = {
138 |         "question": {"type": "string", "description": "The question to ask the user"}
139 |     }
140 |     output_type = "string"
141 | 
142 |     def forward(self, question):
143 |         user_input = input(f"{question} => ")
144 |         return user_input
145 | 
146 | 
147 | class DuckDuckGoSearchTool(Tool):
148 |     name = "web_search"
149 |     description = """Performs a duckduckgo web search based on your query (think a Google search) then returns the top search results as a list of dict elements.
150 |     Each result has keys 'title', 'href' and 'body'."""
151 |     inputs = {
152 |         "query": {"type": "string", "description": "The search query to perform."}
153 |     }
154 |     output_type = "any"
155 | 
156 |     def __init__(self, **kwargs):
157 |         super().__init__(self, **kwargs)
158 |         try:
159 |             from duckduckgo_search import DDGS
160 |         except ImportError:
161 |             raise ImportError(
162 |                 "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
163 |             )
164 |         self.ddgs = DDGS()
165 | 
166 |     def forward(self, query: str) -> str:
167 |         results = self.ddgs.text(query, max_results=10)
168 |         postprocessed_results = [
169 |             f"[{result['title']}]({result['href']})\n{result['body']}"
170 |             for result in results
171 |         ]
172 |         return "## Search Results\n\n" + "\n\n".join(postprocessed_results)
173 | 
174 | 
175 | class GoogleSearchTool(Tool):
176 |     name = "web_search"
177 |     description = """Performs a google web search for your query then returns a string of the top search results."""
178 |     inputs = {
179 |         "query": {"type": "string", "description": "The search query to perform."},
180 |         "filter_year": {
181 |             "type": "integer",
182 |             "description": "Optionally restrict results to a certain year",
183 |             "nullable": True,
184 |         },
185 |     }
186 |     output_type = "string"
187 | 
188 |     def __init__(self):
189 |         super().__init__(self)
190 |         import os
191 | 
192 |         self.serpapi_key = os.getenv("SERPAPI_API_KEY")
193 | 
194 |     def forward(self, query: str, filter_year: Optional[int] = None) -> str:
195 |         import requests
196 | 
197 |         if self.serpapi_key is None:
198 |             raise ValueError(
199 |                 "Missing SerpAPI key. Make sure you have 'SERPAPI_API_KEY' in your env variables."
200 |             )
201 | 
202 |         params = {
203 |             "engine": "google",
204 |             "q": query,
205 |             "api_key": self.serpapi_key,
206 |             "google_domain": "google.com",
207 |         }
208 |         if filter_year is not None:
209 |             params["tbs"] = (
210 |                 f"cdr:1,cd_min:01/01/{filter_year},cd_max:12/31/{filter_year}"
211 |             )
212 | 
213 |         response = requests.get("https://serpapi.com/search.json", params=params)
214 | 
215 |         if response.status_code == 200:
216 |             results = response.json()
217 |         else:
218 |             raise ValueError(response.json())
219 | 
220 |         if "organic_results" not in results.keys():
221 |             if filter_year is not None:
222 |                 raise Exception(
223 |                     f"'organic_results' key not found for query: '{query}' with filtering on year={filter_year}. Use a less restrictive query or do not filter on year."
224 |                 )
225 |             else:
226 |                 raise Exception(
227 |                     f"'organic_results' key not found for query: '{query}'. Use a less restrictive query."
228 |                 )
229 |         if len(results["organic_results"]) == 0:
230 |             year_filter_message = (
231 |                 f" with filter year={filter_year}" if filter_year is not None else ""
232 |             )
233 |             return f"No results found for '{query}'{year_filter_message}. Try with a more general query, or remove the year filter."
234 | 
235 |         web_snippets = []
236 |         if "organic_results" in results:
237 |             for idx, page in enumerate(results["organic_results"]):
238 |                 date_published = ""
239 |                 if "date" in page:
240 |                     date_published = "\nDate published: " + page["date"]
241 | 
242 |                 source = ""
243 |                 if "source" in page:
244 |                     source = "\nSource: " + page["source"]
245 | 
246 |                 snippet = ""
247 |                 if "snippet" in page:
248 |                     snippet = "\n" + page["snippet"]
249 | 
250 |                 redacted_version = f"{idx}. [{page['title']}]({page['link']}){date_published}{source}\n{snippet}"
251 | 
252 |                 redacted_version = redacted_version.replace(
253 |                     "Your browser can't play this video.", ""
254 |                 )
255 |                 web_snippets.append(redacted_version)
256 | 
257 |         return "## Search Results\n" + "\n\n".join(web_snippets)
258 | 
259 | 
260 | class VisitWebpageTool(Tool):
261 |     name = "visit_webpage"
262 |     description = "Visits a webpage at the given url and reads its content as a markdown string. Use this to browse webpages."
263 |     inputs = {
264 |         "url": {
265 |             "type": "string",
266 |             "description": "The url of the webpage to visit.",
267 |         }
268 |     }
269 |     output_type = "string"
270 | 
271 |     def forward(self, url: str) -> str:
272 |         try:
273 |             from markdownify import markdownify
274 |             import requests
275 |             from requests.exceptions import RequestException
276 |         except ImportError:
277 |             raise ImportError(
278 |                 "You must install packages `markdownify` and `requests` to run this tool: for instance run `pip install markdownify requests`."
279 |             )
280 |         try:
281 |             # Send a GET request to the URL
282 |             response = requests.get(url)
283 |             response.raise_for_status()  # Raise an exception for bad status codes
284 | 
285 |             # Convert the HTML content to Markdown
286 |             markdown_content = markdownify(response.text).strip()
287 | 
288 |             # Remove multiple line breaks
289 |             markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
290 | 
291 |             return markdown_content
292 | 
293 |         except RequestException as e:
294 |             return f"Error fetching the webpage: {str(e)}"
295 |         except Exception as e:
296 |             return f"An unexpected error occurred: {str(e)}"
297 | 
298 | 
299 | class SpeechToTextTool(PipelineTool):
300 |     default_checkpoint = "openai/whisper-large-v3-turbo"
301 |     description = "This is a tool that transcribes an audio into text. It returns the transcribed text."
302 |     name = "transcriber"
303 |     pre_processor_class = WhisperProcessor
304 |     model_class = WhisperForConditionalGeneration
305 | 
306 |     inputs = {
307 |         "audio": {
308 |             "type": "audio",
309 |             "description": "The audio to transcribe. Can be a local path, an url, or a tensor.",
310 |         }
311 |     }
312 |     output_type = "string"
313 | 
314 |     def encode(self, audio):
315 |         audio = AgentAudio(audio).to_raw()
316 |         return self.pre_processor(audio, return_tensors="pt")
317 | 
318 |     def forward(self, inputs):
319 |         return self.model.generate(inputs["input_features"])
320 | 
321 |     def decode(self, outputs):
322 |         return self.pre_processor.batch_decode(outputs, skip_special_tokens=True)[0]
323 | 
324 | 
325 | __all__ = [
326 |     "PythonInterpreterTool",
327 |     "FinalAnswerTool",
328 |     "UserInputTool",
329 |     "DuckDuckGoSearchTool",
330 |     "GoogleSearchTool",
331 |     "VisitWebpageTool",
332 |     "SpeechToTextTool",
333 | ]
334 | 


--------------------------------------------------------------------------------
/src/smolagents/e2b_executor.py:
--------------------------------------------------------------------------------
  1 | #!/usr/bin/env python
  2 | # coding=utf-8
  3 | 
  4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
  5 | #
  6 | # Licensed under the Apache License, Version 2.0 (the "License");
  7 | # you may not use this file except in compliance with the License.
  8 | # You may obtain a copy of the License at
  9 | #
 10 | #     http://www.apache.org/licenses/LICENSE-2.0
 11 | #
 12 | # Unless required by applicable law or agreed to in writing, software
 13 | # distributed under the License is distributed on an "AS IS" BASIS,
 14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 15 | # See the License for the specific language governing permissions and
 16 | # limitations under the License.
 17 | from dotenv import load_dotenv
 18 | import textwrap
 19 | import base64
 20 | import pickle
 21 | from io import BytesIO
 22 | from PIL import Image
 23 | 
 24 | from e2b_code_interpreter import Sandbox
 25 | from typing import List, Tuple, Any
 26 | from .tool_validation import validate_tool_attributes
 27 | from .utils import instance_to_source, BASE_BUILTIN_MODULES, console
 28 | from .tools import Tool
 29 | 
 30 | load_dotenv()
 31 | 
 32 | 
 33 | class E2BExecutor:
 34 |     def __init__(self, additional_imports: List[str], tools: List[Tool]):
 35 |         self.custom_tools = {}
 36 |         self.sbx = Sandbox()  # "qywp2ctmu2q7jzprcf4j")
 37 |         # TODO: validate installing agents package or not
 38 |         # print("Installing agents package on remote executor...")
 39 |         # self.sbx.commands.run(
 40 |         #     "pip install git+https://github.com/huggingface/smolagents.git",
 41 |         #     timeout=300
 42 |         # )
 43 |         # print("Installation of agents package finished.")
 44 |         additional_imports = additional_imports + ["pickle5"]
 45 |         if len(additional_imports) > 0:
 46 |             execution = self.sbx.commands.run(
 47 |                 "pip install " + " ".join(additional_imports)
 48 |             )
 49 |             if execution.error:
 50 |                 raise Exception(f"Error installing dependencies: {execution.error}")
 51 |             else:
 52 |                 console.print(f"Installation of {additional_imports} succeeded!")
 53 | 
 54 |         tool_codes = []
 55 |         for tool in tools:
 56 |             validate_tool_attributes(tool.__class__, check_imports=False)
 57 |             tool_code = instance_to_source(tool, base_cls=Tool)
 58 |             tool_code = tool_code.replace("from smolagents.tools import Tool", "")
 59 |             tool_code += f"\n{tool.name} = {tool.__class__.__name__}()\n"
 60 |             tool_codes.append(tool_code)
 61 | 
 62 |         tool_definition_code = "\n".join(
 63 |             [f"import {module}" for module in BASE_BUILTIN_MODULES]
 64 |         )
 65 |         tool_definition_code += textwrap.dedent("""
 66 |         class Tool:
 67 |             def __call__(self, *args, **kwargs):
 68 |                 return self.forward(*args, **kwargs)
 69 | 
 70 |             def forward(self, *args, **kwargs):
 71 |                 pass # to be implemented in child class
 72 |         """)
 73 |         tool_definition_code += "\n\n".join(tool_codes)
 74 | 
 75 |         tool_definition_execution = self.run_code_raise_errors(tool_definition_code)
 76 |         console.print(tool_definition_execution.logs)
 77 | 
 78 |     def run_code_raise_errors(self, code: str):
 79 |         execution = self.sbx.run_code(
 80 |             code,
 81 |         )
 82 |         if execution.error:
 83 |             execution_logs = "\n".join([str(log) for log in execution.logs.stdout])
 84 |             logs = execution_logs
 85 |             logs += "Executing code yielded an error:"
 86 |             logs += execution.error.name
 87 |             logs += execution.error.value
 88 |             logs += execution.error.traceback
 89 |             raise ValueError(logs)
 90 |         return execution
 91 | 
 92 |     def __call__(self, code_action: str, additional_args: dict) -> Tuple[Any, Any]:
 93 |         if len(additional_args) > 0:
 94 |             # Pickle additional_args to server
 95 |             import tempfile
 96 | 
 97 |             with tempfile.NamedTemporaryFile() as f:
 98 |                 pickle.dump(additional_args, f)
 99 |                 f.flush()
100 |                 with open(f.name, "rb") as file:
101 |                     self.sbx.files.write("/home/state.pkl", file)
102 |             remote_unloading_code = """import pickle
103 | import os
104 | print("File path", os.path.getsize('/home/state.pkl'))
105 | with open('/home/state.pkl', 'rb') as f:
106 |     pickle_dict = pickle.load(f)
107 | locals().update({key: value for key, value in pickle_dict.items()})
108 | """
109 |             execution = self.run_code_raise_errors(remote_unloading_code)
110 |             execution_logs = "\n".join([str(log) for log in execution.logs.stdout])
111 |             console.print(execution_logs)
112 | 
113 |         execution = self.run_code_raise_errors(code_action)
114 |         execution_logs = "\n".join([str(log) for log in execution.logs.stdout])
115 |         if not execution.results:
116 |             return None, execution_logs
117 |         else:
118 |             for result in execution.results:
119 |                 if result.is_main_result:
120 |                     for attribute_name in ["jpeg", "png"]:
121 |                         if getattr(result, attribute_name) is not None:
122 |                             image_output = getattr(result, attribute_name)
123 |                             decoded_bytes = base64.b64decode(
124 |                                 image_output.encode("utf-8")
125 |                             )
126 |                             return Image.open(BytesIO(decoded_bytes)), execution_logs
127 |                     for attribute_name in [
128 |                         "chart",
129 |                         "data",
130 |                         "html",
131 |                         "javascript",
132 |                         "json",
133 |                         "latex",
134 |                         "markdown",
135 |                         "pdf",
136 |                         "svg",
137 |                         "text",
138 |                     ]:
139 |                         if getattr(result, attribute_name) is not None:
140 |                             return getattr(result, attribute_name), execution_logs
141 |             raise ValueError("No main result returned by executor!")
142 | 
143 | 
144 | __all__ = ["E2BExecutor"]
145 | 


--------------------------------------------------------------------------------
/src/smolagents/gradio_ui.py:
--------------------------------------------------------------------------------
  1 | #!/usr/bin/env python
  2 | # coding=utf-8
  3 | 
  4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
  5 | #
  6 | # Licensed under the Apache License, Version 2.0 (the "License");
  7 | # you may not use this file except in compliance with the License.
  8 | # You may obtain a copy of the License at
  9 | #
 10 | #     http://www.apache.org/licenses/LICENSE-2.0
 11 | #
 12 | # Unless required by applicable law or agreed to in writing, software
 13 | # distributed under the License is distributed on an "AS IS" BASIS,
 14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 15 | # See the License for the specific language governing permissions and
 16 | # limitations under the License.
 17 | from .types import AgentAudio, AgentImage, AgentText, handle_agent_output_types
 18 | from .agents import MultiStepAgent, AgentStep, ActionStep
 19 | import gradio as gr
 20 | 
 21 | 
 22 | def pull_messages_from_step(step_log: AgentStep, test_mode: bool = True):
 23 |     """Extract ChatMessage objects from agent steps"""
 24 |     if isinstance(step_log, ActionStep):
 25 |         yield gr.ChatMessage(role="assistant", content=step_log.llm_output)
 26 |         if step_log.tool_call is not None:
 27 |             used_code = step_log.tool_call.name == "code interpreter"
 28 |             content = step_log.tool_call.arguments
 29 |             if used_code:
 30 |                 content = f"```py\n{content}\n```"
 31 |             yield gr.ChatMessage(
 32 |                 role="assistant",
 33 |                 metadata={"title": f"🛠️ Used tool {step_log.tool_call.name}"},
 34 |                 content=str(content),
 35 |             )
 36 |         if step_log.observations is not None:
 37 |             yield gr.ChatMessage(
 38 |                 role="assistant", content=f"```\n{step_log.observations}\n```"
 39 |             )
 40 |         if step_log.error is not None:
 41 |             yield gr.ChatMessage(
 42 |                 role="assistant",
 43 |                 content=str(step_log.error),
 44 |                 metadata={"title": "💥 Error"},
 45 |             )
 46 | 
 47 | 
 48 | def stream_to_gradio(
 49 |     agent,
 50 |     task: str,
 51 |     test_mode: bool = False,
 52 |     reset_agent_memory: bool = False,
 53 |     **kwargs,
 54 | ):
 55 |     """Runs an agent with the given task and streams the messages from the agent as gradio ChatMessages."""
 56 | 
 57 |     for step_log in agent.run(task, stream=True, reset=reset_agent_memory, **kwargs):
 58 |         for message in pull_messages_from_step(step_log, test_mode=test_mode):
 59 |             yield message
 60 | 
 61 |     final_answer = step_log  # Last log is the run's final_answer
 62 |     final_answer = handle_agent_output_types(final_answer)
 63 | 
 64 |     if isinstance(final_answer, AgentText):
 65 |         yield gr.ChatMessage(
 66 |             role="assistant",
 67 |             content=f"**Final answer:**\n```\n{final_answer.to_string()}\n```",
 68 |         )
 69 |     elif isinstance(final_answer, AgentImage):
 70 |         yield gr.ChatMessage(
 71 |             role="assistant",
 72 |             content={"path": final_answer.to_string(), "mime_type": "image/png"},
 73 |         )
 74 |     elif isinstance(final_answer, AgentAudio):
 75 |         yield gr.ChatMessage(
 76 |             role="assistant",
 77 |             content={"path": final_answer.to_string(), "mime_type": "audio/wav"},
 78 |         )
 79 |     else:
 80 |         yield gr.ChatMessage(role="assistant", content=str(final_answer))
 81 | 
 82 | 
 83 | class GradioUI:
 84 |     """A one-line interface to launch your agent in Gradio"""
 85 | 
 86 |     def __init__(self, agent: MultiStepAgent):
 87 |         self.agent = agent
 88 | 
 89 |     def interact_with_agent(self, prompt, messages):
 90 |         messages.append(gr.ChatMessage(role="user", content=prompt))
 91 |         yield messages
 92 |         for msg in stream_to_gradio(self.agent, task=prompt, reset_agent_memory=False):
 93 |             messages.append(msg)
 94 |             yield messages
 95 |         yield messages
 96 | 
 97 |     def launch(self):
 98 |         with gr.Blocks() as demo:
 99 |             stored_message = gr.State([])
100 |             chatbot = gr.Chatbot(
101 |                 label="Agent",
102 |                 type="messages",
103 |                 avatar_images=(
104 |                     None,
105 |                     "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png",
106 |                 ),
107 |             )
108 |             text_input = gr.Textbox(lines=1, label="Chat Message")
109 |             text_input.submit(
110 |                 lambda s: (s, ""), [text_input], [stored_message, text_input]
111 |             ).then(self.interact_with_agent, [stored_message, chatbot], [chatbot])
112 | 
113 |         demo.launch()
114 | 
115 | 
116 | __all__ = ["stream_to_gradio", "GradioUI"]
117 | 


--------------------------------------------------------------------------------
/src/smolagents/models.py:
--------------------------------------------------------------------------------
  1 | #!/usr/bin/env python
  2 | # coding=utf-8
  3 | 
  4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
  5 | #
  6 | # Licensed under the Apache License, Version 2.0 (the "License");
  7 | # you may not use this file except in compliance with the License.
  8 | # You may obtain a copy of the License at
  9 | #
 10 | #     http://www.apache.org/licenses/LICENSE-2.0
 11 | #
 12 | # Unless required by applicable law or agreed to in writing, software
 13 | # distributed under the License is distributed on an "AS IS" BASIS,
 14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 15 | # See the License for the specific language governing permissions and
 16 | # limitations under the License.
 17 | from copy import deepcopy
 18 | from enum import Enum
 19 | import json
 20 | from typing import Dict, List, Optional
 21 | from transformers import (
 22 |     AutoTokenizer,
 23 |     AutoModelForCausalLM,
 24 |     StoppingCriteria,
 25 |     StoppingCriteriaList,
 26 | )
 27 | 
 28 | import litellm
 29 | import logging
 30 | import os
 31 | import random
 32 | 
 33 | from huggingface_hub import InferenceClient
 34 | 
 35 | from .tools import Tool
 36 | from .utils import parse_json_tool_call
 37 | 
 38 | logger = logging.getLogger(__name__)
 39 | 
 40 | DEFAULT_JSONAGENT_REGEX_GRAMMAR = {
 41 |     "type": "regex",
 42 |     "value": 'Thought: .+?\\nAction:\\n\\{\\n\\s{4}"action":\\s"[^"\\n]+",\\n\\s{4}"action_input":\\s"[^"\\n]+"\\n\\}\\n<end_action>',
 43 | }
 44 | 
 45 | DEFAULT_CODEAGENT_REGEX_GRAMMAR = {
 46 |     "type": "regex",
 47 |     "value": "Thought: .+?\\nCode:\\n```(?:py|python)?\\n(?:.|\\s)+?\\n```<end_action>",
 48 | }
 49 | 
 50 | 
 51 | class MessageRole(str, Enum):
 52 |     USER = "user"
 53 |     ASSISTANT = "assistant"
 54 |     SYSTEM = "system"
 55 |     TOOL_CALL = "tool-call"
 56 |     TOOL_RESPONSE = "tool-response"
 57 | 
 58 |     @classmethod
 59 |     def roles(cls):
 60 |         return [r.value for r in cls]
 61 | 
 62 | 
 63 | tool_role_conversions = {
 64 |     MessageRole.TOOL_CALL: MessageRole.ASSISTANT,
 65 |     MessageRole.TOOL_RESPONSE: MessageRole.USER,
 66 | }
 67 | 
 68 | 
 69 | def get_json_schema(tool: Tool) -> Dict:
 70 |     properties = deepcopy(tool.inputs)
 71 |     required = []
 72 |     for key, value in properties.items():
 73 |         if value["type"] == "any":
 74 |             value["type"] = "string"
 75 |         if not ("nullable" in value and value["nullable"]):
 76 |             required.append(key)
 77 |     return {
 78 |         "type": "function",
 79 |         "function": {
 80 |             "name": tool.name,
 81 |             "description": tool.description,
 82 |             "parameters": {
 83 |                 "type": "object",
 84 |                 "properties": properties,
 85 |                 "required": required,
 86 |             },
 87 |         },
 88 |     }
 89 | 
 90 | 
 91 | def remove_stop_sequences(content: str, stop_sequences: List[str]) -> str:
 92 |     for stop_seq in stop_sequences:
 93 |         if content[-len(stop_seq) :] == stop_seq:
 94 |             content = content[: -len(stop_seq)]
 95 |     return content
 96 | 
 97 | 
 98 | def get_clean_message_list(
 99 |     message_list: List[Dict[str, str]],
100 |     role_conversions: Dict[MessageRole, MessageRole] = {},
101 | ) -> List[Dict[str, str]]:
102 |     """
103 |     Subsequent messages with the same role will be concatenated to a single message.
104 | 
105 |     Args:
106 |         message_list (`List[Dict[str, str]]`): List of chat messages.
107 |     """
108 |     final_message_list = []
109 |     message_list = deepcopy(message_list)  # Avoid modifying the original list
110 |     for message in message_list:
111 |         # if not set(message.keys()) == {"role", "content"}:
112 |         #     raise ValueError("Message should contain only 'role' and 'content' keys!")
113 | 
114 |         role = message["role"]
115 |         if role not in MessageRole.roles():
116 |             raise ValueError(
117 |                 f"Incorrect role {role}, only {MessageRole.roles()} are supported for now."
118 |             )
119 | 
120 |         if role in role_conversions:
121 |             message["role"] = role_conversions[role]
122 | 
123 |         if (
124 |             len(final_message_list) > 0
125 |             and message["role"] == final_message_list[-1]["role"]
126 |         ):
127 |             final_message_list[-1]["content"] += "\n=======\n" + message["content"]
128 |         else:
129 |             final_message_list.append(message)
130 |     return final_message_list
131 | 
132 | 
133 | class Model:
134 |     def __init__(self):
135 |         self.last_input_token_count = None
136 |         self.last_output_token_count = None
137 | 
138 |     def get_token_counts(self):
139 |         return {
140 |             "input_token_count": self.last_input_token_count,
141 |             "output_token_count": self.last_output_token_count,
142 |         }
143 | 
144 |     def generate(
145 |         self,
146 |         messages: List[Dict[str, str]],
147 |         stop_sequences: Optional[List[str]] = None,
148 |         grammar: Optional[str] = None,
149 |         max_tokens: int = 1500,
150 |     ):
151 |         raise NotImplementedError
152 | 
153 |     def __call__(
154 |         self,
155 |         messages: List[Dict[str, str]],
156 |         stop_sequences: Optional[List[str]] = None,
157 |         grammar: Optional[str] = None,
158 |         max_tokens: int = 1500,
159 |     ) -> str:
160 |         """Process the input messages and return the model's response.
161 | 
162 |         Parameters:
163 |             messages (`List[Dict[str, str]]`):
164 |                 A list of message dictionaries to be processed. Each dictionary should have the structure `{"role": "user/system", "content": "message content"}`.
165 |             stop_sequences (`List[str]`, *optional*):
166 |                 A list of strings that will stop the generation if encountered in the model's output.
167 |             grammar (`str`, *optional*):
168 |                 The grammar or formatting structure to use in the model's response.
169 |             max_tokens (`int`, *optional*):
170 |                 The maximum count of tokens to generate.
171 |         Returns:
172 |             `str`: The text content of the model's response.
173 |         """
174 |         if not isinstance(messages, List):
175 |             raise ValueError(
176 |                 "Messages should be a list of dictionaries with 'role' and 'content' keys."
177 |             )
178 |         if stop_sequences is None:
179 |             stop_sequences = []
180 |         response = self.generate(messages, stop_sequences, grammar, max_tokens)
181 | 
182 |         return remove_stop_sequences(response, stop_sequences)
183 | 
184 | 
185 | class HfApiModel(Model):
186 |     """A class to interact with Hugging Face's Inference API for language model interaction.
187 | 
188 |     This engine allows you to communicate with Hugging Face's models using the Inference API. It can be used in both serverless mode or with a dedicated endpoint, supporting features like stop sequences and grammar customization.
189 | 
190 |     Parameters:
191 |         model (`str`, *optional*, defaults to `"Qwen/Qwen2.5-Coder-32B-Instruct"`):
192 |             The Hugging Face model ID to be used for inference. This can be a path or model identifier from the Hugging Face model hub.
193 |         token (`str`, *optional*):
194 |             Token used by the Hugging Face API for authentication. This token need to be authorized 'Make calls to the serverless Inference API'.
195 |             If the model is gated (like Llama-3 models), the token also needs 'Read access to contents of all public gated repos you can access'.
196 |             If not provided, the class will try to use environment variable 'HF_TOKEN', else use the token stored in the Hugging Face CLI configuration.
197 |         max_tokens (`int`, *optional*, defaults to 1500):
198 |             The maximum number of tokens allowed in the output.
199 |         timeout (`int`, *optional*, defaults to 120):
200 |             Timeout for the API request, in seconds.
201 | 
202 |     Raises:
203 |         ValueError:
204 |             If the model name is not provided.
205 | 
206 |     Example:
207 |     ```python
208 |     >>> engine = HfApiModel(
209 |     ...     model="Qwen/Qwen2.5-Coder-32B-Instruct",
210 |     ...     token="your_hf_token_here",
211 |     ...     max_tokens=2000
212 |     ... )
213 |     >>> messages = [{"role": "user", "content": "Explain quantum mechanics in simple terms."}]
214 |     >>> response = engine(messages, stop_sequences=["END"])
215 |     >>> print(response)
216 |     "Quantum mechanics is the branch of physics that studies..."
217 |     ```
218 |     """
219 | 
220 |     def __init__(
221 |         self,
222 |         model_id: str = "Qwen/Qwen2.5-Coder-32B-Instruct",
223 |         token: Optional[str] = None,
224 |         timeout: Optional[int] = 120,
225 |     ):
226 |         super().__init__()
227 |         self.model_id = model_id
228 |         if token is None:
229 |             token = os.getenv("HF_TOKEN")
230 |         self.client = InferenceClient(self.model_id, token=token, timeout=timeout)
231 | 
232 |     def generate(
233 |         self,
234 |         messages: List[Dict[str, str]],
235 |         stop_sequences: Optional[List[str]] = None,
236 |         grammar: Optional[str] = None,
237 |         max_tokens: int = 1500,
238 |     ) -> str:
239 |         """Generates a text completion for the given message list"""
240 |         messages = get_clean_message_list(
241 |             messages, role_conversions=tool_role_conversions
242 |         )
243 | 
244 |         # Send messages to the Hugging Face Inference API
245 |         if grammar is not None:
246 |             output = self.client.chat_completion(
247 |                 messages,
248 |                 stop=stop_sequences,
249 |                 response_format=grammar,
250 |                 max_tokens=max_tokens,
251 |             )
252 |         else:
253 |             output = self.client.chat.completions.create(
254 |                 messages, stop=stop_sequences, max_tokens=max_tokens
255 |             )
256 | 
257 |         response = output.choices[0].message.content
258 |         self.last_input_token_count = output.usage.prompt_tokens
259 |         self.last_output_token_count = output.usage.completion_tokens
260 |         return response
261 | 
262 |     def get_tool_call(
263 |         self,
264 |         messages: List[Dict[str, str]],
265 |         available_tools: List[Tool],
266 |         stop_sequences,
267 |     ):
268 |         """Generates a tool call for the given message list. This method is used only by `ToolCallingAgent`."""
269 |         messages = get_clean_message_list(
270 |             messages, role_conversions=tool_role_conversions
271 |         )
272 |         response = self.client.chat.completions.create(
273 |             messages=messages,
274 |             tools=[get_json_schema(tool) for tool in available_tools],
275 |             tool_choice="auto",
276 |             stop=stop_sequences,
277 |         )
278 |         tool_call = response.choices[0].message.tool_calls[0]
279 |         self.last_input_token_count = response.usage.prompt_tokens
280 |         self.last_output_token_count = response.usage.completion_tokens
281 |         return tool_call.function.name, tool_call.function.arguments, tool_call.id
282 | 
283 | 
284 | class TransformersModel(Model):
285 |     """This engine initializes a model and tokenizer from the given `model_id`."""
286 | 
287 |     def __init__(self, model_id: Optional[str] = None):
288 |         super().__init__()
289 |         default_model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
290 |         if model_id is None:
291 |             model_id = default_model_id
292 |             logger.warning(
293 |                 f"`model_id`not provided, using this default tokenizer for token counts: '{model_id}'"
294 |             )
295 |         self.model_id = model_id
296 |         try:
297 |             self.tokenizer = AutoTokenizer.from_pretrained(model_id)
298 |             self.model = AutoModelForCausalLM.from_pretrained(model_id)
299 |         except Exception as e:
300 |             logger.warning(
301 |                 f"Failed to load tokenizer and model for {model_id=}: {e}. Loading default tokenizer and model instead from {model_id=}."
302 |             )
303 |             self.tokenizer = AutoTokenizer.from_pretrained(default_model_id)
304 |             self.model = AutoModelForCausalLM.from_pretrained(default_model_id)
305 | 
306 |     def make_stopping_criteria(self, stop_sequences: List[str]) -> StoppingCriteriaList:
307 |         class StopOnStrings(StoppingCriteria):
308 |             def __init__(self, stop_strings: List[str], tokenizer):
309 |                 self.stop_strings = stop_strings
310 |                 self.tokenizer = tokenizer
311 |                 self.stream = ""
312 | 
313 |             def reset(self):
314 |                 self.stream = ""
315 | 
316 |             def __call__(self, input_ids, scores, **kwargs):
317 |                 generated = self.tokenizer.decode(
318 |                     input_ids[0][-1], skip_special_tokens=True
319 |                 )
320 |                 self.stream += generated
321 |                 if any(
322 |                     [
323 |                         self.stream.endswith(stop_string)
324 |                         for stop_string in self.stop_strings
325 |                     ]
326 |                 ):
327 |                     return True
328 |                 return False
329 | 
330 |         return StoppingCriteriaList([StopOnStrings(stop_sequences, self.tokenizer)])
331 | 
332 |     def generate(
333 |         self,
334 |         messages: List[Dict[str, str]],
335 |         stop_sequences: Optional[List[str]] = None,
336 |         grammar: Optional[str] = None,
337 |         max_tokens: int = 1500,
338 |     ) -> str:
339 |         messages = get_clean_message_list(
340 |             messages, role_conversions=tool_role_conversions
341 |         )
342 | 
343 |         # Get LLM output
344 |         prompt = self.tokenizer.apply_chat_template(
345 |             messages,
346 |             return_tensors="pt",
347 |             return_dict=True,
348 |         )
349 |         prompt = prompt.to(self.model.device)
350 |         count_prompt_tokens = prompt["input_ids"].shape[1]
351 | 
352 |         out = self.model.generate(
353 |             **prompt,
354 |             max_new_tokens=max_tokens,
355 |             stopping_criteria=(
356 |                 self.make_stopping_criteria(stop_sequences) if stop_sequences else None
357 |             ),
358 |         )
359 |         generated_tokens = out[0, count_prompt_tokens:]
360 |         response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
361 | 
362 |         self.last_input_token_count = count_prompt_tokens
363 |         self.last_output_token_count = len(generated_tokens)
364 | 
365 |         if stop_sequences is not None:
366 |             response = remove_stop_sequences(response, stop_sequences)
367 |         return response
368 | 
369 |     def get_tool_call(
370 |         self,
371 |         messages: List[Dict[str, str]],
372 |         available_tools: List[Tool],
373 |         stop_sequences: Optional[List[str]] = None,
374 |         max_tokens: int = 500,
375 |     ) -> str:
376 |         messages = get_clean_message_list(
377 |             messages, role_conversions=tool_role_conversions
378 |         )
379 | 
380 |         prompt = self.tokenizer.apply_chat_template(
381 |             messages,
382 |             tools=[get_json_schema(tool) for tool in available_tools],
383 |             return_tensors="pt",
384 |             return_dict=True,
385 |             add_generation_prompt=True,
386 |         )
387 |         prompt = prompt.to(self.model.device)
388 |         count_prompt_tokens = prompt["input_ids"].shape[1]
389 | 
390 |         out = self.model.generate(
391 |             **prompt,
392 |             max_new_tokens=max_tokens,
393 |             stopping_criteria=(
394 |                 self.make_stopping_criteria(stop_sequences) if stop_sequences else None
395 |             ),
396 |         )
397 |         generated_tokens = out[0, count_prompt_tokens:]
398 |         response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
399 | 
400 |         self.last_input_token_count = count_prompt_tokens
401 |         self.last_output_token_count = len(generated_tokens)
402 | 
403 |         if stop_sequences is not None:
404 |             response = remove_stop_sequences(response, stop_sequences)
405 | 
406 |         tool_name, tool_input = parse_json_tool_call(response)
407 |         call_id = "".join(random.choices("0123456789", k=5))
408 | 
409 |         return tool_name, tool_input, call_id
410 | 
411 | 
412 | class LiteLLMModel(Model):
413 |     def __init__(
414 |         self,
415 |         model_id="anthropic/claude-3-5-sonnet-20240620",
416 |         api_base=None,
417 |         api_key=None,
418 |     ):
419 |         super().__init__()
420 |         self.model_id = model_id
421 |         # IMPORTANT - Set this to TRUE to add the function to the prompt for Non OpenAI LLMs
422 |         litellm.add_function_to_prompt = True
423 |         self.api_base = api_base
424 |         self.api_key = api_key
425 | 
426 |     def __call__(
427 |         self,
428 |         messages: List[Dict[str, str]],
429 |         stop_sequences: Optional[List[str]] = None,
430 |         grammar: Optional[str] = None,
431 |         max_tokens: int = 1500,
432 |     ) -> str:
433 |         messages = get_clean_message_list(
434 |             messages, role_conversions=tool_role_conversions
435 |         )
436 | 
437 |         response = litellm.completion(
438 |             model=self.model_id,
439 |             messages=messages,
440 |             stop=stop_sequences,
441 |             max_tokens=max_tokens,
442 |             api_base=self.api_base,
443 |             api_key=self.api_key,
444 |         )
445 |         self.last_input_token_count = response.usage.prompt_tokens
446 |         self.last_output_token_count = response.usage.completion_tokens
447 |         return response.choices[0].message.content
448 | 
449 |     def get_tool_call(
450 |         self,
451 |         messages: List[Dict[str, str]],
452 |         available_tools: List[Tool],
453 |         stop_sequences: Optional[List[str]] = None,
454 |         max_tokens: int = 1500,
455 |     ):
456 |         messages = get_clean_message_list(
457 |             messages, role_conversions=tool_role_conversions
458 |         )
459 |         response = litellm.completion(
460 |             model=self.model_id,
461 |             messages=messages,
462 |             tools=[get_json_schema(tool) for tool in available_tools],
463 |             tool_choice="required",
464 |             stop=stop_sequences,
465 |             max_tokens=max_tokens,
466 |             api_base=self.api_base,
467 |             api_key=self.api_key,
468 |         )
469 |         tool_calls = response.choices[0].message.tool_calls[0]
470 |         self.last_input_token_count = response.usage.prompt_tokens
471 |         self.last_output_token_count = response.usage.completion_tokens
472 |         arguments = json.loads(tool_calls.function.arguments)
473 |         return tool_calls.function.name, arguments, tool_calls.id
474 | 
475 | 
476 | __all__ = [
477 |     "MessageRole",
478 |     "tool_role_conversions",
479 |     "get_clean_message_list",
480 |     "Model",
481 |     "TransformersModel",
482 |     "HfApiModel",
483 |     "LiteLLMModel",
484 | ]
485 | 


--------------------------------------------------------------------------------
/src/smolagents/monitoring.py:
--------------------------------------------------------------------------------
 1 | #!/usr/bin/env python
 2 | # coding=utf-8
 3 | 
 4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
 5 | #
 6 | # Licensed under the Apache License, Version 2.0 (the "License");
 7 | # you may not use this file except in compliance with the License.
 8 | # You may obtain a copy of the License at
 9 | #
10 | #     http://www.apache.org/licenses/LICENSE-2.0
11 | #
12 | # Unless required by applicable law or agreed to in writing, software
13 | # distributed under the License is distributed on an "AS IS" BASIS,
14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
15 | # See the License for the specific language governing permissions and
16 | # limitations under the License.
17 | from .utils import console
18 | from rich.text import Text
19 | 
20 | 
21 | class Monitor:
22 |     def __init__(self, tracked_model):
23 |         self.step_durations = []
24 |         self.tracked_model = tracked_model
25 |         if (
26 |             getattr(self.tracked_model, "last_input_token_count", "Not found")
27 |             != "Not found"
28 |         ):
29 |             self.total_input_token_count = 0
30 |             self.total_output_token_count = 0
31 | 
32 |     def get_total_token_counts(self):
33 |         return {
34 |             "input": self.total_input_token_count,
35 |             "output": self.total_output_token_count,
36 |         }
37 | 
38 |     def reset(self):
39 |         self.step_durations = []
40 |         self.total_input_token_count = 0
41 |         self.total_output_token_count = 0
42 | 
43 |     def update_metrics(self, step_log):
44 |         step_duration = step_log.duration
45 |         self.step_durations.append(step_duration)
46 |         console_outputs = (
47 |             f"[Step {len(self.step_durations)-1}: Duration {step_duration:.2f} seconds"
48 |         )
49 | 
50 |         if getattr(self.tracked_model, "last_input_token_count", None) is not None:
51 |             self.total_input_token_count += self.tracked_model.last_input_token_count
52 |             self.total_output_token_count += self.tracked_model.last_output_token_count
53 |             console_outputs += f"| Input tokens: {self.total_input_token_count:,} | Output tokens: {self.total_output_token_count:,}"
54 |         console_outputs += "]"
55 |         console.print(Text(console_outputs, style="dim"))
56 | 
57 | 
58 | __all__ = ["Monitor"]
59 | 


--------------------------------------------------------------------------------
/src/smolagents/tool_validation.py:
--------------------------------------------------------------------------------
  1 | import ast
  2 | import inspect
  3 | import builtins
  4 | from typing import Set
  5 | import textwrap
  6 | from .utils import BASE_BUILTIN_MODULES
  7 | 
  8 | _BUILTIN_NAMES = set(vars(builtins))
  9 | 
 10 | 
 11 | class MethodChecker(ast.NodeVisitor):
 12 |     """
 13 |     Checks that a method
 14 |     - only uses defined names
 15 |     - contains no local imports (e.g. numpy is ok but local_script is not)
 16 |     """
 17 | 
 18 |     def __init__(self, class_attributes: Set[str], check_imports: bool = True):
 19 |         self.undefined_names = set()
 20 |         self.imports = {}
 21 |         self.from_imports = {}
 22 |         self.assigned_names = set()
 23 |         self.arg_names = set()
 24 |         self.class_attributes = class_attributes
 25 |         self.errors = []
 26 |         self.check_imports = check_imports
 27 | 
 28 |     def visit_arguments(self, node):
 29 |         """Collect function arguments"""
 30 |         self.arg_names = {arg.arg for arg in node.args}
 31 |         if node.kwarg:
 32 |             self.arg_names.add(node.kwarg.arg)
 33 |         if node.vararg:
 34 |             self.arg_names.add(node.vararg.arg)
 35 | 
 36 |     def visit_Import(self, node):
 37 |         for name in node.names:
 38 |             actual_name = name.asname or name.name
 39 |             self.imports[actual_name] = name.name
 40 | 
 41 |     def visit_ImportFrom(self, node):
 42 |         module = node.module or ""
 43 |         for name in node.names:
 44 |             actual_name = name.asname or name.name
 45 |             self.from_imports[actual_name] = (module, name.name)
 46 | 
 47 |     def visit_Assign(self, node):
 48 |         for target in node.targets:
 49 |             if isinstance(target, ast.Name):
 50 |                 self.assigned_names.add(target.id)
 51 |         self.visit(node.value)
 52 | 
 53 |     def visit_With(self, node):
 54 |         """Track aliases in 'with' statements (the 'y' in 'with X as y')"""
 55 |         for item in node.items:
 56 |             if item.optional_vars:  # This is the 'y' in 'with X as y'
 57 |                 if isinstance(item.optional_vars, ast.Name):
 58 |                     self.assigned_names.add(item.optional_vars.id)
 59 |         self.generic_visit(node)
 60 | 
 61 |     def visit_ExceptHandler(self, node):
 62 |         """Track exception aliases (the 'e' in 'except Exception as e')"""
 63 |         if node.name:  # This is the 'e' in 'except Exception as e'
 64 |             self.assigned_names.add(node.name)
 65 |         self.generic_visit(node)
 66 | 
 67 |     def visit_AnnAssign(self, node):
 68 |         """Track annotated assignments."""
 69 |         if isinstance(node.target, ast.Name):
 70 |             self.assigned_names.add(node.target.id)
 71 |         if node.value:
 72 |             self.visit(node.value)
 73 | 
 74 |     def visit_For(self, node):
 75 |         target = node.target
 76 |         if isinstance(target, ast.Name):
 77 |             self.assigned_names.add(target.id)
 78 |         elif isinstance(target, ast.Tuple):
 79 |             for elt in target.elts:
 80 |                 if isinstance(elt, ast.Name):
 81 |                     self.assigned_names.add(elt.id)
 82 |         self.generic_visit(node)
 83 | 
 84 |     def visit_Attribute(self, node):
 85 |         if not (isinstance(node.value, ast.Name) and node.value.id == "self"):
 86 |             self.generic_visit(node)
 87 | 
 88 |     def visit_Name(self, node):
 89 |         if isinstance(node.ctx, ast.Load):
 90 |             if not (
 91 |                 node.id in _BUILTIN_NAMES
 92 |                 or node.id in BASE_BUILTIN_MODULES
 93 |                 or node.id in self.arg_names
 94 |                 or node.id == "self"
 95 |                 or node.id in self.class_attributes
 96 |                 or node.id in self.imports
 97 |                 or node.id in self.from_imports
 98 |                 or node.id in self.assigned_names
 99 |             ):
100 |                 self.errors.append(f"Name '{node.id}' is undefined.")
101 | 
102 |     def visit_Call(self, node):
103 |         if isinstance(node.func, ast.Name):
104 |             if not (
105 |                 node.func.id in _BUILTIN_NAMES
106 |                 or node.func.id in BASE_BUILTIN_MODULES
107 |                 or node.func.id in self.arg_names
108 |                 or node.func.id == "self"
109 |                 or node.func.id in self.class_attributes
110 |                 or node.func.id in self.imports
111 |                 or node.func.id in self.from_imports
112 |                 or node.func.id in self.assigned_names
113 |             ):
114 |                 self.errors.append(f"Name '{node.func.id}' is undefined.")
115 |         self.generic_visit(node)
116 | 
117 | 
118 | def validate_tool_attributes(cls, check_imports: bool = True) -> None:
119 |     """
120 |     Validates that a Tool class follows the proper patterns:
121 |     0. __init__ takes no argument (args chosen at init are not traceable so we cannot rebuild the source code for them, make them class attributes!).
122 |     1. About the class:
123 |         - Class attributes should only be strings or dicts
124 |         - Class attributes cannot be complex attributes
125 |     2. About all class methods:
126 |         - Imports must be from packages, not local files
127 |         - All methods must be self-contained
128 | 
129 |     Raises all errors encountered, if no error returns None.
130 |     """
131 |     errors = []
132 | 
133 |     source = textwrap.dedent(inspect.getsource(cls))
134 | 
135 |     tree = ast.parse(source)
136 | 
137 |     if not isinstance(tree.body[0], ast.ClassDef):
138 |         raise ValueError("Source code must define a class")
139 | 
140 |     # Check that __init__ method takes no arguments
141 |     if not cls.__init__.__qualname__ == "Tool.__init__":
142 |         sig = inspect.signature(cls.__init__)
143 |         non_self_params = list(
144 |             [arg_name for arg_name in sig.parameters.keys() if arg_name != "self"]
145 |         )
146 |         if len(non_self_params) > 0:
147 |             errors.append(
148 |                 f"This tool has additional args specified in __init__(self): {non_self_params}. Make sure it does not, all values should be hardcoded!"
149 |             )
150 | 
151 |     class_node = tree.body[0]
152 | 
153 |     class ClassLevelChecker(ast.NodeVisitor):
154 |         def __init__(self):
155 |             self.imported_names = set()
156 |             self.complex_attributes = set()
157 |             self.class_attributes = set()
158 |             self.in_method = False
159 | 
160 |         def visit_FunctionDef(self, node):
161 |             old_context = self.in_method
162 |             self.in_method = True
163 |             self.generic_visit(node)
164 |             self.in_method = old_context
165 | 
166 |         def visit_Assign(self, node):
167 |             if self.in_method:
168 |                 return
169 |             # Track class attributes
170 |             for target in node.targets:
171 |                 if isinstance(target, ast.Name):
172 |                     self.class_attributes.add(target.id)
173 | 
174 |             # Check if the assignment is more complex than simple literals
175 |             if not all(
176 |                 isinstance(
177 |                     val, (ast.Str, ast.Num, ast.Constant, ast.Dict, ast.List, ast.Set)
178 |                 )
179 |                 for val in ast.walk(node.value)
180 |             ):
181 |                 for target in node.targets:
182 |                     if isinstance(target, ast.Name):
183 |                         self.complex_attributes.add(target.id)
184 | 
185 |     class_level_checker = ClassLevelChecker()
186 |     class_level_checker.visit(class_node)
187 | 
188 |     if class_level_checker.complex_attributes:
189 |         errors.append(
190 |             f"Complex attributes should be defined in __init__, not as class attributes: "
191 |             f"{', '.join(class_level_checker.complex_attributes)}"
192 |         )
193 | 
194 |     # Run checks on all methods
195 |     for node in class_node.body:
196 |         if isinstance(node, ast.FunctionDef):
197 |             method_checker = MethodChecker(
198 |                 class_level_checker.class_attributes, check_imports=check_imports
199 |             )
200 |             method_checker.visit(node)
201 |             errors += [f"- {node.name}: {error}" for error in method_checker.errors]
202 | 
203 |     if errors:
204 |         raise ValueError("Tool validation failed:\n" + "\n".join(errors))
205 |     return
206 | 


--------------------------------------------------------------------------------
/src/smolagents/types.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | import os
 16 | import pathlib
 17 | import tempfile
 18 | import uuid
 19 | from io import BytesIO
 20 | import requests
 21 | import numpy as np
 22 | 
 23 | from transformers.utils import (
 24 |     is_soundfile_availble,
 25 |     is_torch_available,
 26 |     is_vision_available,
 27 | )
 28 | import logging
 29 | 
 30 | 
 31 | logger = logging.getLogger(__name__)
 32 | 
 33 | if is_vision_available():
 34 |     from PIL import Image
 35 |     from PIL.Image import Image as ImageType
 36 | else:
 37 |     ImageType = object
 38 | 
 39 | if is_torch_available():
 40 |     import torch
 41 |     from torch import Tensor
 42 | else:
 43 |     Tensor = object
 44 | 
 45 | if is_soundfile_availble():
 46 |     import soundfile as sf
 47 | 
 48 | 
 49 | class AgentType:
 50 |     """
 51 |     Abstract class to be reimplemented to define types that can be returned by agents.
 52 | 
 53 |     These objects serve three purposes:
 54 | 
 55 |     - They behave as they were the type they're meant to be, e.g., a string for text, a PIL.Image for images
 56 |     - They can be stringified: str(object) in order to return a string defining the object
 57 |     - They should be displayed correctly in ipython notebooks/colab/jupyter
 58 |     """
 59 | 
 60 |     def __init__(self, value):
 61 |         self._value = value
 62 | 
 63 |     def __str__(self):
 64 |         return self.to_string()
 65 | 
 66 |     def to_raw(self):
 67 |         logger.error(
 68 |             "This is a raw AgentType of unknown type. Display in notebooks and string conversion will be unreliable"
 69 |         )
 70 |         return self._value
 71 | 
 72 |     def to_string(self) -> str:
 73 |         logger.error(
 74 |             "This is a raw AgentType of unknown type. Display in notebooks and string conversion will be unreliable"
 75 |         )
 76 |         return str(self._value)
 77 | 
 78 | 
 79 | class AgentText(AgentType, str):
 80 |     """
 81 |     Text type returned by the agent. Behaves as a string.
 82 |     """
 83 | 
 84 |     def to_raw(self):
 85 |         return self._value
 86 | 
 87 |     def to_string(self):
 88 |         return str(self._value)
 89 | 
 90 | 
 91 | class AgentImage(AgentType, ImageType):
 92 |     """
 93 |     Image type returned by the agent. Behaves as a PIL.Image.
 94 |     """
 95 | 
 96 |     def __init__(self, value):
 97 |         AgentType.__init__(self, value)
 98 |         ImageType.__init__(self)
 99 | 
100 |         if not is_vision_available():
101 |             raise ImportError("PIL must be installed in order to handle images.")
102 | 
103 |         self._path = None
104 |         self._raw = None
105 |         self._tensor = None
106 | 
107 |         if isinstance(value, AgentImage):
108 |             self._raw, self._path, self._tensor = value._raw, value._path, value._tensor
109 |         elif isinstance(value, ImageType):
110 |             self._raw = value
111 |         elif isinstance(value, bytes):
112 |             self._raw = Image.open(BytesIO(value))
113 |         elif isinstance(value, (str, pathlib.Path)):
114 |             self._path = value
115 |         elif isinstance(value, torch.Tensor):
116 |             self._tensor = value
117 |         elif isinstance(value, np.ndarray):
118 |             self._tensor = torch.from_numpy(value)
119 |         else:
120 |             raise TypeError(
121 |                 f"Unsupported type for {self.__class__.__name__}: {type(value)}"
122 |             )
123 | 
124 |     def _ipython_display_(self, include=None, exclude=None):
125 |         """
126 |         Displays correctly this type in an ipython notebook (ipython, colab, jupyter, ...)
127 |         """
128 |         from IPython.display import Image, display
129 | 
130 |         display(Image(self.to_string()))
131 | 
132 |     def to_raw(self):
133 |         """
134 |         Returns the "raw" version of that object. In the case of an AgentImage, it is a PIL.Image.
135 |         """
136 |         if self._raw is not None:
137 |             return self._raw
138 | 
139 |         if self._path is not None:
140 |             self._raw = Image.open(self._path)
141 |             return self._raw
142 | 
143 |         if self._tensor is not None:
144 |             array = self._tensor.cpu().detach().numpy()
145 |             return Image.fromarray((255 - array * 255).astype(np.uint8))
146 | 
147 |     def to_string(self):
148 |         """
149 |         Returns the stringified version of that object. In the case of an AgentImage, it is a path to the serialized
150 |         version of the image.
151 |         """
152 |         if self._path is not None:
153 |             return self._path
154 | 
155 |         if self._raw is not None:
156 |             directory = tempfile.mkdtemp()
157 |             self._path = os.path.join(directory, str(uuid.uuid4()) + ".png")
158 |             self._raw.save(self._path, format="png")
159 |             return self._path
160 | 
161 |         if self._tensor is not None:
162 |             array = self._tensor.cpu().detach().numpy()
163 | 
164 |             # There is likely simpler than load into image into save
165 |             img = Image.fromarray((255 - array * 255).astype(np.uint8))
166 | 
167 |             directory = tempfile.mkdtemp()
168 |             self._path = os.path.join(directory, str(uuid.uuid4()) + ".png")
169 |             img.save(self._path, format="png")
170 | 
171 |             return self._path
172 | 
173 |     def save(self, output_bytes, format: str = None, **params):
174 |         """
175 |         Saves the image to a file.
176 |         Args:
177 |             output_bytes (bytes): The output bytes to save the image to.
178 |             format (str): The format to use for the output image. The format is the same as in PIL.Image.save.
179 |             **params: Additional parameters to pass to PIL.Image.save.
180 |         """
181 |         img = self.to_raw()
182 |         img.save(output_bytes, format=format, **params)
183 | 
184 | 
185 | class AgentAudio(AgentType, str):
186 |     """
187 |     Audio type returned by the agent.
188 |     """
189 | 
190 |     def __init__(self, value, samplerate=16_000):
191 |         super().__init__(value)
192 | 
193 |         if not is_soundfile_availble():
194 |             raise ImportError("soundfile must be installed in order to handle audio.")
195 | 
196 |         self._path = None
197 |         self._tensor = None
198 | 
199 |         self.samplerate = samplerate
200 |         if isinstance(value, (str, pathlib.Path)):
201 |             self._path = value
202 |         elif is_torch_available() and isinstance(value, torch.Tensor):
203 |             self._tensor = value
204 |         elif isinstance(value, tuple):
205 |             self.samplerate = value[0]
206 |             if isinstance(value[1], np.ndarray):
207 |                 self._tensor = torch.from_numpy(value[1])
208 |             else:
209 |                 self._tensor = torch.tensor(value[1])
210 |         else:
211 |             raise ValueError(f"Unsupported audio type: {type(value)}")
212 | 
213 |     def _ipython_display_(self, include=None, exclude=None):
214 |         """
215 |         Displays correctly this type in an ipython notebook (ipython, colab, jupyter, ...)
216 |         """
217 |         from IPython.display import Audio, display
218 | 
219 |         display(Audio(self.to_string(), rate=self.samplerate))
220 | 
221 |     def to_raw(self):
222 |         """
223 |         Returns the "raw" version of that object. It is a `torch.Tensor` object.
224 |         """
225 |         if self._tensor is not None:
226 |             return self._tensor
227 | 
228 |         if self._path is not None:
229 |             if "://" in str(self._path):
230 |                 response = requests.get(self._path)
231 |                 response.raise_for_status()
232 |                 tensor, self.samplerate = sf.read(BytesIO(response.content))
233 |             else:
234 |                 tensor, self.samplerate = sf.read(self._path)
235 |             self._tensor = torch.tensor(tensor)
236 |             return self._tensor
237 | 
238 |     def to_string(self):
239 |         """
240 |         Returns the stringified version of that object. In the case of an AgentAudio, it is a path to the serialized
241 |         version of the audio.
242 |         """
243 |         if self._path is not None:
244 |             return self._path
245 | 
246 |         if self._tensor is not None:
247 |             directory = tempfile.mkdtemp()
248 |             self._path = os.path.join(directory, str(uuid.uuid4()) + ".wav")
249 |             sf.write(self._path, self._tensor, samplerate=self.samplerate)
250 |             return self._path
251 | 
252 | 
253 | AGENT_TYPE_MAPPING = {"string": AgentText, "image": AgentImage, "audio": AgentAudio}
254 | INSTANCE_TYPE_MAPPING = {
255 |     str: AgentText,
256 |     ImageType: AgentImage,
257 |     torch.Tensor: AgentAudio,
258 | }
259 | 
260 | if is_torch_available():
261 |     INSTANCE_TYPE_MAPPING[Tensor] = AgentAudio
262 | 
263 | 
264 | def handle_agent_input_types(*args, **kwargs):
265 |     args = [(arg.to_raw() if isinstance(arg, AgentType) else arg) for arg in args]
266 |     kwargs = {
267 |         k: (v.to_raw() if isinstance(v, AgentType) else v) for k, v in kwargs.items()
268 |     }
269 |     return args, kwargs
270 | 
271 | 
272 | def handle_agent_output_types(output, output_type=None):
273 |     if output_type in AGENT_TYPE_MAPPING:
274 |         # If the class has defined outputs, we can map directly according to the class definition
275 |         decoded_outputs = AGENT_TYPE_MAPPING[output_type](output)
276 |         return decoded_outputs
277 |     else:
278 |         # If the class does not have defined output, then we map according to the type
279 |         for _k, _v in INSTANCE_TYPE_MAPPING.items():
280 |             if isinstance(output, _k):
281 |                 return _v(output)
282 |         return output
283 | 
284 | 
285 | __all__ = ["AgentType", "AgentImage", "AgentText", "AgentAudio"]
286 | 


--------------------------------------------------------------------------------
/src/smolagents/utils.py:
--------------------------------------------------------------------------------
  1 | #!/usr/bin/env python
  2 | # coding=utf-8
  3 | 
  4 | # Copyright 2024 The HuggingFace Inc. team. All rights reserved.
  5 | #
  6 | # Licensed under the Apache License, Version 2.0 (the "License");
  7 | # you may not use this file except in compliance with the License.
  8 | # You may obtain a copy of the License at
  9 | #
 10 | #     http://www.apache.org/licenses/LICENSE-2.0
 11 | #
 12 | # Unless required by applicable law or agreed to in writing, software
 13 | # distributed under the License is distributed on an "AS IS" BASIS,
 14 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 15 | # See the License for the specific language governing permissions and
 16 | # limitations under the License.
 17 | import json
 18 | import re
 19 | from typing import Tuple, Dict, Union
 20 | import ast
 21 | from rich.console import Console
 22 | import inspect
 23 | import types
 24 | 
 25 | from transformers.utils.import_utils import _is_package_available
 26 | 
 27 | _pygments_available = _is_package_available("pygments")
 28 | 
 29 | 
 30 | def is_pygments_available():
 31 |     return _pygments_available
 32 | 
 33 | 
 34 | console = Console()
 35 | 
 36 | BASE_BUILTIN_MODULES = [
 37 |     "collections",
 38 |     "datetime",
 39 |     "itertools",
 40 |     "math",
 41 |     "queue",
 42 |     "random",
 43 |     "re",
 44 |     "stat",
 45 |     "statistics",
 46 |     "time",
 47 |     "unicodedata",
 48 | ]
 49 | 
 50 | 
 51 | class AgentError(Exception):
 52 |     """Base class for other agent-related exceptions"""
 53 | 
 54 |     def __init__(self, message):
 55 |         super().__init__(message)
 56 |         self.message = message
 57 |         console.print(f"[bold red]{message}[/bold red]")
 58 | 
 59 | 
 60 | class AgentParsingError(AgentError):
 61 |     """Exception raised for errors in parsing in the agent"""
 62 | 
 63 |     pass
 64 | 
 65 | 
 66 | class AgentExecutionError(AgentError):
 67 |     """Exception raised for errors in execution in the agent"""
 68 | 
 69 |     pass
 70 | 
 71 | 
 72 | class AgentMaxIterationsError(AgentError):
 73 |     """Exception raised for errors in execution in the agent"""
 74 | 
 75 |     pass
 76 | 
 77 | 
 78 | class AgentGenerationError(AgentError):
 79 |     """Exception raised for errors in generation in the agent"""
 80 | 
 81 |     pass
 82 | 
 83 | 
 84 | def parse_json_blob(json_blob: str) -> Dict[str, str]:
 85 |     try:
 86 |         first_accolade_index = json_blob.find("{")
 87 |         last_accolade_index = [a.start() for a in list(re.finditer("}", json_blob))][-1]
 88 |         json_blob = json_blob[first_accolade_index : last_accolade_index + 1].replace(
 89 |             '\\"', "'"
 90 |         )
 91 |         json_data = json.loads(json_blob, strict=False)
 92 |         return json_data
 93 |     except json.JSONDecodeError as e:
 94 |         place = e.pos
 95 |         if json_blob[place - 1 : place + 2] == "},\n":
 96 |             raise ValueError(
 97 |                 "JSON is invalid: you probably tried to provide multiple tool calls in one action. PROVIDE ONLY ONE TOOL CALL."
 98 |             )
 99 |         raise ValueError(
100 |             f"The JSON blob you used is invalid due to the following error: {e}.\n"
101 |             f"JSON blob was: {json_blob}, decoding failed on that specific part of the blob:\n"
102 |             f"'{json_blob[place-4:place+5]}'."
103 |         )
104 |     except Exception as e:
105 |         raise ValueError(f"Error in parsing the JSON blob: {e}")
106 | 
107 | 
108 | def parse_code_blob(code_blob: str) -> str:
109 |     try:
110 |         pattern = r"```(?:py|python)?\n(.*?)\n```"
111 |         match = re.search(pattern, code_blob, re.DOTALL)
112 |         if match is None:
113 |             raise ValueError(
114 |                 f"No match ground for regex pattern {pattern} in {code_blob=}."
115 |             )
116 |         return match.group(1).strip()
117 | 
118 |     except Exception as e:
119 |         raise ValueError(
120 |             f"""
121 | The code blob you used is invalid: due to the following error: {e}
122 | This means that the regex pattern {pattern} was not respected: make sure to include code with the correct pattern, for instance:
123 | Thoughts: Your thoughts
124 | Code:
125 | ```py
126 | # Your python code here
127 | ```<end_action>"""
128 |         )
129 | 
130 | 
131 | def parse_json_tool_call(json_blob: str) -> Tuple[str, Union[str, None]]:
132 |     json_blob = json_blob.replace("```json", "").replace("```", "")
133 |     tool_call = parse_json_blob(json_blob)
134 |     tool_name_key, tool_arguments_key = None, None
135 |     for possible_tool_name_key in ["action", "tool_name", "tool", "name", "function"]:
136 |         if possible_tool_name_key in tool_call:
137 |             tool_name_key = possible_tool_name_key
138 |     for possible_tool_arguments_key in [
139 |         "action_input",
140 |         "tool_arguments",
141 |         "tool_args",
142 |         "parameters",
143 |     ]:
144 |         if possible_tool_arguments_key in tool_call:
145 |             tool_arguments_key = possible_tool_arguments_key
146 |     if tool_name_key is not None:
147 |         if tool_arguments_key is not None:
148 |             return tool_call[tool_name_key], tool_call[tool_arguments_key]
149 |         else:
150 |             return tool_call[tool_name_key], None
151 |     error_msg = "No tool name key found in tool call!" + f" Tool call: {json_blob}"
152 |     raise AgentParsingError(error_msg)
153 | 
154 | 
155 | MAX_LENGTH_TRUNCATE_CONTENT = 20000
156 | 
157 | 
158 | def truncate_content(
159 |     content: str, max_length: int = MAX_LENGTH_TRUNCATE_CONTENT
160 | ) -> str:
161 |     if len(content) <= max_length:
162 |         return content
163 |     else:
164 |         return (
165 |             content[: MAX_LENGTH_TRUNCATE_CONTENT // 2]
166 |             + f"\n..._This content has been truncated to stay below {max_length} characters_...\n"
167 |             + content[-MAX_LENGTH_TRUNCATE_CONTENT // 2 :]
168 |         )
169 | 
170 | 
171 | class ImportFinder(ast.NodeVisitor):
172 |     def __init__(self):
173 |         self.packages = set()
174 | 
175 |     def visit_Import(self, node):
176 |         for alias in node.names:
177 |             # Get the base package name (before any dots)
178 |             base_package = alias.name.split(".")[0]
179 |             self.packages.add(base_package)
180 | 
181 |     def visit_ImportFrom(self, node):
182 |         if node.module:  # for "from x import y" statements
183 |             # Get the base package name (before any dots)
184 |             base_package = node.module.split(".")[0]
185 |             self.packages.add(base_package)
186 | 
187 | 
188 | def get_method_source(method):
189 |     """Get source code for a method, including bound methods."""
190 |     if isinstance(method, types.MethodType):
191 |         method = method.__func__
192 |     return inspect.getsource(method).strip()
193 | 
194 | 
195 | def is_same_method(method1, method2):
196 |     """Compare two methods by their source code."""
197 |     try:
198 |         source1 = get_method_source(method1)
199 |         source2 = get_method_source(method2)
200 | 
201 |         # Remove method decorators if any
202 |         source1 = "\n".join(
203 |             line for line in source1.split("\n") if not line.strip().startswith("@")
204 |         )
205 |         source2 = "\n".join(
206 |             line for line in source2.split("\n") if not line.strip().startswith("@")
207 |         )
208 | 
209 |         return source1 == source2
210 |     except (TypeError, OSError):
211 |         return False
212 | 
213 | 
214 | def is_same_item(item1, item2):
215 |     """Compare two class items (methods or attributes) for equality."""
216 |     if callable(item1) and callable(item2):
217 |         return is_same_method(item1, item2)
218 |     else:
219 |         return item1 == item2
220 | 
221 | 
222 | def instance_to_source(instance, base_cls=None):
223 |     """Convert an instance to its class source code representation."""
224 |     cls = instance.__class__
225 |     class_name = cls.__name__
226 | 
227 |     # Start building class lines
228 |     class_lines = []
229 |     if base_cls:
230 |         class_lines.append(f"class {class_name}({base_cls.__name__}):")
231 |     else:
232 |         class_lines.append(f"class {class_name}:")
233 | 
234 |     # Add docstring if it exists and differs from base
235 |     if cls.__doc__ and (not base_cls or cls.__doc__ != base_cls.__doc__):
236 |         class_lines.append(f'    """{cls.__doc__}"""')
237 | 
238 |     # Add class-level attributes
239 |     class_attrs = {
240 |         name: value
241 |         for name, value in cls.__dict__.items()
242 |         if not name.startswith("__")
243 |         and not callable(value)
244 |         and not (
245 |             base_cls and hasattr(base_cls, name) and getattr(base_cls, name) == value
246 |         )
247 |     }
248 | 
249 |     for name, value in class_attrs.items():
250 |         if isinstance(value, str):
251 |             if "\n" in value:
252 |                 class_lines.append(f'    {name} = """{value}"""')
253 |             else:
254 |                 class_lines.append(f'    {name} = "{value}"')
255 |         else:
256 |             class_lines.append(f"    {name} = {repr(value)}")
257 | 
258 |     if class_attrs:
259 |         class_lines.append("")
260 | 
261 |     # Add methods
262 |     methods = {
263 |         name: func
264 |         for name, func in cls.__dict__.items()
265 |         if callable(func)
266 |         and not (
267 |             base_cls
268 |             and hasattr(base_cls, name)
269 |             and getattr(base_cls, name).__code__.co_code == func.__code__.co_code
270 |         )
271 |     }
272 | 
273 |     for name, method in methods.items():
274 |         method_source = inspect.getsource(method)
275 |         # Clean up the indentation
276 |         method_lines = method_source.split("\n")
277 |         first_line = method_lines[0]
278 |         indent = len(first_line) - len(first_line.lstrip())
279 |         method_lines = [line[indent:] for line in method_lines]
280 |         method_source = "\n".join(
281 |             ["    " + line if line.strip() else line for line in method_lines]
282 |         )
283 |         class_lines.append(method_source)
284 |         class_lines.append("")
285 | 
286 |     # Find required imports using ImportFinder
287 |     import_finder = ImportFinder()
288 |     import_finder.visit(ast.parse("\n".join(class_lines)))
289 |     required_imports = import_finder.packages
290 | 
291 |     # Build final code with imports
292 |     final_lines = []
293 | 
294 |     # Add base class import if needed
295 |     if base_cls:
296 |         final_lines.append(f"from {base_cls.__module__} import {base_cls.__name__}")
297 | 
298 |     # Add discovered imports
299 |     for package in required_imports:
300 |         final_lines.append(f"import {package}")
301 | 
302 |     if final_lines:  # Add empty line after imports
303 |         final_lines.append("")
304 | 
305 |     # Add the class code
306 |     final_lines.extend(class_lines)
307 | 
308 |     return "\n".join(final_lines)
309 | 
310 | 
311 | __all__ = ["AgentError"]
312 | 


--------------------------------------------------------------------------------
/tests/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/huggingface/smolagents/5991206ae52b1d6d485ffeb918d765c11071cdd1/tests/__init__.py


--------------------------------------------------------------------------------
/tests/fixtures/000000039769.png:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/huggingface/smolagents/5991206ae52b1d6d485ffeb918d765c11071cdd1/tests/fixtures/000000039769.png


--------------------------------------------------------------------------------
/tests/test_agents.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | import os
 16 | import tempfile
 17 | import unittest
 18 | import uuid
 19 | import pytest
 20 | 
 21 | from pathlib import Path
 22 | 
 23 | from smolagents.types import AgentText, AgentImage
 24 | from smolagents.agents import (
 25 |     AgentMaxIterationsError,
 26 |     ManagedAgent,
 27 |     CodeAgent,
 28 |     ToolCallingAgent,
 29 |     Toolbox,
 30 |     ToolCall,
 31 | )
 32 | from smolagents.tools import tool
 33 | from smolagents.default_tools import PythonInterpreterTool
 34 | from transformers.testing_utils import get_tests_dir
 35 | 
 36 | 
 37 | def get_new_path(suffix="") -> str:
 38 |     directory = tempfile.mkdtemp()
 39 |     return os.path.join(directory, str(uuid.uuid4()) + suffix)
 40 | 
 41 | 
 42 | class FakeToolCallModel:
 43 |     def get_tool_call(
 44 |         self, messages, available_tools, stop_sequences=None, grammar=None
 45 |     ):
 46 |         if len(messages) < 3:
 47 |             return "python_interpreter", {"code": "2*3.6452"}, "call_0"
 48 |         else:
 49 |             return "final_answer", {"answer": "7.2904"}, "call_1"
 50 | 
 51 | 
 52 | class FakeToolCallModelImage:
 53 |     def get_tool_call(
 54 |         self, messages, available_tools, stop_sequences=None, grammar=None
 55 |     ):
 56 |         if len(messages) < 3:
 57 |             return (
 58 |                 "fake_image_generation_tool",
 59 |                 {"prompt": "An image of a cat"},
 60 |                 "call_0",
 61 |             )
 62 | 
 63 |         else:  # We're at step 2
 64 |             return "final_answer", "image.png", "call_1"
 65 | 
 66 | 
 67 | def fake_code_model(messages, stop_sequences=None, grammar=None) -> str:
 68 |     prompt = str(messages)
 69 |     if "special_marker" not in prompt:
 70 |         return """
 71 | Thought: I should multiply 2 by 3.6452. special_marker
 72 | Code:
 73 | ```py
 74 | result = 2**3.6452
 75 | ```<end_code>
 76 | """
 77 |     else:  # We're at step 2
 78 |         return """
 79 | Thought: I can now answer the initial question
 80 | Code:
 81 | ```py
 82 | final_answer(7.2904)
 83 | ```<end_code>
 84 | """
 85 | 
 86 | 
 87 | def fake_code_model_error(messages, stop_sequences=None) -> str:
 88 |     prompt = str(messages)
 89 |     if "special_marker" not in prompt:
 90 |         return """
 91 | Thought: I should multiply 2 by 3.6452. special_marker
 92 | Code:
 93 | ```py
 94 | a = 2
 95 | b = a * 2
 96 | print = 2
 97 | print("Ok, calculation done!")
 98 | ```<end_code>
 99 | """
100 |     else:  # We're at step 2
101 |         return """
102 | Thought: I can now answer the initial question
103 | Code:
104 | ```py
105 | final_answer("got an error")
106 | ```<end_code>
107 | """
108 | 
109 | 
110 | def fake_code_model_syntax_error(messages, stop_sequences=None) -> str:
111 |     prompt = str(messages)
112 |     if "special_marker" not in prompt:
113 |         return """
114 | Thought: I should multiply 2 by 3.6452. special_marker
115 | Code:
116 | ```py
117 | a = 2
118 | b = a * 2
119 |     print("Failing due to unexpected indent")
120 | print("Ok, calculation done!")
121 | ```<end_code>
122 | """
123 |     else:  # We're at step 2
124 |         return """
125 | Thought: I can now answer the initial question
126 | Code:
127 | ```py
128 | final_answer("got an error")
129 | ```<end_code>
130 | """
131 | 
132 | 
133 | def fake_code_functiondef(messages, stop_sequences=None) -> str:
134 |     prompt = str(messages)
135 |     if "special_marker" not in prompt:
136 |         return """
137 | Thought: Let's define the function. special_marker
138 | Code:
139 | ```py
140 | import numpy as np
141 | 
142 | def moving_average(x, w):
143 |     return np.convolve(x, np.ones(w), 'valid') / w
144 | ```<end_code>
145 | """
146 |     else:  # We're at step 2
147 |         return """
148 | Thought: I can now answer the initial question
149 | Code:
150 | ```py
151 | x, w = [0, 1, 2, 3, 4, 5], 2
152 | res = moving_average(x, w)
153 | final_answer(res)
154 | ```<end_code>
155 | """
156 | 
157 | 
158 | def fake_code_model_single_step(messages, stop_sequences=None, grammar=None) -> str:
159 |     return """
160 | Thought: I should multiply 2 by 3.6452. special_marker
161 | Code:
162 | ```py
163 | result = python_interpreter(code="2*3.6452")
164 | final_answer(result)
165 | ```
166 | """
167 | 
168 | 
169 | def fake_code_model_no_return(messages, stop_sequences=None, grammar=None) -> str:
170 |     return """
171 | Thought: I should multiply 2 by 3.6452. special_marker
172 | Code:
173 | ```py
174 | result = python_interpreter(code="2*3.6452")
175 | print(result)
176 | ```
177 | """
178 | 
179 | 
180 | class AgentTests(unittest.TestCase):
181 |     def test_fake_single_step_code_agent(self):
182 |         agent = CodeAgent(
183 |             tools=[PythonInterpreterTool()], model=fake_code_model_single_step
184 |         )
185 |         output = agent.run("What is 2 multiplied by 3.6452?", single_step=True)
186 |         assert isinstance(output, str)
187 |         assert "7.2904" in output
188 | 
189 |     def test_fake_toolcalling_agent(self):
190 |         agent = ToolCallingAgent(
191 |             tools=[PythonInterpreterTool()], model=FakeToolCallModel()
192 |         )
193 |         output = agent.run("What is 2 multiplied by 3.6452?")
194 |         assert isinstance(output, str)
195 |         assert "7.2904" in output
196 |         assert agent.logs[1].task == "What is 2 multiplied by 3.6452?"
197 |         assert "7.2904" in agent.logs[2].observations
198 |         assert agent.logs[3].llm_output is None
199 | 
200 |     def test_toolcalling_agent_handles_image_tool_outputs(self):
201 |         from PIL import Image
202 | 
203 |         @tool
204 |         def fake_image_generation_tool(prompt: str) -> Image.Image:
205 |             """Tool that generates an image.
206 | 
207 |             Args:
208 |                 prompt: The prompt
209 |             """
210 |             return Image.open(Path(get_tests_dir("fixtures")) / "000000039769.png")
211 | 
212 |         agent = ToolCallingAgent(
213 |             tools=[fake_image_generation_tool], model=FakeToolCallModelImage()
214 |         )
215 |         output = agent.run("Make me an image.")
216 |         assert isinstance(output, AgentImage)
217 |         assert isinstance(agent.state["image.png"], Image.Image)
218 | 
219 |     def test_fake_code_agent(self):
220 |         agent = CodeAgent(tools=[PythonInterpreterTool()], model=fake_code_model)
221 |         output = agent.run("What is 2 multiplied by 3.6452?")
222 |         assert isinstance(output, float)
223 |         assert output == 7.2904
224 |         assert agent.logs[1].task == "What is 2 multiplied by 3.6452?"
225 |         assert agent.logs[3].tool_call == ToolCall(
226 |             name="python_interpreter", arguments="final_answer(7.2904)", id="call_3"
227 |         )
228 | 
229 |     def test_additional_args_added_to_task(self):
230 |         agent = CodeAgent(tools=[], model=fake_code_model)
231 |         agent.run(
232 |             "What is 2 multiplied by 3.6452?",
233 |             additional_args={"instruction": "Remember this."},
234 |         )
235 |         assert "Remember this" in agent.task
236 |         assert "Remember this" in str(agent.input_messages)
237 | 
238 |     def test_reset_conversations(self):
239 |         agent = CodeAgent(tools=[PythonInterpreterTool()], model=fake_code_model)
240 |         output = agent.run("What is 2 multiplied by 3.6452?", reset=True)
241 |         assert output == 7.2904
242 |         assert len(agent.logs) == 4
243 | 
244 |         output = agent.run("What is 2 multiplied by 3.6452?", reset=False)
245 |         assert output == 7.2904
246 |         assert len(agent.logs) == 6
247 | 
248 |         output = agent.run("What is 2 multiplied by 3.6452?", reset=True)
249 |         assert output == 7.2904
250 |         assert len(agent.logs) == 4
251 | 
252 |     def test_code_agent_code_errors_show_offending_lines(self):
253 |         agent = CodeAgent(tools=[PythonInterpreterTool()], model=fake_code_model_error)
254 |         output = agent.run("What is 2 multiplied by 3.6452?")
255 |         assert isinstance(output, AgentText)
256 |         assert output == "got an error"
257 |         assert "Code execution failed at line 'print = 2' because of" in str(agent.logs)
258 | 
259 |     def test_code_agent_syntax_error_show_offending_lines(self):
260 |         agent = CodeAgent(
261 |             tools=[PythonInterpreterTool()], model=fake_code_model_syntax_error
262 |         )
263 |         output = agent.run("What is 2 multiplied by 3.6452?")
264 |         assert isinstance(output, AgentText)
265 |         assert output == "got an error"
266 |         assert '    print("Failing due to unexpected indent")' in str(agent.logs)
267 | 
268 |     def test_setup_agent_with_empty_toolbox(self):
269 |         ToolCallingAgent(model=FakeToolCallModel(), tools=[])
270 | 
271 |     def test_fails_max_iterations(self):
272 |         agent = CodeAgent(
273 |             tools=[PythonInterpreterTool()],
274 |             model=fake_code_model_no_return,  # use this callable because it never ends
275 |             max_iterations=5,
276 |         )
277 |         agent.run("What is 2 multiplied by 3.6452?")
278 |         assert len(agent.logs) == 8
279 |         assert type(agent.logs[-1].error) is AgentMaxIterationsError
280 | 
281 |     def test_init_agent_with_different_toolsets(self):
282 |         toolset_1 = []
283 |         agent = CodeAgent(tools=toolset_1, model=fake_code_model)
284 |         assert (
285 |             len(agent.toolbox.tools) == 1
286 |         )  # when no tools are provided, only the final_answer tool is added by default
287 | 
288 |         toolset_2 = [PythonInterpreterTool(), PythonInterpreterTool()]
289 |         agent = CodeAgent(tools=toolset_2, model=fake_code_model)
290 |         assert (
291 |             len(agent.toolbox.tools) == 2
292 |         )  # deduplication of tools, so only one python_interpreter tool is added in addition to final_answer
293 | 
294 |         toolset_3 = Toolbox(toolset_2)
295 |         agent = CodeAgent(tools=toolset_3, model=fake_code_model)
296 |         assert (
297 |             len(agent.toolbox.tools) == 2
298 |         )  # same as previous one, where toolset_3 is an instantiation of previous one
299 | 
300 |         # check that add_base_tools will not interfere with existing tools
301 |         with pytest.raises(KeyError) as e:
302 |             agent = ToolCallingAgent(
303 |                 tools=toolset_3, model=FakeToolCallModel(), add_base_tools=True
304 |             )
305 |         assert "already exists in the toolbox" in str(e)
306 | 
307 |         # check that python_interpreter base tool does not get added to code agents
308 |         agent = CodeAgent(tools=[], model=fake_code_model, add_base_tools=True)
309 |         assert (
310 |             len(agent.toolbox.tools) == 3
311 |         )  # added final_answer tool + search + transcribe
312 | 
313 |     def test_function_persistence_across_steps(self):
314 |         agent = CodeAgent(
315 |             tools=[],
316 |             model=fake_code_functiondef,
317 |             max_iterations=2,
318 |             additional_authorized_imports=["numpy"],
319 |         )
320 |         res = agent.run("ok")
321 |         assert res[0] == 0.5
322 | 
323 |     def test_init_managed_agent(self):
324 |         agent = CodeAgent(tools=[], model=fake_code_functiondef)
325 |         managed_agent = ManagedAgent(agent, name="managed_agent", description="Empty")
326 |         assert managed_agent.name == "managed_agent"
327 |         assert managed_agent.description == "Empty"
328 | 
329 |     def test_agent_description_gets_correctly_inserted_in_system_prompt(self):
330 |         agent = CodeAgent(tools=[], model=fake_code_functiondef)
331 |         managed_agent = ManagedAgent(agent, name="managed_agent", description="Empty")
332 |         manager_agent = CodeAgent(
333 |             tools=[],
334 |             model=fake_code_functiondef,
335 |             managed_agents=[managed_agent],
336 |         )
337 |         assert "You can also give requests to team members." not in agent.system_prompt
338 |         print("ok1")
339 |         assert "{{managed_agents_descriptions}}" not in agent.system_prompt
340 |         assert (
341 |             "You can also give requests to team members." in manager_agent.system_prompt
342 |         )
343 | 


--------------------------------------------------------------------------------
/tests/test_all_docs.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | 
 16 | import ast
 17 | import os
 18 | import re
 19 | import shutil
 20 | import tempfile
 21 | import subprocess
 22 | import traceback
 23 | import pytest
 24 | from pathlib import Path
 25 | from typing import List
 26 | from dotenv import load_dotenv
 27 | 
 28 | 
 29 | class SubprocessCallException(Exception):
 30 |     pass
 31 | 
 32 | 
 33 | def run_command(command: List[str], return_stdout=False, env=None):
 34 |     """
 35 |     Runs command with subprocess.check_output and returns stdout if requested.
 36 |     Properly captures and handles errors during command execution.
 37 |     """
 38 |     for i, c in enumerate(command):
 39 |         if isinstance(c, Path):
 40 |             command[i] = str(c)
 41 | 
 42 |     if env is None:
 43 |         env = os.environ.copy()
 44 | 
 45 |     try:
 46 |         output = subprocess.check_output(command, stderr=subprocess.STDOUT, env=env)
 47 |         if return_stdout:
 48 |             if hasattr(output, "decode"):
 49 |                 output = output.decode("utf-8")
 50 |             return output
 51 |     except subprocess.CalledProcessError as e:
 52 |         raise SubprocessCallException(
 53 |             f"Command `{' '.join(command)}` failed with the following error:\n\n{e.output.decode()}"
 54 |         ) from e
 55 | 
 56 | 
 57 | class DocCodeExtractor:
 58 |     """Handles extraction and validation of Python code from markdown files."""
 59 | 
 60 |     @staticmethod
 61 |     def extract_python_code(content: str) -> List[str]:
 62 |         """Extract Python code blocks from markdown content."""
 63 |         pattern = r"```(?:python|py)\n(.*?)\n```"
 64 |         matches = re.finditer(pattern, content, re.DOTALL)
 65 |         return [match.group(1).strip() for match in matches]
 66 | 
 67 |     @staticmethod
 68 |     def create_test_script(code_blocks: List[str], tmp_dir: str) -> Path:
 69 |         """Create a temporary Python script from code blocks."""
 70 |         combined_code = "\n\n".join(code_blocks)
 71 |         assert len(combined_code) > 0, "Code is empty!"
 72 |         tmp_file = Path(tmp_dir) / "test_script.py"
 73 | 
 74 |         with open(tmp_file, "w", encoding="utf-8") as f:
 75 |             f.write(combined_code)
 76 | 
 77 |         return tmp_file
 78 | 
 79 | 
 80 | class TestDocs:
 81 |     """Test case for documentation code testing."""
 82 | 
 83 |     @classmethod
 84 |     def setup_class(cls):
 85 |         cls._tmpdir = tempfile.mkdtemp()
 86 |         cls.launch_args = ["python3"]
 87 |         cls.docs_dir = Path(__file__).parent.parent / "docs" / "source"
 88 |         cls.extractor = DocCodeExtractor()
 89 | 
 90 |         if not cls.docs_dir.exists():
 91 |             raise ValueError(f"Docs directory not found at {cls.docs_dir}")
 92 | 
 93 |         load_dotenv()
 94 |         cls.hf_token = os.getenv("HF_TOKEN")
 95 | 
 96 |         cls.md_files = list(cls.docs_dir.rglob("*.md"))
 97 |         if not cls.md_files:
 98 |             raise ValueError(f"No markdown files found in {cls.docs_dir}")
 99 | 
100 |     @classmethod
101 |     def teardown_class(cls):
102 |         shutil.rmtree(cls._tmpdir)
103 | 
104 |     @pytest.mark.timeout(100)
105 |     def test_single_doc(self, doc_path: Path):
106 |         """Test a single documentation file."""
107 |         with open(doc_path, "r", encoding="utf-8") as f:
108 |             content = f.read()
109 | 
110 |         code_blocks = self.extractor.extract_python_code(content)
111 |         excluded_snippets = [
112 |             "ToolCollection",
113 |             "image_generation_tool",
114 |             "from_langchain",
115 |             "while llm_should_continue(memory):",
116 |         ]
117 |         code_blocks = [
118 |             block
119 |             for block in code_blocks
120 |             if not any(
121 |                 [snippet in block for snippet in excluded_snippets]
122 |             )  # Exclude these tools that take longer to run and add dependencies
123 |         ]
124 |         if len(code_blocks) == 0:
125 |             pytest.skip(f"No Python code blocks found in {doc_path.name}")
126 | 
127 |         # Validate syntax of each block individually by parsing it
128 |         for i, block in enumerate(code_blocks, 1):
129 |             ast.parse(block)
130 | 
131 |         # Create and execute test script
132 |         try:
133 |             code_blocks = [
134 |                 block.replace("<YOUR_HUGGINGFACEHUB_API_TOKEN>", self.hf_token).replace(
135 |                     "{your_username}", "m-ric"
136 |                 )
137 |                 for block in code_blocks
138 |             ]
139 |             test_script = self.extractor.create_test_script(code_blocks, self._tmpdir)
140 |             run_command(self.launch_args + [str(test_script)])
141 | 
142 |         except SubprocessCallException as e:
143 |             pytest.fail(f"\nError while testing {doc_path.name}:\n{str(e)}")
144 |         except Exception:
145 |             pytest.fail(
146 |                 f"\nUnexpected error while testing {doc_path.name}:\n{traceback.format_exc()}"
147 |             )
148 | 
149 |     @pytest.fixture(autouse=True)
150 |     def _setup(self):
151 |         """Fixture to ensure temporary directory exists for each test."""
152 |         os.makedirs(self._tmpdir, exist_ok=True)
153 |         yield
154 |         # Clean up test files after each test
155 |         for file in Path(self._tmpdir).glob("*"):
156 |             file.unlink()
157 | 
158 | 
159 | def pytest_generate_tests(metafunc):
160 |     """Generate test cases for each markdown file."""
161 |     if "doc_path" in metafunc.fixturenames:
162 |         test_class = metafunc.cls
163 | 
164 |         # Initialize the class if needed
165 |         if not hasattr(test_class, "md_files"):
166 |             test_class.setup_class()
167 | 
168 |         # Parameterize with the markdown files
169 |         metafunc.parametrize(
170 |             "doc_path", test_class.md_files, ids=[f.stem for f in test_class.md_files]
171 |         )
172 | 


--------------------------------------------------------------------------------
/tests/test_final_answer.py:
--------------------------------------------------------------------------------
 1 | # coding=utf-8
 2 | # Copyright 2024 HuggingFace Inc.
 3 | #
 4 | # Licensed under the Apache License, Version 2.0 (the "License");
 5 | # you may not use this file except in compliance with the License.
 6 | # You may obtain a copy of the License at
 7 | #
 8 | #     http://www.apache.org/licenses/LICENSE-2.0
 9 | #
10 | # Unless required by applicable law or agreed to in writing, software
11 | # distributed under the License is distributed on an "AS IS" BASIS,
12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
13 | # See the License for the specific language governing permissions and
14 | # limitations under the License.
15 | 
16 | import unittest
17 | from pathlib import Path
18 | 
19 | import numpy as np
20 | from PIL import Image
21 | 
22 | from transformers import is_torch_available
23 | from transformers.testing_utils import get_tests_dir, require_torch
24 | from smolagents.types import AGENT_TYPE_MAPPING
25 | 
26 | from smolagents.default_tools import FinalAnswerTool
27 | 
28 | from .test_tools import ToolTesterMixin
29 | 
30 | 
31 | if is_torch_available():
32 |     import torch
33 | 
34 | 
35 | class FinalAnswerToolTester(unittest.TestCase, ToolTesterMixin):
36 |     def setUp(self):
37 |         self.inputs = {"answer": "Final answer"}
38 |         self.tool = FinalAnswerTool()
39 | 
40 |     def test_exact_match_arg(self):
41 |         result = self.tool("Final answer")
42 |         self.assertEqual(result, "Final answer")
43 | 
44 |     def test_exact_match_kwarg(self):
45 |         result = self.tool(answer=self.inputs["answer"])
46 |         self.assertEqual(result, "Final answer")
47 | 
48 |     def create_inputs(self):
49 |         inputs_text = {"answer": "Text input"}
50 |         inputs_image = {
51 |             "answer": Image.open(
52 |                 Path(get_tests_dir("fixtures")) / "000000039769.png"
53 |             ).resize((512, 512))
54 |         }
55 |         inputs_audio = {"answer": torch.Tensor(np.ones(3000))}
56 |         return {"string": inputs_text, "image": inputs_image, "audio": inputs_audio}
57 | 
58 |     @require_torch
59 |     def test_agent_type_output(self):
60 |         inputs = self.create_inputs()
61 |         for input_type, input in inputs.items():
62 |             output = self.tool(**input, sanitize_inputs_outputs=True)
63 |             agent_type = AGENT_TYPE_MAPPING[input_type]
64 |             self.assertTrue(isinstance(output, agent_type))
65 | 


--------------------------------------------------------------------------------
/tests/test_models.py:
--------------------------------------------------------------------------------
 1 | # coding=utf-8
 2 | # Copyright 2024 HuggingFace Inc.
 3 | #
 4 | # Licensed under the Apache License, Version 2.0 (the "License");
 5 | # you may not use this file except in compliance with the License.
 6 | # You may obtain a copy of the License at
 7 | #
 8 | #     http://www.apache.org/licenses/LICENSE-2.0
 9 | #
10 | # Unless required by applicable law or agreed to in writing, software
11 | # distributed under the License is distributed on an "AS IS" BASIS,
12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
13 | # See the License for the specific language governing permissions and
14 | # limitations under the License.
15 | import unittest
16 | from smolagents import models, tool
17 | from typing import Optional
18 | 
19 | 
20 | class ModelTests(unittest.TestCase):
21 |     def test_get_json_schema_has_nullable_args(self):
22 |         @tool
23 |         def get_weather(location: str, celsius: Optional[bool] = False) -> str:
24 |             """
25 |             Get weather in the next days at given location.
26 |             Secretly this tool does not care about the location, it hates the weather everywhere.
27 | 
28 |             Args:
29 |                 location: the location
30 |                 celsius: the temperature type
31 |             """
32 |             return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
33 | 
34 |         assert (
35 |             "nullable"
36 |             in models.get_json_schema(get_weather)["function"]["parameters"][
37 |                 "properties"
38 |             ]["celsius"]
39 |         )
40 | 


--------------------------------------------------------------------------------
/tests/test_monitoring.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | 
 16 | import unittest
 17 | 
 18 | from smolagents import (
 19 |     AgentImage,
 20 |     AgentError,
 21 |     CodeAgent,
 22 |     ToolCallingAgent,
 23 |     stream_to_gradio,
 24 | )
 25 | 
 26 | 
 27 | class MonitoringTester(unittest.TestCase):
 28 |     def test_code_agent_metrics(self):
 29 |         class FakeLLMModel:
 30 |             def __init__(self):
 31 |                 self.last_input_token_count = 10
 32 |                 self.last_output_token_count = 20
 33 | 
 34 |             def __call__(self, prompt, **kwargs):
 35 |                 return """
 36 | Code:
 37 | ```py
 38 | final_answer('This is the final answer.')
 39 | ```"""
 40 | 
 41 |         agent = CodeAgent(
 42 |             tools=[],
 43 |             model=FakeLLMModel(),
 44 |             max_iterations=1,
 45 |         )
 46 | 
 47 |         agent.run("Fake task")
 48 | 
 49 |         self.assertEqual(agent.monitor.total_input_token_count, 10)
 50 |         self.assertEqual(agent.monitor.total_output_token_count, 20)
 51 | 
 52 |     def test_json_agent_metrics(self):
 53 |         class FakeLLMModel:
 54 |             def __init__(self):
 55 |                 self.last_input_token_count = 10
 56 |                 self.last_output_token_count = 20
 57 | 
 58 |             def get_tool_call(self, prompt, **kwargs):
 59 |                 return "final_answer", {"answer": "image"}, "fake_id"
 60 | 
 61 |         agent = ToolCallingAgent(
 62 |             tools=[],
 63 |             model=FakeLLMModel(),
 64 |             max_iterations=1,
 65 |         )
 66 | 
 67 |         agent.run("Fake task")
 68 | 
 69 |         self.assertEqual(agent.monitor.total_input_token_count, 10)
 70 |         self.assertEqual(agent.monitor.total_output_token_count, 20)
 71 | 
 72 |     def test_code_agent_metrics_max_iterations(self):
 73 |         class FakeLLMModel:
 74 |             def __init__(self):
 75 |                 self.last_input_token_count = 10
 76 |                 self.last_output_token_count = 20
 77 | 
 78 |             def __call__(self, prompt, **kwargs):
 79 |                 return "Malformed answer"
 80 | 
 81 |         agent = CodeAgent(
 82 |             tools=[],
 83 |             model=FakeLLMModel(),
 84 |             max_iterations=1,
 85 |         )
 86 | 
 87 |         agent.run("Fake task")
 88 | 
 89 |         self.assertEqual(agent.monitor.total_input_token_count, 20)
 90 |         self.assertEqual(agent.monitor.total_output_token_count, 40)
 91 | 
 92 |     def test_code_agent_metrics_generation_error(self):
 93 |         class FakeLLMModel:
 94 |             def __init__(self):
 95 |                 self.last_input_token_count = 10
 96 |                 self.last_output_token_count = 20
 97 | 
 98 |             def __call__(self, prompt, **kwargs):
 99 |                 self.last_input_token_count = 10
100 |                 self.last_output_token_count = 0
101 |                 raise Exception("Cannot generate")
102 | 
103 |         agent = CodeAgent(
104 |             tools=[],
105 |             model=FakeLLMModel(),
106 |             max_iterations=1,
107 |         )
108 |         agent.run("Fake task")
109 | 
110 |         self.assertEqual(
111 |             agent.monitor.total_input_token_count, 20
112 |         )  # Should have done two monitoring callbacks
113 |         self.assertEqual(agent.monitor.total_output_token_count, 0)
114 | 
115 |     def test_streaming_agent_text_output(self):
116 |         def dummy_model(prompt, **kwargs):
117 |             return """
118 | Code:
119 | ```py
120 | final_answer('This is the final answer.')
121 | ```"""
122 | 
123 |         agent = CodeAgent(
124 |             tools=[],
125 |             model=dummy_model,
126 |             max_iterations=1,
127 |         )
128 | 
129 |         # Use stream_to_gradio to capture the output
130 |         outputs = list(stream_to_gradio(agent, task="Test task", test_mode=True))
131 | 
132 |         self.assertEqual(len(outputs), 4)
133 |         final_message = outputs[-1]
134 |         self.assertEqual(final_message.role, "assistant")
135 |         self.assertIn("This is the final answer.", final_message.content)
136 | 
137 |     def test_streaming_agent_image_output(self):
138 |         class FakeLLM:
139 |             def __init__(self):
140 |                 pass
141 | 
142 |             def get_tool_call(self, messages, **kwargs):
143 |                 return "final_answer", {"answer": "image"}, "fake_id"
144 | 
145 |         agent = ToolCallingAgent(
146 |             tools=[],
147 |             model=FakeLLM(),
148 |             max_iterations=1,
149 |         )
150 | 
151 |         # Use stream_to_gradio to capture the output
152 |         outputs = list(
153 |             stream_to_gradio(
154 |                 agent,
155 |                 task="Test task",
156 |                 additional_args=dict(image=AgentImage(value="path.png")),
157 |                 test_mode=True,
158 |             )
159 |         )
160 | 
161 |         self.assertEqual(len(outputs), 3)
162 |         final_message = outputs[-1]
163 |         self.assertEqual(final_message.role, "assistant")
164 |         self.assertIsInstance(final_message.content, dict)
165 |         self.assertEqual(final_message.content["path"], "path.png")
166 |         self.assertEqual(final_message.content["mime_type"], "image/png")
167 | 
168 |     def test_streaming_with_agent_error(self):
169 |         def dummy_model(prompt, **kwargs):
170 |             raise AgentError("Simulated agent error")
171 | 
172 |         agent = CodeAgent(
173 |             tools=[],
174 |             model=dummy_model,
175 |             max_iterations=1,
176 |         )
177 | 
178 |         # Use stream_to_gradio to capture the output
179 |         outputs = list(stream_to_gradio(agent, task="Test task", test_mode=True))
180 | 
181 |         self.assertEqual(len(outputs), 5)
182 |         final_message = outputs[-1]
183 |         self.assertEqual(final_message.role, "assistant")
184 |         self.assertIn("Simulated agent error", final_message.content)
185 | 


--------------------------------------------------------------------------------
/tests/test_search.py:
--------------------------------------------------------------------------------
 1 | # coding=utf-8
 2 | # Copyright 2024 HuggingFace Inc.
 3 | #
 4 | # Licensed under the Apache License, Version 2.0 (the "License");
 5 | # you may not use this file except in compliance with the License.
 6 | # You may obtain a copy of the License at
 7 | #
 8 | #     http://www.apache.org/licenses/LICENSE-2.0
 9 | #
10 | # Unless required by applicable law or agreed to in writing, software
11 | # distributed under the License is distributed on an "AS IS" BASIS,
12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
13 | # See the License for the specific language governing permissions and
14 | # limitations under the License.
15 | 
16 | import unittest
17 | 
18 | from smolagents import load_tool
19 | 
20 | from .test_tools import ToolTesterMixin
21 | 
22 | 
23 | class DuckDuckGoSearchToolTester(unittest.TestCase, ToolTesterMixin):
24 |     def setUp(self):
25 |         self.tool = load_tool("web_search")
26 |         self.tool.setup()
27 | 
28 |     def test_exact_match_arg(self):
29 |         result = self.tool("Agents")
30 |         assert isinstance(result, str)
31 | 


--------------------------------------------------------------------------------
/tests/test_tools.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | import unittest
 16 | from pathlib import Path
 17 | from typing import Dict, Union, Optional
 18 | 
 19 | import numpy as np
 20 | import pytest
 21 | 
 22 | from transformers import is_torch_available, is_vision_available
 23 | from smolagents.types import (
 24 |     AGENT_TYPE_MAPPING,
 25 |     AgentAudio,
 26 |     AgentImage,
 27 |     AgentText,
 28 | )
 29 | from smolagents.tools import Tool, tool, AUTHORIZED_TYPES
 30 | from transformers.testing_utils import get_tests_dir
 31 | 
 32 | 
 33 | if is_torch_available():
 34 |     import torch
 35 | 
 36 | if is_vision_available():
 37 |     from PIL import Image
 38 | 
 39 | 
 40 | def create_inputs(tool_inputs: Dict[str, Dict[Union[str, type], str]]):
 41 |     inputs = {}
 42 | 
 43 |     for input_name, input_desc in tool_inputs.items():
 44 |         input_type = input_desc["type"]
 45 | 
 46 |         if input_type == "string":
 47 |             inputs[input_name] = "Text input"
 48 |         elif input_type == "image":
 49 |             inputs[input_name] = Image.open(
 50 |                 Path(get_tests_dir("fixtures")) / "000000039769.png"
 51 |             ).resize((512, 512))
 52 |         elif input_type == "audio":
 53 |             inputs[input_name] = np.ones(3000)
 54 |         else:
 55 |             raise ValueError(f"Invalid type requested: {input_type}")
 56 | 
 57 |     return inputs
 58 | 
 59 | 
 60 | def output_type(output):
 61 |     if isinstance(output, (str, AgentText)):
 62 |         return "string"
 63 |     elif isinstance(output, (Image.Image, AgentImage)):
 64 |         return "image"
 65 |     elif isinstance(output, (torch.Tensor, AgentAudio)):
 66 |         return "audio"
 67 |     else:
 68 |         raise TypeError(f"Invalid output: {output}")
 69 | 
 70 | 
 71 | class ToolTesterMixin:
 72 |     def test_inputs_output(self):
 73 |         self.assertTrue(hasattr(self.tool, "inputs"))
 74 |         self.assertTrue(hasattr(self.tool, "output_type"))
 75 | 
 76 |         inputs = self.tool.inputs
 77 |         self.assertTrue(isinstance(inputs, dict))
 78 | 
 79 |         for _, input_spec in inputs.items():
 80 |             self.assertTrue("type" in input_spec)
 81 |             self.assertTrue("description" in input_spec)
 82 |             self.assertTrue(input_spec["type"] in AUTHORIZED_TYPES)
 83 |             self.assertTrue(isinstance(input_spec["description"], str))
 84 | 
 85 |         output_type = self.tool.output_type
 86 |         self.assertTrue(output_type in AUTHORIZED_TYPES)
 87 | 
 88 |     def test_common_attributes(self):
 89 |         self.assertTrue(hasattr(self.tool, "description"))
 90 |         self.assertTrue(hasattr(self.tool, "name"))
 91 |         self.assertTrue(hasattr(self.tool, "inputs"))
 92 |         self.assertTrue(hasattr(self.tool, "output_type"))
 93 | 
 94 |     def test_agent_type_output(self):
 95 |         inputs = create_inputs(self.tool.inputs)
 96 |         output = self.tool(**inputs, sanitize_inputs_outputs=True)
 97 |         if self.tool.output_type != "any":
 98 |             agent_type = AGENT_TYPE_MAPPING[self.tool.output_type]
 99 |             self.assertTrue(isinstance(output, agent_type))
100 | 
101 | 
102 | class ToolTests(unittest.TestCase):
103 |     def test_tool_init_with_decorator(self):
104 |         @tool
105 |         def coolfunc(a: str, b: int) -> float:
106 |             """Cool function
107 | 
108 |             Args:
109 |                 a: The first argument
110 |                 b: The second one
111 |             """
112 |             return b + 2, a
113 | 
114 |         assert coolfunc.output_type == "number"
115 | 
116 |     def test_tool_init_vanilla(self):
117 |         class HFModelDownloadsTool(Tool):
118 |             name = "model_download_counter"
119 |             description = """
120 |             This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
121 |             It returns the name of the checkpoint."""
122 | 
123 |             inputs = {
124 |                 "task": {
125 |                     "type": "string",
126 |                     "description": "the task category (such as text-classification, depth-estimation, etc)",
127 |                 }
128 |             }
129 |             output_type = "string"
130 | 
131 |             def forward(self, task: str) -> str:
132 |                 return "best model"
133 | 
134 |         tool = HFModelDownloadsTool()
135 |         assert list(tool.inputs.keys())[0] == "task"
136 | 
137 |     def test_tool_init_decorator_raises_issues(self):
138 |         with pytest.raises(Exception) as e:
139 | 
140 |             @tool
141 |             def coolfunc(a: str, b: int):
142 |                 """Cool function
143 | 
144 |                 Args:
145 |                     a: The first argument
146 |                     b: The second one
147 |                 """
148 |                 return a + b
149 | 
150 |             assert coolfunc.output_type == "number"
151 |         assert "Tool return type not found" in str(e)
152 | 
153 |         with pytest.raises(Exception) as e:
154 | 
155 |             @tool
156 |             def coolfunc(a: str, b: int) -> int:
157 |                 """Cool function
158 | 
159 |                 Args:
160 |                     a: The first argument
161 |                 """
162 |                 return b + a
163 | 
164 |             assert coolfunc.output_type == "number"
165 |         assert "docstring has no description for the argument" in str(e)
166 | 
167 |     def test_saving_tool_raises_error_imports_outside_function(self):
168 |         with pytest.raises(Exception) as e:
169 |             import numpy as np
170 | 
171 |             @tool
172 |             def get_current_time() -> str:
173 |                 """
174 |                 Gets the current time.
175 |                 """
176 |                 return str(np.random.random())
177 | 
178 |             get_current_time.save("output")
179 | 
180 |         assert "np" in str(e)
181 | 
182 |         # Also test with classic definition
183 |         with pytest.raises(Exception) as e:
184 | 
185 |             class GetCurrentTimeTool(Tool):
186 |                 name = "get_current_time_tool"
187 |                 description = "Gets the current time"
188 |                 inputs = {}
189 |                 output_type = "string"
190 | 
191 |                 def forward(self):
192 |                     return str(np.random.random())
193 | 
194 |             get_current_time = GetCurrentTimeTool()
195 |             get_current_time.save("output")
196 | 
197 |         assert "np" in str(e)
198 | 
199 |     def test_tool_definition_raises_no_error_imports_in_function(self):
200 |         @tool
201 |         def get_current_time() -> str:
202 |             """
203 |             Gets the current time.
204 |             """
205 |             from datetime import datetime
206 | 
207 |             return str(datetime.now())
208 | 
209 |         class GetCurrentTimeTool(Tool):
210 |             name = "get_current_time_tool"
211 |             description = "Gets the current time"
212 |             inputs = {}
213 |             output_type = "string"
214 | 
215 |             def forward(self):
216 |                 from datetime import datetime
217 | 
218 |                 return str(datetime.now())
219 | 
220 |     def test_saving_tool_allows_no_arg_in_init(self):
221 |         # Test one cannot save tool with additional args in init
222 |         class FailTool(Tool):
223 |             name = "specific"
224 |             description = "test description"
225 |             inputs = {
226 |                 "string_input": {"type": "string", "description": "input description"}
227 |             }
228 |             output_type = "string"
229 | 
230 |             def __init__(self, url):
231 |                 super().__init__(self)
232 |                 self.url = "none"
233 | 
234 |             def forward(self, string_input: str) -> str:
235 |                 return self.url + string_input
236 | 
237 |         fail_tool = FailTool("dummy_url")
238 |         with pytest.raises(Exception) as e:
239 |             fail_tool.save("output")
240 |         assert "__init__" in str(e)
241 | 
242 |     def test_saving_tool_allows_no_imports_from_outside_methods(self):
243 |         # Test that using imports from outside functions fails
244 |         import numpy as np
245 | 
246 |         class FailTool(Tool):
247 |             name = "specific"
248 |             description = "test description"
249 |             inputs = {
250 |                 "string_input": {"type": "string", "description": "input description"}
251 |             }
252 |             output_type = "string"
253 | 
254 |             def useless_method(self):
255 |                 self.client = np.random.random()
256 |                 return ""
257 | 
258 |             def forward(self, string_input):
259 |                 return self.useless_method() + string_input
260 | 
261 |         fail_tool = FailTool()
262 |         with pytest.raises(Exception) as e:
263 |             fail_tool.save("output")
264 |         assert "'np' is undefined" in str(e)
265 | 
266 |         # Test that putting these imports inside functions works
267 |         class SuccessTool(Tool):
268 |             name = "specific"
269 |             description = "test description"
270 |             inputs = {
271 |                 "string_input": {"type": "string", "description": "input description"}
272 |             }
273 |             output_type = "string"
274 | 
275 |             def useless_method(self):
276 |                 import numpy as np
277 | 
278 |                 self.client = np.random.random()
279 |                 return ""
280 | 
281 |             def forward(self, string_input):
282 |                 return self.useless_method() + string_input
283 | 
284 |         success_tool = SuccessTool()
285 |         success_tool.save("output")
286 | 
287 |     def test_tool_missing_class_attributes_raises_error(self):
288 |         with pytest.raises(Exception) as e:
289 | 
290 |             class GetWeatherTool(Tool):
291 |                 name = "get_weather"
292 |                 description = "Get weather in the next days at given location."
293 |                 inputs = {
294 |                     "location": {"type": "string", "description": "the location"},
295 |                     "celsius": {
296 |                         "type": "string",
297 |                         "description": "the temperature type",
298 |                     },
299 |                 }
300 | 
301 |                 def forward(
302 |                     self, location: str, celsius: Optional[bool] = False
303 |                 ) -> str:
304 |                     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
305 | 
306 |             GetWeatherTool()
307 |         assert "You must set an attribute output_type" in str(e)
308 | 
309 |     def test_tool_from_decorator_optional_args(self):
310 |         @tool
311 |         def get_weather(location: str, celsius: Optional[bool] = False) -> str:
312 |             """
313 |             Get weather in the next days at given location.
314 |             Secretly this tool does not care about the location, it hates the weather everywhere.
315 | 
316 |             Args:
317 |                 location: the location
318 |                 celsius: the temperature type
319 |             """
320 |             return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
321 | 
322 |         assert "nullable" in get_weather.inputs["celsius"]
323 |         assert get_weather.inputs["celsius"]["nullable"]
324 |         assert "nullable" not in get_weather.inputs["location"]
325 | 
326 |     def test_tool_mismatching_nullable_args_raises_error(self):
327 |         with pytest.raises(Exception) as e:
328 | 
329 |             class GetWeatherTool(Tool):
330 |                 name = "get_weather"
331 |                 description = "Get weather in the next days at given location."
332 |                 inputs = {
333 |                     "location": {"type": "string", "description": "the location"},
334 |                     "celsius": {
335 |                         "type": "string",
336 |                         "description": "the temperature type",
337 |                     },
338 |                 }
339 |                 output_type = "string"
340 | 
341 |                 def forward(
342 |                     self, location: str, celsius: Optional[bool] = False
343 |                 ) -> str:
344 |                     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
345 | 
346 |             GetWeatherTool()
347 |         assert "Nullable" in str(e)
348 | 
349 |         with pytest.raises(Exception) as e:
350 | 
351 |             class GetWeatherTool2(Tool):
352 |                 name = "get_weather"
353 |                 description = "Get weather in the next days at given location."
354 |                 inputs = {
355 |                     "location": {"type": "string", "description": "the location"},
356 |                     "celsius": {
357 |                         "type": "string",
358 |                         "description": "the temperature type",
359 |                     },
360 |                 }
361 |                 output_type = "string"
362 | 
363 |                 def forward(self, location: str, celsius: bool = False) -> str:
364 |                     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
365 | 
366 |             GetWeatherTool2()
367 |         assert "Nullable" in str(e)
368 | 
369 |         with pytest.raises(Exception) as e:
370 | 
371 |             class GetWeatherTool3(Tool):
372 |                 name = "get_weather"
373 |                 description = "Get weather in the next days at given location."
374 |                 inputs = {
375 |                     "location": {"type": "string", "description": "the location"},
376 |                     "celsius": {
377 |                         "type": "string",
378 |                         "description": "the temperature type",
379 |                         "nullable": True,
380 |                     },
381 |                 }
382 |                 output_type = "string"
383 | 
384 |                 def forward(self, location, celsius: str) -> str:
385 |                     return "The weather is UNGODLY with torrential rains and temperatures below -10°C"
386 | 
387 |             GetWeatherTool3()
388 |         assert "Nullable" in str(e)
389 | 


--------------------------------------------------------------------------------
/tests/test_types.py:
--------------------------------------------------------------------------------
  1 | # coding=utf-8
  2 | # Copyright 2024 HuggingFace Inc.
  3 | #
  4 | # Licensed under the Apache License, Version 2.0 (the "License");
  5 | # you may not use this file except in compliance with the License.
  6 | # You may obtain a copy of the License at
  7 | #
  8 | #     http://www.apache.org/licenses/LICENSE-2.0
  9 | #
 10 | # Unless required by applicable law or agreed to in writing, software
 11 | # distributed under the License is distributed on an "AS IS" BASIS,
 12 | # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 13 | # See the License for the specific language governing permissions and
 14 | # limitations under the License.
 15 | import os
 16 | import tempfile
 17 | import unittest
 18 | import uuid
 19 | from pathlib import Path
 20 | 
 21 | from smolagents.types import AgentAudio, AgentImage, AgentText
 22 | from transformers.testing_utils import (
 23 |     require_soundfile,
 24 |     require_torch,
 25 |     require_vision,
 26 | )
 27 | from transformers.utils import (
 28 |     is_soundfile_availble,
 29 | )
 30 | 
 31 | import torch
 32 | from PIL import Image
 33 | 
 34 | 
 35 | if is_soundfile_availble():
 36 |     import soundfile as sf
 37 | 
 38 | 
 39 | def get_new_path(suffix="") -> str:
 40 |     directory = tempfile.mkdtemp()
 41 |     return os.path.join(directory, str(uuid.uuid4()) + suffix)
 42 | 
 43 | 
 44 | @require_soundfile
 45 | @require_torch
 46 | class AgentAudioTests(unittest.TestCase):
 47 |     def test_from_tensor(self):
 48 |         tensor = torch.rand(12, dtype=torch.float64) - 0.5
 49 |         agent_type = AgentAudio(tensor)
 50 |         path = str(agent_type.to_string())
 51 | 
 52 |         # Ensure that the tensor and the agent_type's tensor are the same
 53 |         self.assertTrue(torch.allclose(tensor, agent_type.to_raw(), atol=1e-4))
 54 | 
 55 |         del agent_type
 56 | 
 57 |         # Ensure the path remains even after the object deletion
 58 |         self.assertTrue(os.path.exists(path))
 59 | 
 60 |         # Ensure that the file contains the same value as the original tensor
 61 |         new_tensor, _ = sf.read(path)
 62 |         self.assertTrue(torch.allclose(tensor, torch.tensor(new_tensor), atol=1e-4))
 63 | 
 64 |     def test_from_string(self):
 65 |         tensor = torch.rand(12, dtype=torch.float64) - 0.5
 66 |         path = get_new_path(suffix=".wav")
 67 |         sf.write(path, tensor, 16000)
 68 | 
 69 |         agent_type = AgentAudio(path)
 70 | 
 71 |         self.assertTrue(torch.allclose(tensor, agent_type.to_raw(), atol=1e-4))
 72 |         self.assertEqual(agent_type.to_string(), path)
 73 | 
 74 | 
 75 | @require_vision
 76 | @require_torch
 77 | class AgentImageTests(unittest.TestCase):
 78 |     def test_from_tensor(self):
 79 |         tensor = torch.randint(0, 256, (64, 64, 3))
 80 |         agent_type = AgentImage(tensor)
 81 |         path = str(agent_type.to_string())
 82 | 
 83 |         # Ensure that the tensor and the agent_type's tensor are the same
 84 |         self.assertTrue(torch.allclose(tensor, agent_type._tensor, atol=1e-4))
 85 | 
 86 |         self.assertIsInstance(agent_type.to_raw(), Image.Image)
 87 | 
 88 |         # Ensure the path remains even after the object deletion
 89 |         del agent_type
 90 |         self.assertTrue(os.path.exists(path))
 91 | 
 92 |     def test_from_string(self):
 93 |         path = Path("tests/fixtures/000000039769.png")
 94 |         image = Image.open(path)
 95 |         agent_type = AgentImage(path)
 96 | 
 97 |         self.assertTrue(path.samefile(agent_type.to_string()))
 98 |         self.assertTrue(image == agent_type.to_raw())
 99 | 
100 |         # Ensure the path remains even after the object deletion
101 |         del agent_type
102 |         self.assertTrue(os.path.exists(path))
103 | 
104 |     def test_from_image(self):
105 |         path = Path("tests/fixtures/000000039769.png")
106 |         image = Image.open(path)
107 |         agent_type = AgentImage(image)
108 | 
109 |         self.assertFalse(path.samefile(agent_type.to_string()))
110 |         self.assertTrue(image == agent_type.to_raw())
111 | 
112 |         # Ensure the path remains even after the object deletion
113 |         del agent_type
114 |         self.assertTrue(os.path.exists(path))
115 | 
116 | 
117 | class AgentTextTests(unittest.TestCase):
118 |     def test_from_string(self):
119 |         string = "Hey!"
120 |         agent_type = AgentText(string)
121 | 
122 |         self.assertEqual(string, agent_type.to_string())
123 |         self.assertEqual(string, agent_type.to_raw())
124 |         self.assertEqual(string, agent_type)
125 | 


--------------------------------------------------------------------------------
/tests/test_utils.py:
--------------------------------------------------------------------------------
 1 | import os
 2 | import unittest
 3 | import shutil
 4 | import tempfile
 5 | 
 6 | from pathlib import Path
 7 | 
 8 | 
 9 | def str_to_bool(value) -> int:
10 |     """
11 |     Converts a string representation of truth to `True` (1) or `False` (0).
12 | 
13 |     True values are `y`, `yes`, `t`, `true`, `on`, and `1`; False value are `n`, `no`, `f`, `false`, `off`, and `0`;
14 |     """
15 |     value = value.lower()
16 |     if value in ("y", "yes", "t", "true", "on", "1"):
17 |         return 1
18 |     elif value in ("n", "no", "f", "false", "off", "0"):
19 |         return 0
20 |     else:
21 |         raise ValueError(f"invalid truth value {value}")
22 | 
23 | 
24 | def get_int_from_env(env_keys, default):
25 |     """Returns the first positive env value found in the `env_keys` list or the default."""
26 |     for e in env_keys:
27 |         val = int(os.environ.get(e, -1))
28 |         if val >= 0:
29 |             return val
30 |     return default
31 | 
32 | 
33 | def parse_flag_from_env(key, default=False):
34 |     """Returns truthy value for `key` from the env if available else the default."""
35 |     value = os.environ.get(key, str(default))
36 |     return (
37 |         str_to_bool(value) == 1
38 |     )  # As its name indicates `str_to_bool` actually returns an int...
39 | 
40 | 
41 | _run_slow_tests = parse_flag_from_env("RUN_SLOW", default=False)
42 | 
43 | 
44 | def skip(test_case):
45 |     "Decorator that skips a test unconditionally"
46 |     return unittest.skip("Test was skipped")(test_case)
47 | 
48 | 
49 | def slow(test_case):
50 |     """
51 |     Decorator marking a test as slow. Slow tests are skipped by default. Set the RUN_SLOW environment variable to a
52 |     truthy value to run them.
53 |     """
54 |     return unittest.skipUnless(_run_slow_tests, "test is slow")(test_case)
55 | 
56 | 
57 | class TempDirTestCase(unittest.TestCase):
58 |     """
59 |     A TestCase class that keeps a single `tempfile.TemporaryDirectory` open for the duration of the class, wipes its
60 |     data at the start of a test, and then destroyes it at the end of the TestCase.
61 | 
62 |     Useful for when a class or API requires a single constant folder throughout it's use, such as Weights and Biases
63 | 
64 |     The temporary directory location will be stored in `self.tmpdir`
65 |     """
66 | 
67 |     clear_on_setup = True
68 | 
69 |     @classmethod
70 |     def setUpClass(cls):
71 |         "Creates a `tempfile.TemporaryDirectory` and stores it in `cls.tmpdir`"
72 |         cls.tmpdir = Path(tempfile.mkdtemp())
73 | 
74 |     @classmethod
75 |     def tearDownClass(cls):
76 |         "Remove `cls.tmpdir` after test suite has finished"
77 |         if os.path.exists(cls.tmpdir):
78 |             shutil.rmtree(cls.tmpdir)
79 | 
80 |     def setUp(self):
81 |         "Destroy all contents in `self.tmpdir`, but not `self.tmpdir`"
82 |         if self.clear_on_setup:
83 |             for path in self.tmpdir.glob("**/*"):
84 |                 if path.is_file():
85 |                     path.unlink()
86 |                 elif path.is_dir():
87 |                     shutil.rmtree(path)
88 | 