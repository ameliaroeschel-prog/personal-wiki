"""Thin wrapper around the local Gemma model (MLX). The only file that talks to the model.

Gemma does not read files or remember anything on its own: every call receives exactly
the messages the harness assembles here.
"""
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # never download anything at run time
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import time
import warnings

from . import config

warnings.filterwarnings("ignore")

_model = None
_processor = None


class ModelUnavailable(RuntimeError):
    pass


def load():
    """Load Gemma once per process (~10-20 s on an M1)."""
    global _model, _processor
    if _model is None:
        try:
            from mlx_vlm import load as mlx_load
        except ImportError as e:
            raise ModelUnavailable(
                "mlx-vlm is not installed. Run the CLI with ./wiki (uses ~/local-ai/venv)."
            ) from e
        print(f"[loading {config.MODEL_ID} locally...]", flush=True)
        try:
            _model, _processor = mlx_load(config.MODEL_ID)
        except Exception as e:
            raise ModelUnavailable(
                f"Could not load {config.MODEL_ID} from the local Hugging Face cache.\n"
                "Download it once while online:  "
                f"HF_HUB_OFFLINE=0 ~/local-ai/venv/bin/hf download {config.MODEL_ID}\n"
                f"Details: {e}"
            ) from e
    return _model, _processor


def generate(messages, max_tokens, temperature=0.2, stream=False):
    """Send a list of {role, content} messages to Gemma and return (text, stats)."""
    from mlx_vlm import stream_generate
    from mlx_vlm.prompt_utils import apply_chat_template

    model, processor = load()
    prompt = apply_chat_template(processor, model.config, messages)
    start = time.time()
    text, last = "", None
    for chunk in stream_generate(
        model, processor, prompt, max_tokens=max_tokens, temperature=temperature
    ):
        if stream:
            print(chunk.text, end="", flush=True)
        text += chunk.text
        last = chunk
    if stream:
        print()
    stats = {
        "seconds": round(time.time() - start, 2),
        "prompt_tokens": getattr(last, "prompt_tokens", None),
        "generation_tokens": getattr(last, "generation_tokens", None),
        "peak_memory_gb": round(getattr(last, "peak_memory", 0) or 0, 2),
    }
    return text.strip(), stats
