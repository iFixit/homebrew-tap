import hashlib
from pathlib import Path
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location

spec = spec_from_file_location('update_formula', Path(__file__).with_name('update-formula.py'))
module = module_from_spec(spec)
spec.loader.exec_module(module)


class FormulaTests(unittest.TestCase):
    def test_rejects_missing_or_mismatched_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for target in module.TARGETS:
                name = f'ifixit-v1.2.3-{target}.tar.gz'
                (directory / name).write_bytes(target.encode())
                digest = hashlib.sha256(target.encode()).hexdigest()
                (directory / f'{name}.sha256').write_text(f'{digest}  {name}\n')
            checksums = module.verified_checksums('1.2.3', directory)
            formula = module.render_formula('1.2.3', checksums)
            for target, digest in checksums.items():
                self.assertIn(f'ifixit-v1.2.3-{target}.tar.gz', formula)
                self.assertIn(digest, formula)
            (directory / 'ifixit-v1.2.3-linux-x64.tar.gz').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                module.verified_checksums('1.2.3', directory)

    def test_rejects_untrusted_version_and_checksum_text(self):
        checksums = {target: 'a' * 64 for target in module.TARGETS}
        for version in ('../1', '1.2.3-rc.1', '1.2.3"; system "bad'):
            with self.assertRaises(ValueError):
                module.render_formula(version, checksums)
        checksums['linux-x64'] = 'invalid'
        with self.assertRaises(ValueError):
            module.render_formula('1.2.3', checksums)


unittest.main()
