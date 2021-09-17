import {display, column} from "./_util"

import {figure} from "@bokehjs/api/plotting"
import {Spectral} from "@bokehjs/api/palettes"
import {dark_minimal} from "@bokehjs/api/themes"
import {Parser} from "@bokehjs/api/parser"
import {TeX, FixedTicker} from "@bokehjs/models"
import {Div} from "@bokehjs/models/widgets"
import {NDArray} from "@bokehjs/core/util/ndarray"
import {enumerate} from "@bokehjs/core/util/iterator"

const r = String.raw

function tex(s: TemplateStringsArray, ...subs: unknown[]): TeX {
  return new TeX({text: r(s, ...subs)})
}

function f(s: TemplateStringsArray, ...subs: (number | NDArray)[]): NDArray {
  const ast = new Parser("").parse()
  return ast.eval()
}

namespace np {
  export declare function arange(start: number, end: number, step: number): NDArray
  export declare function linspace(start: number, end: number, step: number): NDArray
  export declare function histogram(array: ArrayLike<number>, options?: {density: boolean, bins: number | ArrayLike<number>}): [NDArray, NDArray]
  export declare function mean(array: ArrayLike<number>): NDArray
  export declare function std(array: ArrayLike<number>): NDArray
  export declare function exp<T extends number | NDArray>(x: T): T
  export declare const pi: number

  export namespace random {
    export declare class RandomGenerator {
      normal(loc: number/* = 0.0*/, scale: number/* = 1.0*/, size?: number): NDArray
    }
    export declare function default_rng(seed: number): RandomGenerator
  }
}

describe("Examples", () => {
  it("should support BlackbodyRadiation", async () => {
    const p = figure({
      width: 700, height: 500,
      toolbar_location: null,
      title: "Black body spectral radiance as a function of frequency",
    })

    function spectral_radiance(nu: NDArray, T: NDArray | number): NDArray {
      const h = 6.626e-34   // Planck constant (Js)
      const k = 1.3806e-23  // Boltzman constant (J/K)
      const c = 2.9979e8    // Speed of light in vacuum (m/s)
      return f`(${2*h}*${nu}**3/${c**2}) / (np.exp(${h}*${nu}/${k}*${T}) - 1.0)`
    }

    const Ts = np.arange(2000, 6001, 500)  // Temperature (K)
    const palette = Spectral.Spectral8
    const nu = np.linspace(0.1, 1e15, 500) // Frequency (1/s)

    for (const [T, i] of enumerate(Ts)) {
      const B_nu = spectral_radiance(nu, T)
      p.line(f`${nu}/1e15`, f`${B_nu}/1e-9`, {
        line_width: 2,
        legend_label: `T = ${T} K`,
        line_color: palette[i],
      })
    }
    p.legend.items.reverse()

    // Peak radiance line
    const Tpr = np.linspace(1900, 6101, 50)
    const peak_freqs = f`${Tpr}*5.879e10`
    const peak_radiance = spectral_radiance(peak_freqs, Tpr)
    p.line(f`${peak_freqs}/1e15`, f`${peak_radiance}/1e-9`, {
      line_color: "silver", line_dash: "dashed", line_width: 2,
      legend_label: "Peak radiance",
    })

    curdoc().theme = dark_minimal
    p.y_range.start = 0
    p.xaxis.axis_label = tex`\color{white} \nu \:(10^{15} s^{-1})`
    p.yaxis.axis_label = tex`\color{white} B_\nu(\nu, T) \quad(10^{-9} J s m^{-3})`

    const div = new Div({text: r`
    A plot of the spectral radiance, defined as a function of the frequency $$\nu$$, is given by the formula
    <p \>
    $$
    \qquad B_\nu(\nu, T) = \frac{2h\nu^3}{c^2} \frac{1}{\exp(h\nu/kT)-1}\ .
    $$
    `})

    await display(column([p, div]))
  })

  it("should support NormalDistribution", async () => {
    const p = figure({
      width: 670, height: 400,
      toolbar_location: null,
      title: "Normal (Gaussian) Distribution",
    })

    const n = 1000
    const rng = np.random.default_rng(825914)
    const x = rng.normal(4.7, 12.3, n)

    // Scale random data so that it has mean of 0 and standard deviation of 1
    const xbar = np.mean(x)
    const sigma = np.std(x)
    const scaled = f`(${x} - ${xbar}) / ${sigma}`

    // Histogram
    const bins = np.linspace(-3, 3, 40)
    const [hist, edges] = np.histogram(scaled, {density: true, bins})
    p.quad({
      top: hist, bottom: 0, left: f`${edges}[:-1]`, right: f`${edges}[1:]`,
      fill_color: "skyblue", line_color: "white",
      legend_label: `${n} random samples`,
    })

    // Probability density function
    const x_pdf = np.linspace(-3.0, 3.0, 100)
    const pdf = f`np.exp(-0.5*${x_pdf}**2) / np.sqrt(2.0*${np.pi})`
    p.line(x_pdf, pdf, {
      line_width: 2, line_color: "navy",
      legend_label: "Probability Density Function",
    })

    p.y_range.start = 0
    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "PDF(x)"

    p.xaxis.ticker = new FixedTicker({ticks: [-3, -2, -1, 0, 1, 2, 3]})
    p.xaxis.major_label_overrides = {
      "-3": tex`\overline{x} - 3\sigma`,
      "-2": tex`\overline{x} - 2\sigma`,
      "-1": tex`\overline{x} - \sigma`,
      0: tex`\overline{x}`,
      1: tex`\overline{x} + \sigma`,
      2: tex`\overline{x} + 2\sigma`,
      3: tex`\overline{x} + 3\sigma`,
    }

    p.yaxis.ticker = new FixedTicker({ticks: [0, 0.1, 0.2, 0.3, 0.4]})
    p.yaxis.major_label_overrides = {
      0: tex`0`,
      0.1: tex`0.1/\sigma`,
      0.2: tex`0.2/\sigma`,
      0.3: tex`0.3/\sigma`,
      0.4: tex`0.4/\sigma`,
    }

    const div = new Div({text: r`
      A histogram of a samples from a Normal (Gaussian) distribution, together with
      the ideal probability density function, given by the equation:
      <p />
      $$
      \qquad PDF(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left[-\frac{1}{2}
      \left(\frac{x-\overline{x}}{\sigma}\right)^2 \right]
      $$
    `})

    await display(column([p, div]))
  })
})
