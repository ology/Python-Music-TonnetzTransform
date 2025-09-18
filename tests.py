import sys
sys.path.append('./src')
from music_tonnetztransform.neo_riemann_tonnetz import Tonnetz
from music_tonnetztransform.music_tonnetztransform import Transform
import unittest

class TestNeoRiemannianTonnetz(unittest.TestCase):
  def setUp(self):
    self.Nrt = Tonnetz()

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

class TestTransform(unittest.TestCase):
    def test_defaults(self):
        t = Transform(format="ISO")
        self.assertEqual(t.base_chord, [60, 64, 67])

    def test_generate_default(self):
        t = Transform()
        self.assertEqual(len(t.generate()[0]), 4)

    def test_circular_default(self):
        t = Transform()
        self.assertEqual(len(t.circular()[0]), 4)

    def test_transform_array(self):
        t = Transform(transforms=['O','P','T2'])
        self.assertEqual(t.generate()[0], [[60,64,67],[60,63,67],[62,65,69]])

    def test_transform_integer(self):
        t = Transform(transforms=3)
        self.assertEqual(len(t.generate()[0]), 3)

    def test_transform_base(self):
        t = Transform(base_note='G', base_octave=5)
        self.assertEqual(len(t.generate()[0]), 4)

    def test_ISO_format(self):
        t = Transform(format='ISO', transforms=['O'])
        self.assertEqual(t.generate()[0][0], ['C4','E4','G4'])

    def test_circular(self):
        t = Transform(transforms=['I','P','T2'], max=4)
        got = t.circular()[0]
        self.assertEqual(len(got), 4)
        self.assertEqual(got[0], [60,64,67])

    def test_t_quality(self):
        t = Transform(chord_quality='7', transforms=['I','T1','T2','T-3'])
        got = t.generate()[0]
        self.assertEqual(len(got), 4)
        self.assertEqual(got, [[60,64,67,70],[61,65,68,71],[63,67,70,73],[60,64,67,70]])

    def test_nro_quality(self):
        t = Transform(chord_quality='7', transforms=['I','C32','C34','C65'])
        got = t.generate()[0]
        self.assertEqual(len(got), 4)
        self.assertEqual(got, [[60,64,67,70],[61,64,67,69],[60,64,67,70],[61,64,66,70]])

    def test_transformation(self):
        t = Transform(format='ISO', transforms=['R','L','P'])
        rlp = t.generate()[0]
        self.assertEqual(rlp, [['C4', 'E4', 'A4'], ['C4', 'F4', 'A4'], ['C4', 'F4', 'G#4']])
        t = Transform(format='ISO', transforms=['L','P','R'])
        lpr = t.generate()[0]
        self.assertEqual(lpr, [['B3', 'E4', 'G4'], ['B3', 'E4', 'G#4'], ['C#4', 'E4', 'G#4']])
        t = Transform(format='ISO', transforms=['L','P','L'])
        lpl = t.generate()[0]
        self.assertEqual(lpl, [['B3', 'E4', 'G4'], ['B3', 'E4', 'G#4'], ['B3', 'Eb4', 'G#4']])
        t = Transform(format='ISO', transforms=['N'])
        n = t.generate()[0]
        self.assertEqual(n[0], rlp[-1])
        t = Transform(format='ISO', transforms=['S'])
        s = t.generate()[0]
        self.assertEqual(s[0], lpr[-1])
        t = Transform(format='ISO', transforms=['H'])
        h = t.generate()[0]
        self.assertEqual(h[0], lpl[-1])

    # def test_example(self):
    #     from music21 import duration, chord, stream
    #     from random_rhythms import Rhythm
    #     s = stream.Stream()
    #     p = stream.Part()
    #     r = Rhythm(durations=[1, 3/2, 2])
    #     motif = r.motif()
    #     t = Transform(max=len(motif))
    #     generated = t.generate()[0]
    #     print(generated)
    #     for i,dura in enumerate(motif):
    #         c = chord.Chord(generated[i])
    #         c.duration = duration.Duration(dura)
    #         p.append(c)
    #     s.append(p)
    #     s.show()

if __name__ == '__main__':
  unittest.main()
