# WebGPU kernel projects

Ten small web pages that run real GPU maths in a browser tab, plus the research that chose them.

Every page is one self-contained HTML file. No npm, no bundler, no build step, no server-side code. Each page imports [`@huggingface/kernels`](https://huggingface.co/docs/kernels/index) from a CDN, calls a handful of the 200-plus WebGPU kernels that Hugging Face published on the Hub, and draws the result.

**Live site — <https://az9713.github.io/webgpu-projects/>**

Every page below runs in your browser with nothing to install. The ten demos are at <https://az9713.github.io/webgpu-projects/projects/>.

## Where this came from

Hugging Face shipped more than 200 WebGPU kernels for browser AI, all open source on the Hub, together with a library that loads and runs them. The launch video is the origin of this whole repo:

- **Video — [Hugging Face: 200+ WebGPU kernels for browser AI](https://www.youtube.com/watch?v=y9xup6XEP2o)**
- Blog post — <https://huggingface.co/blog/webgpu-kernels> ([source](https://github.com/huggingface/blog/blob/main/webgpu-kernels.md))
- The kernels on the Hub — <https://huggingface.co/webgpu-kernels>
- Library docs — <https://huggingface.co/docs/kernels/index>

The video makes one claim worth testing: an ONNX operation is a mathematical description, a kernel is its implementation on one piece of hardware, and the library hides all the JavaScript-to-GPU glue. That is true, and it means a browser tab can now run numerical work that used to need Python. This repo is an attempt to find out what that is actually good for.

## Running it locally

The live site above needs no setup. To run from a clone instead, a local server is required. Opening a page with `file://` fails, because the CDN module import is blocked from that origin. `localhost` counts as a secure context, so WebGPU works there with no certificate.

```
git clone https://github.com/az9713/webgpu-projects
cd webgpu-projects
python -m http.server 8791
```

Then open <http://localhost:8791/projects/>.

You need a browser with WebGPU: Chrome or Edge 113 and later, or Safari 26 and later. The index page names the GPU adapter it found, and says so in red if it found none.

## The ten pages

Every page carries a **The science** section under the demo: the governing equation or algorithm, why it is correct, and a number you can check against the page while it runs.

Each result below was measured once, on an RTX 3050 laptop GPU, in Chrome. Read every number as plus or minus 10%. Every page also writes its numbers to `window.__result` and its state to `window.__status` and `window.__error`, so a script can check it without a human watching.

| # | Page | What it does, and what it measured | Kernels loaded |
|---|---|---|---|
| 01 | [Quantum wavepacket tunnelling](https://az9713.github.io/webgpu-projects/projects/01-quantum-wavepacket.html) | Split-step Schrödinger solver on a 256² grid, 17 kernel calls a step, 109 steps/s. Total probability holds at 1.0000 until the edges absorb it. A barrier of 0.6 against an energy of 0.405 lets 2.3% through, which matches exp(−2κa). | 9 — `Add` `Concat` `Cos` `DFT` `Gather` `Mul` `Neg` `Sin` `Transpose` |
| 02 | [An untrained network as a painting machine](https://az9713.github.io/webgpu-projects/projects/02-untrained-painting.html) | Pixel coordinates go into a small network with random weights that nobody trained; the three outputs are read as red, green and blue. 512² in about 380 ms, 1024² in about 620 ms, over 21 calls and one readback. | 5 — `Add` `MatMul` `Sigmoid` `Sin` `Tanh` |
| 03 | [Quantisation error microscope](https://az9713.github.io/webgpu-projects/projects/03-quant-microscope.html) | Max error 0.035 at int8, 0.63 at 4-bit, 4.05 at 2-bit with a single scale. Per-row scales are selectable. The 4-bit and 2-bit paths are simulated inside int8; the page says so. | 6 — `Abs` `DequantizeLinear` `QuantizeLinear` `ReduceMax` `ReduceMean` `Sub` |
| 04 | [Poison the training set with a click](https://az9713.github.io/webgpu-projects/projects/04-poison-training.html) | Logistic regression trained live, 8 calls a step, about 96 steps/s. Ten poisoned points tilt the decision line and halve the weights, while clean accuracy still sits near 98%. | 6 — `Abs` `MatMul` `Mul` `ReduceMean` `Sigmoid` `Sub` |
| 05 | [The cost of coming back to JavaScript](https://az9713.github.io/webgpu-projects/projects/05-readback-cost.html) | The same eight-call chain, run two ways. Keeping buffers on the card with `{ output: "gpu" }` is 3.0 to 4.6× faster at N ≥ 256. | 3 — `Add` `MatMul` `Mul` |
| 06 | [Train a digit classifier, then draw a digit](https://az9713.github.io/webgpu-projects/projects/06-mnist-train.html) | Fetches the tfjs MNIST sprite (10.7 MB). 784→64→10, batch 128, learning rate 0.3: 94.8% test accuracy after about 8 epochs, at 80–92 steps/s. Then you draw on a pad and it classifies the stroke. | 13 — `Add` `Greater` `Log` `MatMul` `Mul` `Neg` `ReduceMean` `ReduceSum` `Relu` `Softmax` `Sub` `Transpose` `Where` |
| 07 | [Two moons, gradients written by hand](https://az9713.github.io/webgpu-projects/projects/07-two-moons.html) | 2→16→1, 26 calls a step, about 100 steps/s, 99.5% at 630 steps. The ReLU gradient is a `Greater` and a `Where` — there is no autograd here. | 12 — `Abs` `Add` `Greater` `MatMul` `Mul` `ReduceMean` `ReduceSum` `Relu` `Sigmoid` `Sub` `Transpose` `Where` |
| 08 | [Principal components without a decomposition kernel](https://az9713.github.io/webgpu-projects/projects/08-pca-power.html) | Power iteration, because the 207 kernels contain no eigensolver. 27 iterations at an eigenvalue gap of 2.0, 88 iterations at a gap of 1.1. Residual \|Cv − λv\| ≈ 1e-5. | 5 — `Gemm` `LpNormalization` `MatMul` `ReduceMean` `Sub` |
| 09 | [Take a floating point number apart](https://az9713.github.io/webgpu-projects/projects/09-float-bits.html) | `BitCast`, `BitShift` and `BitwiseAnd` split sign, exponent and mantissa. `exp(x)` overflows at x ≥ 88.73, which is ln(3.403×10³⁸) = 88.7228. Dividing 10⁻³⁸ by 10⁵ gives 9.95×10⁻⁴⁴, a true subnormal, and this GPU returns exactly zero for it — it flushes subnormals. | 9 — `BitCast` `BitShift` `BitwiseAnd` `Concat` `Div` `Exp` `IsInf` `IsNaN` `Sub` |
| 10 | [Slime mould: agents that build networks](https://az9713.github.io/webgpu-projects/projects/10-slime-mould.html) | 250k Physarum agents on a 512² trail map, 46 calls a step, 44 steps/s. A web forms by about step 140, then coarsens into thick veins. | 18 — `Add` `And` `Cast` `Concat` `Conv` `Cos` `Floor` `Greater` `GridSample` `Mod` `Mul` `Reshape` `ScatterElements` `Sin` `Split` `Sub` `Transpose` `Where` |


Across the ten pages that is **42 distinct kernels of the 207**. Six do most of the work — `Sub` on seven pages, `Mul`, `Add` and `MatMul` on six, `ReduceMean` on five, `Transpose` on four — while 26 appear on exactly one page. The column counts kernels *loaded*, not calls made: page 10 loads 18 and issues 46 calls a step.

## The research behind the choice

Three documents sit next to the pages. They came first; the ten pages are the result.

- **[`webgpu-kernels-report.html`](https://az9713.github.io/webgpu-projects/webgpu-kernels-report.html)** — the research report. Thirteen sections on how the library works, how kernels are packaged on the Hub, and what the API costs you. Sections 1–9 and 12–13 come from sources. **Section 10 is measured on one laptop, not researched**, and Section 11 documents the harness that measured it.
- **[`webgpu-kernel-projects.html`](https://az9713.github.io/webgpu-projects/webgpu-kernel-projects.html)** — the catalogue. 121 project ideas in 18 categories, each with the exact kernel names it needs and an honest ceiling on what it can reach. Every kernel name in the file was checked against the Hub API list: 0 invalid, 179 of the 207 kernels named by at least one project. A sortable ranking table (`#scores`) scores all 121 on seven axes. The ten pages here are the top ten of that ranking, with one swap.
- **[`bench.html`](https://az9713.github.io/webgpu-projects/bench.html)** — the benchmark harness for Section 10. One file, commented, run twice, reproducing its numbers within about 10%.

`scratch/` holds the working files: the raw 121-project notes, the scoring script that produced the ranking, and the twenty-line table sort.

## What the kernels cannot do

Four absences are confirmed, and they shape every project here.

- **No random number generator.** Noise must be uploaded from JavaScript.
- **No sort.** Anything needing an ordering does it on the CPU.
- **No matrix inverse and no decomposition.** That is why project 08 uses power iteration.
- **No subgroup matrix support** on this hardware (`subgroup-matrix: false`).

A fifth trap: `ScatterND` wants int64 indices, and no kernel on the card can produce int64. Use `ScatterElements`, which takes int32 and has `reduction: "add"`.

## Notes for anyone building on this

Facts learned the hard way while building the ten pages.

- Argument names are the manifest's `args` keys, lower case. `MatMul` is `a, b → y`. `Add`, `Sub` and `Mul` are `a, b → c`. `Gather` is `data, indices → output`. `Transpose` is `x → y`.
- Attributes go in `options.attrs`: `perm`, `axes`, `to`, `direction`, `reduction`, `inverse`.
- Always pass `attrs: { axes: [...] }` to a reduction, and always pass an `outputs` shape. A reduction with no `axes` may have no matching variant, depending on the shape.
- `Transpose`, `DFT`, `QuantizeLinear`, `Split` and the `Reduce` family all need an explicit `outputs: { <name>: { shape, dtype } }`.
- The `DFT` fast path runs only along the default axis, at a power-of-2 length, with length × 16 within workgroup storage — so N ≤ 1024. A 2-D transform is `DFT`, `Transpose [1,0,2]`, `DFT`, `Transpose`.
- Kernel artifacts live on the **`v1` branch** under `build/webgpu/`, not on `main`, and the URL needs a `/kernels/` path segment.
- Chrome picks one GPU at startup. A per-app GPU setting in Windows plus a full browser restart is the only way to move a page to a different adapter.
- `requestAnimationFrame` pauses in a hidden tab. The animated pages use `setTimeout(…, 0)` loops instead.

## Honesty about the numbers

Every measurement here is one run on one laptop with one GPU. Nothing is averaged over machines and nothing is compared against a native baseline. The scores in the catalogue's ranking are a single consistent judgement, not a measurement — they were assigned before anything was built. Treat all of it as a starting point, not a benchmark.

## Credit

The kernels, the library and the launch video are Hugging Face's work. This repo is an independent exploration of them, and is not affiliated with or endorsed by Hugging Face.
