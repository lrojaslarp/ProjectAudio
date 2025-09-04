# Optional SSL embeddings (wav2vec2/HubERT) if local env has torch/torchaudio/transformers.
def ssl_embedding(x, sr, model_name_or_path="facebook/wav2vec2-base-960h", device="cpu"):
    try:
        import torch, numpy as np
        from transformers import Wav2Vec2Processor, Wav2Vec2Model
    except Exception:
        return None, "transformers/torch not available"
    try:
        import numpy as np
        import torch
        processor = Wav2Vec2Processor.from_pretrained(model_name_or_path, local_files_only=True)
        model = Wav2Vec2Model.from_pretrained(model_name_or_path, local_files_only=True).to(device)
        with torch.no_grad():
            inputs = processor(x, sampling_rate=sr, return_tensors="pt").to(device)
            hidden = model(**inputs).last_hidden_state  # [1, T, D]
            emb = hidden.mean(dim=1).cpu().numpy().flatten()
        return emb, None
    except Exception as e:
        return None, str(e)
