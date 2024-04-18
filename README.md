# Curator AI

This project is a modified version of the examples from [CrewAI](https://github.com/joaomdmoura/crewAI). This crew of AI agents is configured to research the latest AI and technology trends or advancements, then suggest projects and blog content that can be created for it. 

Another unique part of this example is that instead of using OpenAI GPT models, this uses Databricks' [DBRX](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-dbrx-new-standard-efficient-open-source-models) model, which is a cost-effective open source Mixture-of-Experts (MoE) model. I use the Pay-per-Token pricing for DBRX because it's simple, accessible, and cost-effective for such a project to be used very infrequently or adhoc; however, you can also swap out the model for another or use Model Serving to host provisioned models with more predictable performance. 

## Getting Started

To use this project, you must have Python 3.8+ and Poetry installed. Then you can install the project dependencies and run the crew with the following:  

Export the following environment variables:  
```shell
export OPENAI_API_KEY=NA
export OPENAI_API_BASE=https://your_workspace_url.cloud.databricks.com/serving-endpoints
export OPENAI_MODEL_NAME=databricks-dbrx-instruct
export SERPER_API_KEY=changeme # Get a key at https://serper.dev/
```

Then run:  

```shell
poetry install
poetry run curator-ai
```
