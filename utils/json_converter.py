import json

def convert_to_label_studio(path_info, data, save_path=None):
    template = {
        "data": {"audio": path_info},
        "predictions": [
            {
                "model_version": 1.0,
                "score": 0.5,
                "result": []
            }
        ]
    }
    
    for idx, item in enumerate(data, start=1):
        converted_item = {
            "value": {
                "start": item["start"],
                "end": item["end"],
                "channel": 0,
                "labels": [item["type"]]
            },
            "id": f"PRED_{idx}",
            "from_name": "label",
            "to_name": "audio",
            "type": "labels"
        }
        template["predictions"][0]["result"].append(converted_item)

    if save_path:
        with open(save_path, 'w') as f:
            json.dump([template], f, ensure_ascii=False,indent=2)

    return template




if __name__ == "__main__":
    with open('.output/Sample1_mask.json', 'r') as f:
        data = json.load(f)
    
    template_data = convert_to_label_studio('YOUR PATH INFO' , data)
    
    with open('.output/converted_template.json', 'w') as f:
        json.dump([template_data], f, indent=2)

    print("save to converted_template.json")