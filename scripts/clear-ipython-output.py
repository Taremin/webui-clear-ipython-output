import importlib.util
in_ipython = importlib.util.find_spec('IPython')
if in_ipython is not None:
    from IPython.display import clear_output

import modules.scripts as scripts
import gradio as gr
import os
import json

SavePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "settings.json"))
#SavePath = os.path.join(__file__, "..", "settings.json")

def load_settings():
    global settings
    
    try:
        with open(SavePath, mode="r") as f:
            settings = json.loads(f.read())
    except:
        settings = {}
    
    return settings
settings = load_settings()

def save_settings(args):
    def save_settings(*inputs):
        global settings
        
        if len(args) != len(inputs):
            raise ValueError("invalid parameter length")
        
        for index in range(len(inputs)):
            settings[args[index]["key"]] = inputs[index]
            
        with open(SavePath, "w") as f:
            json.dump(settings, f)
            
    return save_settings

def load_setting(key: str, default: any):
    global settings
    return lambda: settings.get(key, default)

class ClearOutput(scripts.Script):  
    def title(self):
        return self.__class__.__name__
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        save_targets = []
        
        with gr.Accordion(self.title(), open=False):
            with gr.Row():
                with gr.Column(min_width = 50, scale=1):
                    enable = gr.Checkbox(value=load_setting("enable", True), label="Enable")
                    save_targets.append({"key": "enable", "value": enable})
         
        for save_target in save_targets:
            save_target["value"].change(fn=save_settings(save_targets), inputs=[save_target["value"] for save_target in save_targets])

        return [enable]
    
    def process(self, p, enable, *args, **kwargs):
        if not enable:
            return
        
        if in_ipython is None:
            return
        
        print("clear output")
        clear_output(wait=False)
        
        
        
        
        
