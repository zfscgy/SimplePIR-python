import numpy as np


class Params:
    """
    We follow the original paper's implementation, where the secret dimension and the ciphertext modulus is fixed.
    The database size
    """
    secret_dimension = 1024
    ciphertext_modulus = 2 ** 32

    @classmethod
    def get_plaintext_modulus(cls, database_size: int):
        return np.floor((cls.ciphertext_modulus / (2 ** 0.5 * 6.4 * database_size ** 0.25 * 40 ** 0.5)) ** 0.5).astype(int)


if __name__ == '__main__':
    for i in range(15, 30):
        print(f"Database size = 2^{i}, pt modulus={Params.get_plaintext_modulus(2**i)}")