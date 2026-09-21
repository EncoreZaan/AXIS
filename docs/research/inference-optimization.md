# Inference Optimization & Prospective Acceleration Research

> **Status:** PROSPECTIVE RESEARCH & INVESTIGATION ONLY  
> **Rule:** No acceleration claim or throughput gain is considered valid until empirically benchmarked on physical hardware with reproducible scripts.

---

## 1. Context and Objective

Spatial and architectural reasoning workloads in AXIS combine distinct computational profiles:
1. **Geometric Coordinate Regressors & Graph Neural Networks:** Ultra-fast, compute-light, latency-sensitive ($\le 10$ ms).
2. **Vision-Language Backbones (VLM / M-RoPE 2D/3D):** Memory-bound, activation-heavy, requiring substantial KV-cache and vision token processing.
3. **BIM / IFC STEP Interpreters:** I/O and CPU parsing bound, transforming topological entities into tensor scene graphs.

To enable efficient deployment—both on resource-constrained local workstations (e.g. 8 GB RTX 4060 Ti) and production inference clusters—several optimization vectors are currently under investigation.

---

## 2. Research Vectors Under Investigation

### 2.1. Quantization Techniques
- **4-bit NormalFloat (NF4):** Validated in dry-run and proof-of-concept stages with `bitsandbytes` to reduce model memory footprint from ~15 GB down to ~5.8 GB VRAM.
- **AWQ / GPTQ / SmoothQuant:** Under consideration for downstream post-training quantization on language backbones once full-scale fine-tuning commences.
- **FP8 (Float8 E4M3/E5M2):** Prospective evaluation for Ada Lovelace and Hopper architectures natively supporting FP8 tensor cores.

### 2.2. Custom Kernels & Memory Optimization
- **Fused Operators:** Custom Triton / CUDA kernels for Euclidean distance matrices and 3D spatial clearance bounding box intersections.
- **Gradient & Activation Checkpointing:** Crucial for micro-batching on 8 GB VRAM, trading ~20% compute for $> 50\%$ activation memory reduction.
- **Paged Attention & KV Cache Management:** Investigating vLLM / SGLang integration to avoid KV cache fragmentation during long multi-turn design critiques.

### 2.3. Dynamic Batching & Spatial Caching
- **Graph Embedding Caching:** Caching invariant scene graph embeddings for static architectural components (e.g., structural columns, load-bearing walls) across multiple interactive queries.
- **Dynamic Speculative Decoding:** Utilizing lightweight geometric heads (`SpatialRelationMLP`) as draft models to verify spatial constraints ahead of full VLM textual generation.

---

## 3. DSpark Investigation

### Status: Prospective / Exploratory Track
**DSpark** is tracked on the AXIS research roadmap as an **exploratory acceleration technology to evaluate**.

> [!WARNING]
> **No Empirical Claims at this Stage:**  
> DSpark is strictly an investigation item. It has **NOT** yet been integrated into the current AXIS codebase, and **NO** performance boost, latency reduction, or memory saving is claimed or verified.

### Scope of Future Evaluation:
- Analyze compatibility with PyTorch graph execution and custom architectural tensor representations.
- Benchmark throughput and VRAM efficiency against standard PyTorch 2.x `torch.compile(mode="reduce-overhead")`.
- Publish formal before/after benchmark results in `docs/experiments/` before making any adoption decisions.
