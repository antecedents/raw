<br>

## Environments

### Remote Development

For this Python project/template, the remote development environment requires

* [Dockerfile](../.devcontainer/Dockerfile)
* [requirements.txt](../.devcontainer/requirements.txt)

An image is built via the command

```shell
docker build . --file .devcontainer/Dockerfile -t uncertainty
```

On success, the output of

```shell
docker images
```

should include

<br>

| repository  | tag    | image id | created  | size     |
|:------------|:-------|:---------|:---------|:---------|
| uncertainty | latest | $\ldots$ | $\ldots$ | $\ldots$ |


<br>

Subsequently, run a container, i.e., an instance, of the image `uncertainty` via:

<br>


```shell
docker run --rm -i -t -p 8000:8000  
    -w /app --mount type=bind,src="$(pwd)",target=/app 
      -v ~/.aws:/root/.aws uncertainty
```

<br>

Herein, `-p 8000:8000` maps the host port `8000` to container port `8000`.  Note, the container's working environment, i.e., -w, must be inline with this project's top directory.  Additionally

* --rm: [automatically remove container](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the)
* -i: [interact](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di)
* -t: [tag](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your)
* -p: [publish](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s)

<br>

The part `-v ~/.aws:/root/.aws` ascertains Amazon Web Services interactions via containers. Get the name of the running instance of ``uncertainty`` via:

```shell
docker ps --all
```

Never deploy a root container.

<br>

### Remote Development & Integrated Development Environments

An IDE (integrated development environment) is a helpful remote development tool.  The **IntelliJ
IDEA** set up involves connecting to a machine's Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker), the steps are

<br>

> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** {select the linux operating system}
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

<br>

**Visual Studio Code** has its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).

<br>
<br>



## Code Analysis

The GitHub Actions script [main.yml](../.github/workflows/main.yml) conducts code analysis within a Cloud GitHub Workspace.  Depending on the script, code analysis may occur `on push` to any repository branch, or `on push` to a specific branch.

The sections herein outline remote code analysis.

<br>

### pylint

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Analyse a directory via the command

```shell
python -m pylint --rcfile .pylintrc {directory}
```

The `.pylintrc` file of this template project has been **amended to adhere to team norms**, including

* Maximum number of characters on a single line.
  > max-line-length=127

* Maximum number of lines in a module.
  > max-module-lines=135


<br>


### pytest & pytest coverage

The directive patterns

```shell
python -m pytest tests/{directory.name}/...py
pytest --cov-report term-missing  --cov src/{directory.name}/...py tests/{directory.name}/...py
```

for test and test coverage, respectively.


<br>


### flake8

For code & complexity analysis.  A directive of the form

```bash
python -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics src/...
```

inspects issues in relation to logic (F7), syntax (Python E9, Flake F7), mathematical formulae symbols (F63), undefined variable names (F82).  Additionally

```shell
python -m flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics src/...
```

inspects complexity.


<br>
<br>


## References

### Articles

* [Population Based Training](https://deepmind.google/discover/blog/population-based-training-of-neural-networks/), ([paper](https://arxiv.org/abs/1711.09846))

<br>

### Modelling

#### Configuring, etc.

* [AutoModel.from_pretrained](https://huggingface.co/docs/transformers/v4.42.0/en/model_doc/auto#transformers.AutoModel.from_pretrained)
  * [pre-trained configuration](https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/configuration#transformers.PretrainedConfig)
  * [PreTrainedTokenizerFast](https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/tokenizer#transformers.PreTrainedTokenizerFast)

* [Configurations of tasks that include text generation steps](https://huggingface.co/docs/transformers/main_classes/text_generation)
  * Beware, configuration settings methods are undergoing changes.  Instead: [default text generation configuration.](https://huggingface.co/docs/transformers/generation_strategies#default-text-generation-configuration)
  * [generation configuration](https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/text_generation#transformers.GenerationConfig)
  * [from_pretrained](https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/text_generation#transformers.GenerationConfig.from_pretrained)

<br>

#### Hyperparameters

* [Hyperparameter Tuning with Ray Tune](https://docs.ray.io/en/latest/train/user-guides/hyperparameter-optimization.html)
  * [Getting Started with Ray Tune](https://docs.ray.io/en/latest/tune/getting-started.html)
  * [train hyperparameter search](https://docs.ray.io/en/latest/tune/examples/pbt_transformers.html)
  * [Logging and Outputs in Tune](https://docs.ray.io/en/latest/tune/tutorials/tune-output.html)
  * [Tune Experiments](https://docs.ray.io/en/latest/tune/examples/tune_analyze_results.html)

* [Using Huggingface Transformers with Tune](https://docs.ray.io/en/latest/tune/examples/pbt_transformers.html)
  * [Configure PBT and Tuner](https://docs.ray.io/en/latest/tune/examples/pbt_visualization/pbt_visualization.html)
  * [ray.tune.schedulers.PopulationBasedTraining](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.PopulationBasedTraining.html), [schedulers](https://docs.ray.io/en/latest/tune/api/schedulers.html)
  * [ray.tune.Tuner](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.Tuner.html)
  * [tune_basic_example](https://docs.ray.io/en/latest/tune/examples/includes/tune_basic_example.html)
  * [A Guide To Parallelism and Resources for Ray Tune](https://docs.ray.io/en/latest/tune/tutorials/tune-resources.html)

<br>

#### Logging: Model & System
* [Logging and Outputs in Tune](https://docs.ray.io/en/latest/tune/tutorials/tune-output.html)
  * And, using TensorBoard
  * [Loggers](https://docs.ray.io/en/latest/tune/tutorials/tune-output.html#how-to-build-custom-tune-loggers)
  * [Logging](https://docs.ray.io/en/latest/tune/examples/includes/logging_example.html)
* [TensorboardX](https://tensorboardx.readthedocs.io/en/latest/tutorial.html#what-is-tensorboard-x) (Pytorch)
* [Ray Dashboard: Getting Started](https://docs.ray.io/en/latest/ray-observability/getting-started.html)
* [Ray, Grafana, Prometheus](https://docs.ray.io/en/latest/cluster/configure-manage-dashboard.html#embed-grafana-visualizations-into-ray-dashboard)
* [ray.init()](https://docs.ray.io/en/latest/ray-core/api/doc/ray.init.html)
* [Application & Cluster Metrics](https://docs.ray.io/en/latest/cluster/metrics.html)
* [Usage Stats Collection](https://docs.ray.io/en/latest/cluster/usage-stats.html)
* [seqeval](https://huggingface.co/spaces/evaluate-metric/seqeval/blob/main/seqeval.py)

<br>

#### Distributed Training
* [Distributed Communication](https://docs.w3cub.com/pytorch/distributed.html)
* [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist_overview.html)
* [Get Started with Distributed Training using Hugging Face Transformers](https://docs.ray.io/en/latest/train/getting-started-transformers.html)
* [Get Started with Distributed Training using Hugging Face Transformers](https://docs.ray.io/en/latest/train/getting-started-transformers.html#transformerstrainer-migration-guide)
* [Token classification](https://huggingface.co/docs/transformers/tasks/token_classification)


<br>

#### File Formats
* GGUF: GPT-Generated Unified Format[^gpt]
* GGML: GPT-Generated Model Language
* [What is GGUF and GGML?](https://medium.com/@phillipgimmi/what-is-gguf-and-ggml-e364834d241c)
* [About GGUF](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
* [to GGUF](https://medium.com/@qdrddr/the-easiest-way-to-convert-a-model-to-gguf-and-quantize-91016e97c987)
* [to GGUF discussion](https://github.com/ggerganov/llama.cpp/discussions/2948)
* [Hugging Face & GGUF](https://huggingface.co/docs/hub/gguf)

<br>

### Docker, etc.

* [Setup Grafana with Prometheus for Python projects using Docker](https://dev.to/thedevtimeline/setup-grafana-with-prometheus-for-python-projects-using-docker-4o5g)
* [Interactive shell using Docker Compose](https://betterstack.com/community/questions/question-interactive-shell-using-docker-compose/)
* [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/)
* [Development Environments](https://docs.docker.com/compose/intro/features-uses/#development-environments)
* [Interactive Shell Using Docker](https://www.baeldung.com/ops/docker-compose-interactive-shell)
* [Remote Development](https://www.docker.com/blog/containerized-python-development-part-1/)
* [Django Development with Docker Compose and Machine](https://realpython.com/django-development-with-docker-compose-and-machine/)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>

[^tracking]: [Python, Grafana, Prometheus, Docker](https://dev.to/thedevtimeline/setup-grafana-with-prometheus-for-python-projects-using-docker-4o5g)

[^gpt]: GPT: Generative Pre-trained Transformer
