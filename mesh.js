class YuanMesh extends YuanObject {
    // 表示三维物体的类
    constructor() {
        super()
        this.position = YuanVector.new(0, 0, 0)
        this.rotation = YuanVector.new(0, 0, 0)
        this.scale = YuanVector.new(1, 1, 1)
        this.vertices = null
        this.indices = null
    }
    // 返回一个正方体
    static cube() {
        // 8 points
        let points = [
            -1, 1,  -1,     // 0
            1,  1,  -1,     // 1
            -1, -1, -1,     // 2
            1,  -1, -1,     // 3
            -1, 1,  1,      // 4
            1,  1,  1,      // 5
            -1, -1, 1,      // 6
            1,  -1, 1,      // 7
        ]

        let vertices = []
        let colors = [YuanColor.red(),YuanColor.blue(),YuanColor.green(),YuanColor.white(),YuanColor.new(234,210,244,255)]
        for (let i = 0; i < points.length; i += 3) {
            let v = YuanVector.new(points[i], points[i+1], points[i+2])
            // let c = YuanColor.randomColor()
            let index = i % 5
            let c = colors[index]
            vertices.push(YuanVertex.new(v, c))
        }

        // 12 triangles * 3 vertices each = 36 vertex indices
        let indices = [
            // 12
            [0, 1, 2],
            [1, 3, 2],
            [1, 7, 3],
            [1, 5, 7],
            [5, 6, 7],
            [5, 4, 6],
            [4, 0, 6],
            [0, 2, 6],
            [0, 4, 5],
            [5, 1, 0],
            [2, 3, 7],
            [2, 7, 6],
        ]
        let m = this.new()
        m.vertices = vertices
        m.indices = indices
        return m
    }
    static imagepixels() {
        this.pixels = []
        let pixels = yuanimage.split('\n').slice(4)
        for (let i = 0; i < pixels.length; i++) {
            let s = pixels[i]
            let pixel = s.split(' ')
            let ps = []
            for (let j = 0; j < pixel.length; j++) {
                let p = parseInt(pixel[j])
                let r = p >>> 24
                let g = (((p >>> 16) * 2**16) - (r * 2**24))>>>16
                let b = (((p >>> 8) * 2**8) - (r * 2**24) - (g * 2**16))>>>8
                let a = p - (r * 2**24) - (g * 2**16) - (b * 2**8)
                ps.push([r,g,b,a])
            }
            this.pixels.push(ps)
        }
    }

    static fromYuan3d(yuan3dString) {
        let arrs = yuan3dString.split('\n')
        let vectors = arrs.slice(4,4046)
        let indices = arrs.slice(4046)
        for (var i = 0; i < vectors.length; i++) {
            let v = vectors[i].split(' ')
            for (var j = 0; j < v.length; j++) {
                v[j] = parseFloat(v[j])
            }
            vectors[i] = v
        }
        for (var i = 0; i < indices.length; i++) {
            let t = indices[i].split(' ')
            for (var j = 0; j < t.length; j++) {
                t[j] = parseFloat(t[j])
            }
            indices[i] = t
        }
        let vertices = []
        for (var i = 0; i < vectors.length; i++) {
            let vector = vectors[i]
            let v = YuanVector.new(vector[0], vector[1], vector[2])
            let vu = vector[6]
            let vv = vector[7]
            let x = Math.floor(vu * 255)
            let y = Math.floor(vv * 255)
            let [r,g,b,a] = this.pixels[y][x]
            let c = YuanColor.new(r,g,b,a)
            vertices.push(YuanVertex.new(v, c, vu, vv))
        }
        let illidan = this.new()
        illidan.indices = indices
        illidan.vertices = vertices
        return illidan
    }
}
