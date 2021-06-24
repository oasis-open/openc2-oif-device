"""
Test Format Conversion
"""
import json
import os
import unittest

from pathlib import Path
from tempfile import TemporaryFile
from typing import Dict, Union
from xml.dom import minidom
from beautifultable import BeautifulTable
from sb_utils import Message, SerialFormats
from .utils import MetaTests, sizeof_fmt

test_dir = os.path.dirname(os.path.realpath(__file__))


class FormatTests(unittest.TestCase, metaclass=MetaTests):
    msg_dir = os.path.join(test_dir, 'messages')
    msg_files: Dict[str, dict]
    sizes: Dict[str, Dict[str, Dict[str, int]]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.msg_files = {}
        cls.sizes = {}

    @classmethod
    def tearDownClass(cls) -> None:
        with open(os.path.join(test_dir, '../sizes.md'), 'w') as f:
            f.write('# Message Sizes\n\n')
            for test, results in cls.sizes.items():
                f.write(f'## {test}')
                # Format Sizes
                table = BeautifulTable()
                table.set_style(BeautifulTable.STYLE_MARKDOWN)
                table.columns.header = ["Request", "Response", "Notification"]
                row_headers = []

                for fmt, msgs in results.items():
                    row_headers.append(fmt)
                    table.rows.append([sizeof_fmt(msgs[c]) if c in msgs else 'N/A' for c in table.columns.header])
                table.rows.header = row_headers
                f.write(f'\n{table}\n\n')

    def _getSize(self, msg: Message, file: str) -> None:
        m = msg.oc2_message(True)
        f = ' '.join(map(str.capitalize, os.path.splitext(
            os.path.split(file)[1])[0].split('_')))
        with TemporaryFile(mode='wb' if isinstance(m, bytes) else 'w') as tf:
            tf.write(m)
            tf.flush()
            self.sizes.setdefault(f, {}).setdefault(msg.content_type.name, {})[
                msg.msg_type.name] = tf.tell()

    def _load_msg(self, msg_file: str, fmt: SerialFormats) -> Message:
        file_fmt = SerialFormats.from_value(os.path.splitext(msg_file)[1][1:])
        if msg_file in self.msg_files:
            m = self.msg_files[msg_file]
        else:
            msg = Path(msg_file)
            m = msg.read_bytes() if SerialFormats.is_binary(file_fmt) else msg.read_text()
        try:
            msg = Message.oc2_loads(m, file_fmt)
        except Exception as e:
            err = f'{msg_file} - {e}'
            raise Exception(err)
        msg.content_type = fmt
        self._getSize(msg, msg_file)
        return msg

    def _equality(self, msg1: Union[bytes, str], msg2: Union[bytes, str], fmt: SerialFormats, equal=True) -> None:
        # TODO: Add more format comparisons?
        if fmt == SerialFormats.JSON:
            msg1 = json.loads(msg1)
            msg2 = json.loads(msg2)
            if equal:
                self.assertDictEqual(msg1, msg2)
            else:
                self.assertRaises(
                    AssertionError, self.assertDictEqual(msg1, msg2))
        elif fmt == SerialFormats.XML:
            msg1 = minidom.parseString(
                ''.join(map(str.lstrip, msg1.split('\n')))).toxml()
            msg2 = minidom.parseString(msg2).toxml()

        if equal:
            self.assertEqual(msg1, msg2)
        else:
            self.assertNotEqual(msg1, msg2)

    # Base tests for all messages
    def _test_good_msg(self, msg_file: str, fmt: SerialFormats) -> None:
        msg = self._load_msg(msg_file, fmt)
        file = os.path.splitext(msg_file.replace(
            'messages/input/', 'messages/output/'))[0] + f'.{fmt}'
        if os.path.isfile(file):
            m = Path(file)
            m = m.read_bytes() if SerialFormats.is_binary(fmt) else m.read_text()
            self._equality(m, msg.oc2_message(True), fmt, True)

    def _test_bad_msg(self, msg_file: str, fmt: SerialFormats) -> None:
        with self.assertRaises(Exception):
            msg = self._load_msg(msg_file, fmt)
            file = os.path.splitext(msg_file.replace(
                'messages/input/', 'messages/output/'))[0] + f'.{fmt}'
            if os.path.isfile(file):
                m = Path(file)
                m = m.read_bytes() if SerialFormats.is_binary(fmt) else m.read_text()
                self._equality(m, msg.oc2_message(True), fmt, False)

    # Tests are generated via the metaclass


if __name__ == "__main__":
    unittest.main()
