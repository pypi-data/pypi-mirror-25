from binascii import unhexlify

from stp_core.crypto.util import ed25519SkToCurve25519, ed25519PkToCurve25519


def testNodesConnectedUsingConvertedKeys(nodeSet, up):
    for node in nodeSet:
        secretKey = ed25519SkToCurve25519(node.nodestack.keyhex)
        publicKey = ed25519PkToCurve25519(node.nodestack.verhex)
        assert unhexlify(node.nodestack.prihex) == secretKey
        assert unhexlify(node.nodestack.pubhex) == publicKey

        secretKey = ed25519SkToCurve25519(node.clientstack.keyhex)
        publicKey = ed25519PkToCurve25519(node.clientstack.verhex)
        assert unhexlify(node.clientstack.prihex) == secretKey
        assert unhexlify(node.clientstack.pubhex) == publicKey


def testClientConnectedUsingConvertedKeys(nodeSet, up, client1, replied1):
    secretKey = ed25519SkToCurve25519(client1.nodestack.keyhex)
    publicKey = ed25519PkToCurve25519(client1.nodestack.verhex)
    assert unhexlify(client1.nodestack.prihex) == secretKey
    assert unhexlify(client1.nodestack.pubhex) == publicKey
