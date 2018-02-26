class GuaVertex extends GuaObject {
    // 表示顶点的类, 包含 GuaVector 和 GuaColor
    // 表示了一个坐标和一个颜色
    constructor(position, color, u, v) {
        super()
        this.position = position
        this.color = color
        this.u = u || ''
        this.v = v || ''
    }
    interpolate(other, factor) {
        let a = this
        let b = other
        let p = a.position.interpolate(b.position, factor)
        let c = a.color.interpolate(b.color, factor)
        let u = a.u + (b.u - a.u) * factor
        let v = a.v + (b.v - a.v) * factor
        return GuaVertex.new(p, c, u, v)
    }
}
