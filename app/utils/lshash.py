from typing import List

import numpy as np
import numpy.typing as npt


class RandomProjectionHasher:
    # Code modified from: https://github.com/loretoparisi/lshash
    def __init__(self, hash_size: int, input_dim: int, seed: int = 42):
        self.hash_size = hash_size
        self.input_dim = input_dim
        self.seed = seed
        self.planes = self._generate_uniform_planes()

    def _generate_uniform_planes(self):
        rs = np.random.RandomState(seed=self.seed)
        return rs.randn(self.hash_size, self.input_dim)

    def hash(self, input_point: npt.ArrayLike) -> str:
        """Generates the binary hash for `input_point` and returns it.
        :param input_point:
        A Python tuple or list object that contains only numbers.
        Needs to be 1-dimensional, with size `input_dim`.
        """
        input_point = np.array(input_point)
        projections = np.dot(input_point, self.planes.T)
        return "".join(["1" if i > 0 else "0" for i in projections])

    def hash_bulk(self, input_points: npt.ArrayLike) -> List[str]:
        """

        :rtype: object
        """
        projections_list = np.dot(input_points, self.planes.T)
        return [
            "".join(projections)
            for projections in (projections_list > 0).astype(int).astype(str)
        ]
