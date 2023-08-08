from src.mongo.MongoConnect import MongoConnect

class ModelConfig:
    
    def __init__(self, model_configurations):
        self.model_config = model_configurations

    # mutating model config, from mongodb
    def models(self, question, context):
        models = self.model_config
        prompt = "Answer the question based on the context below."
        for model in models:

            if("prompt" in model):
                prompt = model["prompt"]

            prompt = f"{prompt} \
                        Context: {context} \
                        Question: {question}"
            model["inputs"] = [prompt]
            model["prompt"] = prompt
            #del model["prompt"]
        return models