# SimplePIR-python

This repository is a python implementation of the SimplePIR protocol based on the **Learning with Errors** algorithm, proposed in the USENIX'23 paper:

 [One Server for the Price of Two:Simple and Fast Single-Server Private Information Retrieval (full length)](https://eprint.iacr.org/2022/949.pdf)

**Citation for the original paper**

```
@inproceedings{cryptoeprint:2022/949,
      author = {Alexandra Henzinger and Matthew M. Hong and Henry Corrigan-Gibbs and Sarah Meiklejohn and Vinod Vaikuntanathan},
      title = {One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval},
      booktitle = {32nd USENIX Security Symposium (USENIX Security 23)},
      year = {2023},
      address = {Anaheim, CA},
      url = {https://www.usenix.org/conference/usenixsecurity23/presentation/henzinger},
      publisher = {USENIX Association},
      month = aug,
}
```

The only dependency for this library is *Numpy*.

## Example Usage

```python
import numpy as np
from simple_pir.pir import PIRServer, PIRClient

# Randomly initialize the database, where each entry is a integer in 0...999
database = np.random.randint(0, 1000, [1000 * 1000], dtype=np.uint32)

pir_server = PIRServer(database)

# pir_server.setup() method returns the client hint
pir_client = PIRClient(pir_server.lwe_mat, pir_server.setup(), pir_server.get_scale_factor())

index = 123456
q = pir_client.query(index)
ans = pir_server.answer(q)
r = pir_client.recover(index, ans)

print(f"Expected {database[index]}, get {r}")
```

Notice that, in this implementation, each database entry is only a small integer whose upper bound can be computed via the database size, in order to meet security&correctness standards, using the bound computed in *Theorem C.1* in the paper.

If your database contain larger records, you can split one record into multiple "small integers". Also, there are several optimization methods in the original paper which may be helpful.

## Security Notice

* This repository is for research purpose only. The developer takes no responsibility on the security of this code.

* PIR only protects the client privacy. **The database privacy is not protected**, i.e., the client can recover the whole row in that database. If you want to achieve server-side privacy, please use a modified protocol.

## Related Resources

1. The original implementation in Go: [github.com/ahenzinger/simplepir](https://github.com/ahenzinger/simplepir/tree/main)
2. An estimator used to estimate the LWE hardness, which is used to compute the parameters in the original paper: [github.com/malb/lattice-estimator: An attempt at a new LWE estimator (github.com)](https://github.com/malb/lattice-estimator/)

