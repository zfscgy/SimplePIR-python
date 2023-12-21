from typing import List, Collection

import numpy as np
np.seterr(over='ignore')

from params import Params
from discrete_gaussian import default_sampler


class PIRServer:
    def __init__(self, database: Collection[int]):
        self.plain_modulus = Params.get_plaintext_modulus(len(database))
        if np.max(database) >= self.plain_modulus or np.min(database) < 0:
            raise ValueError(f"Database elements shall not exceed the plaintext_modulus {self.plain_modulus} "
                             f"or be negative!")

        n_rows = n_cols = np.ceil(np.sqrt(len(database))).astype(int)
        self.data_matrix = np.zeros((n_rows, n_cols), dtype=np.uint32)
        index1d = np.arange(0, len(database))
        row_ind = index1d // n_cols
        col_ind = index1d % n_cols
        self.data_matrix[row_ind, col_ind] = database
        self.lwe_mat = np.random.randint(0, 2**32, [n_cols, Params.secret_dimension], dtype=np.uint32)

    def get_scale_factor(self):
        return (2 ** 32) // self.plain_modulus

    def setup(self):
        """
        Send the client hint to the client
        :return:
        """
        client_hint = self.data_matrix @ self.lwe_mat
        return client_hint

    def answer(self, query: np.ndarray):
        return self.data_matrix @ query


class PIRClient:
    def __init__(self, lwe_mat: np.ndarray, hint: np.ndarray, scale_factor: int):
        self.lwe_mat = lwe_mat
        self.hint = hint
        self.secret = np.random.randint(0, 2**32, [Params.secret_dimension], dtype=np.uint32)
        self.scale_factor = scale_factor
        self.n_rows = hint.shape[0]
        self.n_cols = lwe_mat.shape[0]

    def query(self, index: int):
        col_id = index % self.n_cols
        noise = default_sampler.sample_dgaussian(self.n_rows).astype(np.uint32)
        row_selection = np.zeros([self.n_rows], dtype=np.uint32)
        row_selection[col_id] = 1
        return self.lwe_mat @ self.secret + noise + self.scale_factor * row_selection

    def recover(self, index: int, answer: np.ndarray):
        row_id = index // self.n_cols
        col_id = index % self.n_cols
        d = answer[row_id] - self.hint[row_id] @ self.secret
        # Round d to its nearest multiple of scale_factor
        d = (d + self.scale_factor // 2) // self.scale_factor
        return d


if __name__ == '__main__':
    database = np.random.randint(0, 1000, [1000 * 1000], dtype=np.uint32)
    pir_server = PIRServer(database)
    pir_client = PIRClient(pir_server.lwe_mat, pir_server.setup(), pir_server.get_scale_factor())

    index = 123456
    q = pir_client.query(index)
    ans = pir_server.answer(q)
    r = pir_client.recover(index, ans)

    print(f"Expected {database[index]}, get {r}")
