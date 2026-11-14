"""LaBSE sentence embeddings (bitext-mining model) with an on-disk cache keyed by text hash."""
import hashlib, os
import numpy as np
import torch

_model = None
CACHE = "data/processed/labse_cache.npz"


def _load():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
        _model = SentenceTransformer("sentence-transformers/LaBSE", device=dev)
    return _model


def embed(texts, batch_size=64):
    keys = [hashlib.md5(t.encode("utf-8")).hexdigest() for t in texts]
    cache = dict(np.load(CACHE, allow_pickle=True)) if os.path.exists(CACHE) else {}
    todo = [i for i, k in enumerate(keys) if k not in cache]
    if todo:
        vecs = _load().encode([texts[i] for i in todo], batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)
        for i, v in zip(todo, vecs):
            cache[keys[i]] = v.astype(np.float32)
        np.savez(CACHE, **cache)
    return np.stack([cache[k] for k in keys])
