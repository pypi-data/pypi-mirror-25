import mock
import unittest
import uuid

from ambisafe_tenant.crypt import Crypt


class SignaturesTestCase(unittest.TestCase):

    @mock.patch.object(uuid, 'uuid4')
    def test_signatures_setup(self, mock_nonce):
        mock_nonce.side_effect = ['286cff6d-a12c-4414-94fb-7cde0f3dbb22']
        c = Crypt('75f24a36fbff3e57717b6badf82d3bbca56993dd', '278a5de700e29faae8e40e366ec5012b5ec63d36ec77e8a2417154cc1d25383f')
        sig = c.get_recovery_tenant_signatures()
        self.assertEqual(sig.get('nonce'), '286cff6d-a12c-4414-94fb-7cde0f3dbb22')
        self.assertEqual(sig.get('r'), '0x2e900401c604aa02544c18bb23e424c7df5673d8fe9d6cb89941fa3a30c34562')
        self.assertEqual(sig.get('s'), '0x6f2280f970e6fa6c8382cd8feacab1e65da490092230d479b4d7842a8bc8a39a')
        self.assertEqual(sig.get('v'), '28')

    @mock.patch.object(uuid, 'uuid4')
    def test_signatures_recovery_request(self, mock_nonce):
        mock_nonce.side_effect = ['5cfae0ae-cc4b-4b7f-8cc9-3ce1e45d95d0']
        c = Crypt('75f24a36fbff3e57717b6badf82d3bbca56993dd75f24a36fbff3e57717b6badf82d3bbca56993ee',
                  '278a5de700e29faae8e40e366ec5012b5ec63d36ec77e8a2417154cc1d25383f')
        sig = c.get_recovery_tenant_signatures()
        self.assertEqual(sig.get('nonce'), '5cfae0ae-cc4b-4b7f-8cc9-3ce1e45d95d0')
        self.assertEqual(sig.get('r'), '0x4f0e49c23cde0416cbee3d565e49ece924e169d7746165ff32d7b0af8f97ee34')
        self.assertEqual(sig.get('s'), '0x00c1ae9ac91873f37ff3e6a100d61e796149dc546f0c4d38394e8748b976cdcd')
        self.assertEqual(sig.get('v'), '27')

if __name__ == '__main__':
    unittest.main()