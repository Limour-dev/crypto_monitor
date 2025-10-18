from bip_utils import (
    Bip39WordsNum,
    Bip39MnemonicGenerator,
    Bip39MnemonicValidator,
    Bip39Languages,
    MnemonicChecksumError
)
from bip_utils.bip.bip39.bip39_mnemonic_utils import Bip39WordsListGetter
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

english_words = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
english_words = english_words.m_idx_to_words

mnemo_g =  Bip39MnemonicGenerator(Bip39Languages.ENGLISH)
mnemonic = str(mnemo_g.FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)).split(' ')

max_ws = len(english_words)
for i in range(0, 24, 2):
    print(i, mnemonic[i])
    while True:
        try:
            et = int(input(f'请输入一个 1 到 {max_ws} 随机的整数：'))
            break
        except:
            pass
    print(i, english_words[et % max_ws])
    mnemonic[i] = english_words[et % max_ws]

mnemo_v = Bip39MnemonicValidator(Bip39Languages.ENGLISH)
tmp_mnemonic = ' '.join(mnemonic[:-1]) + ' '
possible_last_words = []
for bip39w in english_words:
    mnemonic_candidate = tmp_mnemonic + bip39w
    try:
        mnemo_v.Validate(mnemonic_candidate)
        possible_last_words.append(bip39w)
    except MnemonicChecksumError:
        pass

print(possible_last_words)
et = int(input(f'请输入一个 1 到 {len(possible_last_words)} 随机的整数：'))
mnemonic[-1] = possible_last_words[et % max_ws]

seed_bytes = Bip39SeedGenerator(' '.join(mnemonic)).Generate()
bip44_eth_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
addr_index0 = (bip44_eth_ctx.Purpose().Coin().
               Account(0). # 用来区分不同账户，方便记账和管理
               Change(Bip44Changes.CHAIN_EXT).
               AddressIndex(1)) # 用来防止地址重复使用，提高隐私性, 更适合频繁生成新地址的场景

print("ETH 助记词:", ' '.join(mnemonic))
print("ETH 地址:", addr_index0.PublicKey().ToAddress())
print("ETH 私钥(hex):", addr_index0.PrivateKey().Raw().ToHex())
