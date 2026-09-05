# WebGPU kernel projects

Sixteen small web pages that run real GPU maths in a browser tab, plus the research that chose them.

Every page is one self-contained HTML file. No npm, no bundler, no build step, no server-side code. Each page imports [`@huggingface/kernels`](https://huggingface.co/docs/kernels/index) from a CDN, calls a handful of the 200-plus WebGPU kernels that Hugging Face published on the Hub, and draws the result.

**Live site — <https://az9713.github.io/webgpu-projects/>**

Every page below runs in your browser with nothing to install. The sixteen demos are at <https://az9713.github.io/webgpu-projects/projects/>.

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

## The sixteen pages

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
| 11 | [Why the stable form of softmax exists](https://az9713.github.io/webgpu-projects/projects/11-stable-softmax.html) | Naive `exp(x) / Sum exp(x)` against the max-subtracted form. On this card the sum overflows at 88.2645 and `exp` at 88.7228; between the two every exponential is finite, the sum is not, and the naive panel returns eight zeros with no NaN raised, off by 0.63. The stable form stays within 5.9e-8 from -120 to 120. | 9 — `Div` `Exp` `IsInf` `IsNaN` `ReduceLogSumExp` `ReduceMax` `ReduceSum` `Softmax` `Sub` |
| 12 | [Seam carving — the photo shrinks and the subject does not](https://az9713.github.io/webgpu-projects/projects/12-seam-carving.html) | A Sobel energy map, then a dynamic program down the rows picks the lowest-energy connected path and removes it. After 77 seams the figure still spans 25 columns; a plain resize to the same width leaves it 17, which is exactly round(25 × 179/256). The traced seam matches the dynamic program's own total to 7.7e-8. 564 calls a seam, 0.22 seams/s — the row sweep is serial. | 8 — `Abs` `Add` `Concat` `Conv` `Gather` `ReduceMin` `ReduceSum` `Reshape` |
| 13 | [Convolution unmasked — im2col and one matrix multiply](https://az9713.github.io/webgpu-projects/projects/13-im2col-convolution.html) | Direct `Conv` against the im2col route: one `Gather` builds a 9×16384 column matrix, one `MatMul` does every multiply-add, and `Col2Im` folds it back. The two disagree by at most **1.192e-7** over 16384 pixels, mean 1.5e-8. That is exactly 2⁻²³, one float32 ulp near 1.0 — the same nine products summed in a different order. | 7 — `Abs` `Col2Im` `Conv` `Gather` `MatMul` `Reshape` `Sub` |
| 14 | [Real-time fluid you can stir with the mouse](https://az9713.github.io/webgpu-projects/projects/14-fluid-stir.html) | A Stam stable-fluids solver, 36.5 steps/s at 128². Before it animates it solves a known sine mode, where Jacobi must shrink the error by cos(πj/(N+1)) per sweep: after 20 sweeps it measures 0.9093321970, 0.0011022035 and 0.6161289335 against a theory of 0.9093321930, 0.0011022045 and 0.6161289248. Jacobi kills the middle frequency and barely touches the smoothest or roughest. Set sweeps to 0 and retained divergence is exactly 1. | 8 — `Add` `Concat` `Conv` `Exp` `GridSample` `Mul` `Sub` `Transpose` |
| 15 | [The scan, and everything it builds](https://az9713.github.io/webgpu-projects/projects/15-the-scan.html) | Stream compaction, run-length encoding, a histogram and a variable-size allocator, all from one prefix sum. Every result is checked against plain JavaScript: the histogram's 16 bins sum to 4096 and agree bin by bin, compaction 13/13, run-length 15/15, allocation 57/57. `ScatterND` forces one CPU round trip per scatter, because it needs int64 indices and no kernel here makes int64. | 5 — `CumSum` `Equal` `Range` `ScatterND` `Where` |
| 16 | [The activation zoo, all twenty of them](https://az9713.github.io/webgpu-projects/projects/16-activation-zoo.html) | All 20 activations plotted from one shared input, including the `com.microsoft` pair. Softplus(0) returns 0.6931472 (ln 2), Sigmoid and HardSigmoid 0.5, the other 17 zero. Measured slopes at the origin: Sigmoid 0.24995, Tanh 0.99917, Erf 1.12744. Softsign reads 0.95238, which is 1/1.05 exactly — the step size showing through, not a bug. FastGelu differs from Gelu by 4.7e-4, QuickGelu by 0.0203. | 20 — `Celu` `Elu` `Erf` `FastGelu` `Gelu` `HardSigmoid` `HardSwish` `LeakyRelu` `Mish` `PRelu` `QuickGelu` `Relu` `Selu` `Shrink` `Sigmoid` `Softplus` `Softsign` `Swish` `Tanh` `ThresholdedRelu` |


Across the sixteen pages that is **66 distinct kernels of the 207**. A handful do most of the work — `Sub` on ten pages, `Add` on eight, `Mul` and `MatMul` on seven, `Abs`, `Concat`, `ReduceMean` and `Transpose` on five — while 39 appear on exactly one page. Page 16 alone brought 18 new kernels, all of them activations. The column counts kernels *loaded*, not calls made: page 10 loads 18 and issues 46 calls a step.

## The research behind the choice

Three documents sit next to the pages. They came first; the sixteen pages are the result.

- **[`webgpu-kernels-report.html`](https://az9713.github.io/webgpu-projects/webgpu-kernels-report.html)** — the research report. Thirteen sections on how the library works, how kernels are packaged on the Hub, and what the API costs you. Sections 1–9 and 12–13 come from sources. **Section 10 is measured on one laptop, not researched**, and Section 11 documents the harness that measured it.
- **[`webgpu-kernel-projects.html`](https://az9713.github.io/webgpu-projects/webgpu-kernel-projects.html)** — the catalogue. 121 project ideas in 18 categories, each with the exact kernel names it needs and an honest ceiling on what it can reach. Every kernel name in the file was checked against the Hub API list: 0 invalid, 179 of the 207 kernels named by at least one project. A sortable ranking table (`#scores`) scores all 121 on seven axes. The sixteen pages here come from the top of that ranking. Project 104 was the one swapped out for 115 when the pages were first built; it is now page 11.
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

Facts learned the hard way while building the sixteen pages.

- Argument names are the manifest's `args` keys, lower case. `MatMul` is `a, b → y`. `Add`, `Sub` and `Mul` are `a, b → c`. `Gather` is `data, indices → output`. `Transpose` is `x → y`.
- Attributes go in `options.attrs`: `perm`, `axes`, `to`, `direction`, `reduction`, `inverse`.
- Always pass `attrs: { axes: [...] }` to a reduction, and always pass an `outputs` shape. A reduction with no `axes` may have no matching variant, depending on the shape.
- `Transpose`, `DFT`, `QuantizeLinear`, `Split` and the `Reduce` family all need an explicit `outputs: { <name>: { shape, dtype } }`.
- The `DFT` fast path runs only along the default axis, at a power-of-2 length, with length × 16 within workgroup storage — so N ≤ 1024. A 2-D transform is `DFT`, `Transpose [1,0,2]`, `DFT`, `Transpose`.
- Kernel artifacts live on the **`v1` branch** under `build/webgpu/`, not on `main`, and the URL needs a `/kernels/` path segment.
- Chrome picks one GPU at startup. A per-app GPU setting in Windows plus a full browser restart is the only way to move a page to a different adapter.
- `requestAnimationFrame` pauses in a hidden tab. The animated pages use `setTimeout(…, 0)` loops instead.
- **Argument names are not consistent, so read the manifest rather than guessing.** Most activations take `x`, but `Softsign` takes `input`, and `FastGelu` and `QuickGelu` take a capital `X`. `PRelu` takes `x, slope`. `Col2Im` is `input, image_shape, block_shape → output`.
- **`CumSum`'s `axis` is a plain JavaScript number in the args object** — not an attribute and not a tensor. The manifest lists only `x` as an input and only `exclusive` and `reverse` as attributes, which is misleading: omit `axis` and the call fails with *missing required arg axis*; pass it as a tensor and it fails with *not a tensor arg of this op*. Verified on a [2,3] input: `axis: 0` gives [1,2,3,11,22,33], `axis: 1` gives [1,3,6,10,30,60], and `exclusive: 1` gives [0,1,3,0,10,30].
- **`Range` wants rank-0 scalars**, shape `[]` and not `[1]`, for `start`, `limit` and `delta`. It returns `output`.
- Multi-channel `Conv` works: a `[2,2,3,3]` weight over a two-channel input runs, as does `GridSample` on two channels. `Gather` accepts a rank-2 index tensor — `[9, 16384]` against rank-1 data is fine.
- **The Hub rate-limits at 3000 requests per 300 seconds** for anonymous clients, published in every response as `RateLimit-Policy: "fixed window";"resolvers";q=3000;w=300`. One kernel repo holds 6 files, and a page loading 20 kernels costs about 82 requests, so roughly 2.7% of the window. Concurrency itself is not limited — 24 parallel requests all succeed — but a burst can still return 429, and a `/resolve/` fetch costs two requests because the redirect counts.

## Honesty about the numbers

Every measurement here is one run on one laptop with one GPU. Nothing is averaged over machines and nothing is compared against a native baseline. The scores in the catalogue's ranking are a single consistent judgement, not a measurement — they were assigned before anything was built. Treat all of it as a starting point, not a benchmark.

## Credit

The kernels, the library and the launch video are Hugging Face's work. This repo is an independent exploration of them, and is not affiliated with or endorsed by Hugging Face.
