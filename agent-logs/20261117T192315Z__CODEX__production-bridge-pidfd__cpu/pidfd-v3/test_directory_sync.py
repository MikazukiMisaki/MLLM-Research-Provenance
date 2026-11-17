"""Fake filesystem fault injection: no child is ever spawned."""
import errno
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from owner import Owner

class DirectorySyncTests(unittest.TestCase):
    def test_parent_fsync_failure_prevents_owner_and_spawn(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent=Path(tmp);root=parent/'owner';identity=os.stat(parent)
            real=os.fsync;observed=[]
            def inject(fd):
                st=os.fstat(fd);observed.append((st.st_dev,st.st_ino))
                if (st.st_dev,st.st_ino)==(identity.st_dev,identity.st_ino):
                    raise OSError(errno.EIO,'synthetic parent fsync failure')
                return real(fd)
            with mock.patch('owner.os.fsync',side_effect=inject),mock.patch('owner.subprocess.Popen') as spawn:
                with self.assertRaises(OSError) as error:Owner(root)
                self.assertEqual(error.exception.errno,errno.EIO);spawn.assert_not_called()
            self.assertTrue(root.is_dir());self.assertFalse((root/'owner.jsonl').exists())
            self.assertEqual(observed[0],(identity.st_dev,identity.st_ino))
            print('EVIDENCE parent fsync failure propagated; no journal or child; directory retained')
    def test_parent_directory_then_owner_directory_synced(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent=Path(tmp);root=parent/'owner';identity=os.stat(parent)
            real=os.fsync;observed=[]
            def track(fd):
                st=os.fstat(fd);observed.append((st.st_dev,st.st_ino));return real(fd)
            with mock.patch('owner.os.fsync',side_effect=track),mock.patch('owner.subprocess.Popen') as spawn:
                owner=Owner(root);spawn.assert_not_called()
            root_st=os.stat(root);file_st=os.stat(root/'owner.jsonl')
            self.assertEqual(observed[:3],[(identity.st_dev,identity.st_ino),
                (root_st.st_dev,root_st.st_ino),(file_st.st_dev,file_st.st_ino)])
            self.assertTrue(owner.durable);self.assertEqual(owner.state,'NEW')
            print('EVIDENCE observed fsync order parent directory, owner directory, journal')

if __name__=='__main__':unittest.main(verbosity=2)
