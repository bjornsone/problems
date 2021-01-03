import enum
import math
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from level import vector_util_2d as v


class AngleMarker(enum.Enum):
    NONE = 0
    RIGHT_ANGLE = 1
    OTHER_ANGLE = 2


class SegmentImage:

    def __init__(self, dx=250, dy=200):
        self.dx = dx
        self.dy = dy
        self.margin_x = [20, 20]
        self.margin_y = [20, 20]
        self.points = None
        self.midpoints = None
        self.side_labels = None
        self.vertex_labels = None
        self.angle_labels = None
        self.label_directions = None
        self.vertex_directions = None
        self.angle_markers = None
        self.font_size = 20

        self.min_x = 0.0
        self.min_y = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0

    def add_points(self, points):
        self.points = points
        cnt = len(points)
        mps = []
        for i in range(cnt):
            i2 = (i + 1) % len(points)
            mpx = (points[i][0] + points[i2][0]) / 2
            mpy = (points[i][1] + points[i2][1]) / 2
            mps.append((mpx, mpy))
        self.midpoints = mps
        lds = []
        for i in range(cnt):
            i2 = (i + 1) % cnt
            d = points[i2][0] - points[i][0], points[i2][1] - points[i][1]
            lds.append(v.rotated_90(v.normed(d)))
        self.label_directions = lds
        vds = []
        for i in range(cnt):
            i0 = (i + cnt - 1) % cnt
            d = lds[i][0] + lds[i0][0], lds[i][1] + lds[i0][1]
            vds.append(v.normed(d))
        self.vertex_directions = vds

    def add_triangle(self, segment_lengths, point0=None):
        if not point0:
            point0 = (0, 0)
        assert len(segment_lengths) == 3
        l0, l1, l2 = segment_lengths
        point1 = (l0 + point0[0], point0[1])  # horizontal offset
        cos_a = (l1 * l1 - l0 * l0 - l2 * l2) / (2 * l0 * l2)
        point2 = point0[0] + l2 * cos_a, point0[1] - l2 * math.sqrt(1 - cos_a * cos_a)
        self.add_points([point0, point1, point2])

    def add_side_labels(self, side_labels):
        self.side_labels = side_labels

    def add_vertex_labels(self, vertex_labels):
        self.vertex_labels = vertex_labels

    def add_angle_labels(self, angle_labels):
        self.angle_labels = angle_labels

    def add_angle_markers(self, angle_markers):
        self.angle_markers = angle_markers

    def _set_scale(self, d, f):
        w_max, h_max = 0, 0
        for s in self.side_labels:
            if s:
                w, h = d.textsize(s, font=f)
                w_max = max(w_max, w)
                h_max = max(h_max, h)

        min_x = np.array([p[0] for p in self.points]).min()
        max_x = np.array([p[0] for p in self.points]).max()
        min_y = np.array([p[1] for p in self.points]).min()
        max_y = np.array([p[1] for p in self.points]).max()

        scale_x = (self.dx - (self.margin_x[0] + self.margin_x[1] + w_max*2)) / (max_x - min_x)
        scale_y = (self.dy - (self.margin_y[0] + self.margin_y[1] + h_max*2)) / (max_y - min_y)
        scale = min(scale_x, scale_y)
        self.scale_x = scale
        self.scale_y = scale

        self.min_x = min_x - (self.margin_x[0] + w_max) / self.scale_x
        self.min_y = min_y - (self.margin_y[0] + h_max) / self.scale_y

    def _rescale(self, p, include_offset=True):
        """Rescales a point based on the self.min_[xy] and self.scale_[xy]"""
        if include_offset:
            return np.array([(p[0] - self.min_x) * self.scale_x, (p[1] - self.min_y) * self.scale_y])
        else:
            return np.array([p[0] * self.scale_x, p[1] * self.scale_y])

    def add_right_triangle(self, a, b, c):
        self.add_triangle([a, b, c])
        self.add_angle_markers([AngleMarker.RIGHT_ANGLE, AngleMarker.NONE, AngleMarker.NONE])

    def _line(self, d, start, end, is_thin = False):
        width = 2 if is_thin else 4
        d.line((tuple(start.tolist()), tuple(end.tolist())), fill='black', width=width)

    def save(self, out_file):
        image = Image.new(mode="RGB", size=(self.dx, self.dy), color='white')
        d = ImageDraw.Draw(image)
        cnt = len(self.points)
        f = ImageFont.truetype("arial.ttf", self.font_size)
        self._set_scale(d, f)
        for i in range(cnt):
            i2 = (i + 1) % cnt
            i0 = (i + cnt -1) % cnt
            self._line(d, self._rescale(self.points[i]), self._rescale(self.points[i2]))
            s = self.side_labels[i]
            if s:
                text_size = np.array(d.textsize(s, font=f))
                text_projection = v.project(text_size, self.label_directions[i], .6)
                text_location = text_projection - text_size / 2 + self._rescale(self.midpoints[i])
                d.text(text_location, s, (0, 0, 0), font=f)
            s = self.angle_labels[i] if self.angle_labels else None
            if s:
                text_size = np.array(d.textsize(s, font=f))
                vd = self._rescale(self.vertex_directions[i], include_offset=False)
                text_projection = v.project(text_size, vd, -1.0)
                text_location = text_projection * 1.6 - text_size / 2 + self._rescale(self.points[i])
                d.text(text_location, s, (0, 0, 0), font=f)
            s = self.vertex_labels[i] if self.vertex_labels else None
            if s:
                text_size = np.array(d.textsize(s, font=f))
                vd = self._rescale(self.vertex_directions[i], include_offset=False)
                text_projection = v.project(text_size, vd, 1.0)
                # p_ic = self._rescale(self.points[i])  # in image coordinates
                # self._line(d, p_ic, p_ic+vd)  # draws a line for debugging purposes
                text_location = text_projection - text_size / 2 + self._rescale(self.points[i])
                d.text(text_location, s, (0, 0, 0), font=f)
            if self.angle_markers and self.angle_markers[i] == AngleMarker.RIGHT_ANGLE:
                size = self.font_size
                ld0, ld1 = self.label_directions[i], self.label_directions[i0]
                delta0, delta1 = v.normed(ld0) * size, v.normed(ld1) * size
                p_ic = self._rescale(self.points[i])  # in image coordinates
                self._line(d, p_ic-delta0, p_ic-delta0-delta1, is_thin=True)
                self._line(d, p_ic-delta1, p_ic-delta0-delta1, is_thin=True)
        image.save(out_file, "PNG")


if __name__ == '__main__':
    test = SegmentImage()
    test.add_right_triangle(12, 13, 5)
    test.add_side_labels(["x", "13", "5"])
    test.add_angle_labels(["\u03b8", "b", "c"])
    test.add_vertex_labels(["A", "B", "C"])
    test.save('test_image.png')
    exit()
