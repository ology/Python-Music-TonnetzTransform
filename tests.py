import sys
sys.path.append('./src')
from music_tonnetztransform.music_tonnetztransform import Transform
import unittest

class TestNeoRiemannianTonnetz(unittest.TestCase):
  def setUp(self):
    self.Nrt = Transform()

  def test_taskify_tokens(self):
    tasks = self.Nrt.taskify_tokens('P')
    self.assertEqual(len(tasks), 1, 'single step task count')
    self.assertTrue(callable(tasks[0][1]), 'task is code ref')

    tasks = self.Nrt.taskify_tokens('N')  # should expand to RLP
    self.assertEqual(len(tasks), 3, 'three step task count')
    self.assertEqual(
      sum(1 for t in tasks if callable(t[1])), 3, 'three little code refs'
    )

  def test_techno(self):
    techno = ['tonn', 'tz'] * 8
    even_more_techno = ['tonn', 'tz'] * 32
    self.assertEqual(list(self.Nrt.techno()), techno, 'tonn tz')
    self.assertEqual(list(self.Nrt.techno(4)), even_more_techno, 'even more tonn tz')

  def test_transform_3_11(self):
    # flip minor|major triads
    pset = self.Nrt.transform('P', [60, 63, 67])
    self.assertEqual(pset, [60, 64, 67], 'P - minor triad to major')
    pset = self.Nrt.transform('P', pset)
    self.assertEqual(pset, [60, 63, 67], 'P - major triad to minor')

    # should be a no-op, repeated P just toggle the 3rd back and forth
    self.assertEqual(
      self.Nrt.transform('PPPP', [57, 60, 64]),
      [57, 60, 64],
      'PPPP toggle'
    )

    # unsupported pitch set (for now)
    with self.assertRaises(Exception):
      self.Nrt.transform('P', [0, 1, 2])

    self.assertEqual(
      self.Nrt.transform('R', [57, 60, 64]),
      [55, 60, 64],
      'R - A minor to C major'
    )
    self.assertEqual(
      self.Nrt.transform('R', [60, 64, 67]),
      [60, 64, 69],
      'R - C major to A minor'
    )

    self.assertEqual(
      self.Nrt.transform('L', [57, 60, 64]),
      [57, 60, 65],
      'L - A minor to F major'
    )
    self.assertEqual(
      self.Nrt.transform('L', [60, 64, 67]),
      [59, 64, 67],
      'L - C major to E minor'
    )

    self.assertEqual(
      self.Nrt.transform('N', [57, 60, 64]),
      [56, 59, 64],
      'N - A minor to E major'
    )
    self.assertEqual(
      self.Nrt.transform('N', [60, 64, 67]),
      [60, 65, 68],
      'N - C major to F minor'
    )

    self.assertEqual(
      self.Nrt.transform('RLP', [57, 60, 64]),
      [56, 59, 64],
      'RLP - A minor to E major'
    )

    self.assertEqual(
      self.Nrt.transform('S', [60, 64, 67]),
      [61, 64, 68],
      'S - C major to C# minor'
    )
    self.assertEqual(
      self.Nrt.transform('S', [61, 64, 68]),
      [60, 64, 67],
      'S - C# minor to C major'
    )

    self.assertEqual(
      self.Nrt.transform('H', [60, 64, 67]),
      [59, 63, 68],
      'H - C major to Ab minor'
    )
    self.assertEqual(
      self.Nrt.transform('H', [59, 63, 68]),
      [60, 64, 67],
      'H - Ab minor to C major'
    )

  def test_transform_4_27(self):
    # Via table in [Childs 1998] p.186
    self.assertEqual(
      self.Nrt.transform('S23', [65, 69, 72, 75]),
      [65, 68, 71, 75],
      'S23 - F+ to F-'
    )
    self.assertEqual(
      self.Nrt.transform('S32', [65, 69, 72, 75]),
      [66, 69, 72, 76],
      'S32 - F+ to F#-'
    )
    self.assertEqual(
      self.Nrt.transform('S34', [65, 69, 72, 75]),
      [66, 70, 72, 75],
      'S34 - F+ to C-'
    )
    self.assertEqual(
      self.Nrt.transform('S43', [65, 69, 72, 75]),
      [65, 69, 71, 74],
      'S43 - F+ to B-'
    )
    self.assertEqual(
      self.Nrt.transform('S56', [65, 69, 72, 75]),
      [65, 68, 72, 74],
      'S56 - F+ to D-'
    )
    self.assertEqual(
      self.Nrt.transform('S65', [65, 69, 72, 75]),
      [66, 69, 73, 75],
      'S65 - F+ to D#-'
    )
    self.assertEqual(
      self.Nrt.transform('C32', [65, 69, 72, 75]),
      [66, 69, 72, 74],
      'C32 - F+ to D+'
    )
    self.assertEqual(
      self.Nrt.transform('C34', [65, 69, 72, 75]),
      [66, 68, 72, 75],
      'C34 - F+ to Ab+'
    )
    self.assertEqual(
      self.Nrt.transform('C65', [65, 69, 72, 75]),
      [66, 69, 71, 75],
      'C65 - F+ to B+'
    )

    self.assertEqual(
      self.Nrt.transform('S23', [65, 68, 71, 75]),
      [65, 69, 72, 75],
      'S23 - F- to F+'
    )
    self.assertEqual(
      self.Nrt.transform('S32', [65, 68, 71, 75]),
      [64, 68, 71, 74],
      'S32 - F- to E+'
    )
    self.assertEqual(
      self.Nrt.transform('S34', [65, 68, 71, 75]),
      [65, 68, 70, 74],
      'S34 - F- to Bb+'
    )
    self.assertEqual(
      self.Nrt.transform('S43', [65, 68, 71, 75]),
      [66, 69, 71, 75],
      'S43 - F- to B+'
    )
    self.assertEqual(
      self.Nrt.transform('S56', [65, 68, 71, 75]),
      [66, 68, 72, 75],
      'S56 - F- to Ab+'
    )
    self.assertEqual(
      self.Nrt.transform('S65', [65, 68, 71, 75]),
      [65, 67, 71, 74],
      'S65 - F- to G+'
    )
    self.assertEqual(
      self.Nrt.transform('C32', [65, 68, 71, 75]),
      [66, 68, 71, 74],
      'C32 - F- to G#-'
    )
    self.assertEqual(
      self.Nrt.transform('C34', [65, 68, 71, 75]),
      [65, 68, 72, 74],
      'C34 - F- to D-'
    )
    self.assertEqual(
      self.Nrt.transform('C65', [65, 68, 71, 75]),
      [65, 69, 71, 74],
      'C65 - F- to B-'
    )

if __name__ == '__main__':
  unittest.main()
