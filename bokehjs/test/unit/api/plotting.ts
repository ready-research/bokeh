import {expect} from "assertions"

import {figure} from "@bokehjs/api/plotting"
import {LinearAxis} from "@bokehjs/models"

describe("in api/plotting module", () => {
  describe("figure()", () => {
    it("should support axis property proxying", () => {
      const p = figure({x_axis_label: "X0", y_axis_label: "Y0"})

      expect(p.xaxes.length).to.be.equal(1)
      expect(p.yaxes.length).to.be.equal(1)
      expect(p.axes.length).to.be.equal(2)

      expect(p.xaxes.map((axis) => axis.axis_label)).to.be.equal(["X0"])
      expect(p.yaxes.map((axis) => axis.axis_label)).to.be.equal(["Y0"])

      p.add_layout(new LinearAxis(), "left")
      p.add_layout(new LinearAxis(), "right")

      p.add_layout(new LinearAxis(), "above")
      p.add_layout(new LinearAxis(), "below")

      expect(p.xaxes.length).to.be.equal(3)
      expect(p.yaxes.length).to.be.equal(3)
      expect(p.axes.length).to.be.equal(6)

      p.xaxes.forEach((axis) => axis.axis_label = "X1")
      p.yaxes.forEach((axis) => axis.axis_label = "Y1")

      expect(p.xaxes.map((axis) => axis.axis_label)).to.be.equal(["X1", "X1", "X1"])
      expect(p.yaxes.map((axis) => axis.axis_label)).to.be.equal(["Y1", "Y1", "Y1"])

      p.xaxis.each((axis) => axis.axis_label = "X2")
      p.yaxis.each((axis) => axis.axis_label = "Y2")

      expect(p.xaxes.map((axis) => axis.axis_label)).to.be.equal(["X2", "X2", "X2"])
      expect(p.yaxes.map((axis) => axis.axis_label)).to.be.equal(["Y2", "Y2", "Y2"])

      p.xaxis.axis_label = "X3"
      p.yaxis.axis_label = "Y3"

      expect(p.xaxes.map((axis) => axis.axis_label)).to.be.equal(["X3", "X3", "X3"])
      expect(p.yaxes.map((axis) => axis.axis_label)).to.be.equal(["Y3", "Y3", "Y3"])

      p.add_layout(new LinearAxis(), "left")
      p.add_layout(new LinearAxis(), "right")

      p.add_layout(new LinearAxis(), "above")
      p.add_layout(new LinearAxis(), "below")

      p.xaxis.axis_label = "X4"
      p.yaxis.axis_label = "Y4"

      expect(p.xaxes.map((axis) => axis.axis_label)).to.be.equal(["X4", "X4", "X4", "X4", "X4"])
      expect(p.yaxes.map((axis) => axis.axis_label)).to.be.equal(["Y4", "Y4", "Y4", "Y4", "Y4"])

      // TODO: this should be disallowed on the type level
      expect(() => p.xaxis.axis_label).to.throw()
      expect(() => p.yaxis.axis_label).to.throw()
    })

    it("should throw if multiple legend_* attributes are provided", () => {
      expect(() => figure().circle(0, 0, {legend_label: "circle", legend_field: "circle"})).to.throw()
    })
  })
})
