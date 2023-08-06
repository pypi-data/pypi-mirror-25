import unittest

import ModernGL

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_glo(self):
        glo = self.ctx.default_framebuffer.glo
        self.assertEqual(glo, 0)

    def test_viewport(self):
        x, y, width, height = self.ctx.default_framebuffer.viewport
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertNotEqual(width, 0)
        self.assertNotEqual(height, 0)

    def test_size(self):
        width, height = self.ctx.default_framebuffer.size
        self.assertNotEqual(width, 0)
        self.assertNotEqual(height, 0)

    def test_having_color_attachments(self):
        with self.assertRaisesRegex(ModernGL.Error, 'attachment'):
            self.ctx.default_framebuffer.color_attachments

    def test_having_depth_attachment(self):
        with self.assertRaisesRegex(ModernGL.Error, 'attachment'):
            self.ctx.default_framebuffer.depth_attachment


if __name__ == '__main__':
    unittest.main()
