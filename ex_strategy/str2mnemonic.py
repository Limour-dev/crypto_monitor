from bip_utils import (
    Bip39MnemonicValidator,
    Bip39Languages,
    MnemonicChecksumError,
    Bip39MnemonicGenerator
)
from bip_utils.bip.bip39.bip39_mnemonic_utils import Bip39WordsListGetter
from hashlib import sha256

english_words = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
english_words_idx = english_words.m_words_to_idx
english_words = english_words.m_idx_to_words

sha256_hash  = sha256()
entropy_1 = input('请输入一段文字，无标点无空格：').strip()
entropy_2 = input('请输入一段口令：').strip()
sha256_hash.update((entropy_1 + entropy_2).encode(encoding='utf-8'))
entropy = sha256_hash.digest()

# 基于 entropy 创建，entropy 相同则值不变，24 个词
mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy).ToStr().split(' ')

print("ETH 原始助记词:", ' '.join(mnemonic))

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

print("ETH 可变助记词:", possible_last_words)
