# Parameterized Argumentation-based Reasoning Tasks for Benchmarking Generative Language Models

This repository contains all the code and datasets to run the experiments presented in "Parameterized Argumentation-based Reasoning Tasks for Benchmarking Generative Language Models"; a paper accepted at the International Conference of AI & Law in 2025.

## Abstract:
Generative large language models as tools in the legal domain have the potential to improve the justice system. However, the reasoning behavior of current generative models is brittle and poorly understood, hence cannot be responsibly applied in the domains of law and evidence. In this paper, we introduce an approach for creating benchmarks that can be used to evaluate the reasoning capabilities of generative language models. These benchmarks are dynamically varied, scalable in their complexity, and have clear, unambiguous formal interpretations. In this study, we illustrate the approach on the basis of witness testimony, focusing on the underlying argument attack structure. We dynamically generate both linear and non-linear argument attack graphs of varying complexity and translate these into reasoning puzzles about witness testimony expressed in natural language. We show that state-of-the-art large language models often fail in these reasoning puzzles, already at low complexity. Obvious mistakes are made by the models, and their inconsistent performance indicates that their reasoning capabilities are brittle. Furthermore, at higher complexity, even state-of-the-art models specifically designed for reasoning make mistakes. We show the viability of using a parametrized benchmark with varying complexity to evaluate the reasoning capabilities of generative language models. As such, the findings contribute to a better understanding of the limitations of the reasoning capabilities of generative models, which is essential when designing responsible AI systems in the legal domain.

## Content:
- LinearGraphGenerator.py: Python file containing functions to generate prompts based on linear argument graphs.
- NonLinearGraphGenerator.py: Python file containing functions to generate prompts based on non-linear argument graphs.
- ModelFunctions.py: Python file containing helper functions for the experiment.
- personal_key.py: Python file that should contain the API keys for the commercial LLMs.

- 01_evaluate_models_linear.ipynb: The notebook to run the experiments with prompts based on linear argument graphs.
- 02_evaluate_models_nonlinear.ipynb: The notebook to run the experiments with prompts based on non-linear argument graphs, both shuffled and non-shuffled.

- ontologies/: Contains the list of names and statements.
- results/: Used to store the results of the experiment. This folder also contains the experimental results discussed in the paper. 
- static_benchmarks/: Used to store static benchmarks for experimental purposes.
