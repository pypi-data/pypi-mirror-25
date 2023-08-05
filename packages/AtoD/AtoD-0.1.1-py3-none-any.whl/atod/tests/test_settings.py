import os
import unittest

from atod import files


class TestSettings(unittest.TestCase):
    ''' Class to test atod.files.py files

        Checks existance of all the needed files.
    '''
    def test_existance(self):
        ''' Tests existance of files mentioned in settings.

            Files names variables have caps-locked names.
        '''
        settings_dir = dir(files)

        paths_names = ['FOLDER', 'PATH', 'FILE']

        files = [d for d in settings_dir if
                            any(map(lambda x: x in d, paths_names))]

        paths = [getattr(files, file_) for file_ in files]

        paths_tested = 0
        for path in paths:
            self.assertEqual(os.path.exists(path), True)
            paths_tested += 1


if __name__ == '__main__':
    unittest.main()
