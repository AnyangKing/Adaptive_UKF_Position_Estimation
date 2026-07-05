import unittest
import numpy as np
from blind_association import associate_array
from config import ChannelConfig
from run_validation_test import extract_records


class BlindAssociationTest(unittest.TestCase):
    def test_true_prior_associates_clean_triplets(self):
        position = np.array([150.0, 40.0, -45.0]); cfg = ChannelConfig(seed=29001, snr_db=30.0)
        records = extract_records(position, cfg); associations = associate_array(records, position, cfg)
        for record, association in zip(records, associations):
            truth = np.array([p.delay_s for p in record["true_paths"]])
            self.assertTrue(np.all(np.abs(association["times_s"] - truth) < 2/12000))


if __name__ == "__main__": unittest.main()
